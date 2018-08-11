import libtcodpy as libtcod
from ai import *
from render_functions import RenderOrder
from random_utils import *
from warfighter import *
from entity import *
from GameMap import *
from game_messages import Message

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')
    results = []
    is_item = kwargs.get('isitem')
    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health.')})
    else:
        results.append(entity.fighter.heal(amount))
        results.append({'consumed': True, 'message': Message('Your wounds stitch themselves closed!', libtcod.green)})
    return results

def restoremp(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')
    results = []
    is_item = kwargs.get('isitem')
    if entity.spellcaster.mp == entity.spellcaster.max_mp:
        results.append({'consumed': False, 'message': Message('You are already at full MP.')})
    else:
        entity.spellcaster.alter_mp(amount)
        results.append({'consumed': True, 'message': Message('You feel refreshed!', libtcod.blue)})
    return results

def cast_smite(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []
    target = None
    closest_distance = maximum_range +1
    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)
            if distance < closest_distance:
                target = entity
                closest_distance = distance
                if distance < closest_distance:
                    target = entity
                    closest_distance = distance
    if target:
        findamage = max(1, damage - target.fighter.defense)
        results.append({'consumed': True, 'target': target, 'message': Message('The {0} is smote by magical power! {1} damage!'.format(target.name, findamage))})
        results.extend(target.fighter.take_damage(findamage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is within range.')})
    return results

def animate_all(*args, **kwargs):
    entities = kwargs.get('entities')
    number = kwargs.get('number')
    monchances = {
        'undead': 10 - number,
        'undeads': 1
    }
    results = []
    deadmessage = False
    for entity in entities:
        if entity.render_order == RenderOrder.CORPSE and entity.undead == False and get_blocking_entities_at_location(entities, entity.x, entity.y) is None:
            if deadmessage == False:
                results.append({'consumed': False, 'target': None, 'message': Message('The dead rise from their graves!', libtcod.yellow)})
                deadmessage = True
            monster_choice = random_choice_from_dict(monchances)
            if monster_choice == 'undead':
                entity.name = 'Zombie'
                fighter_component = fighter(hp=5, defense=0, power=3, xp=1)
                ai_component = BasicMonster()
                entity.char = '%'
                entity.color = libtcod.dark_green
                entity.render_order = RenderOrder.ACTOR
                entity.blocks = True
                fighter_component.owner = entity
                entity.fighter = fighter_component
                entity.ai = ai_component
                ai_component.owner = entity
                entity.moncaster = None
                entity.undead = True
            else:
                entity.name = 'Greater Zombie'
                fighter_component = fighter(hp = 10, defense = 0, power = 4, xp = 2)
                ai_component = BasicMonster()
                entity.char = '%'
                entity.color = libtcod.dark_green
                entity.render_order = RenderOrder.ACTOR
                entity.blocks = True
                fighter_component.owner = entity
                entity.fighter = fighter_component
                entity.ai = ai_component
                ai_component.owner = entity
                entity.moncaster = None
                entity.undead = True
    return results

def summon_demons(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    number = kwargs.get('number')
    game_map = kwargs.get('gamemap')
    results = []
    monchances = {
        'thorror':10,
        'hhound':10,
        'ablob':10
    }
    castx = caster.x
    casty = caster.y
    i = 0
    monsterssummoned = 0
    messageyet = False
    while i<8 and monsterssummoned < number:
        x = castx
        y = casty
        if i == 0:
            y = casty + 1
        elif i == 1:
            x = castx + 1
            y = casty + 1
        elif i == 2:
            x = castx + 1
        elif i == 3:
            x = castx + 1
            y = casty - 1
        elif i == 4:
            y = casty -1
        elif i == 5:
            y = casty -1
            x = castx -1
        elif i == 6:
            x = castx -1
        elif i == 7:
            x = castx -1
            y = casty +1

        if (get_blocking_entities_at_location(entities, x, y) is None) and game_map.is_blocked(x, y) == False:
            if messageyet == False:
                results.append({'message': Message('The {0} summons things from beyond the void!'.format(caster.name))})
                messageyet = True
            monster_choice = random_choice_from_dict(monchances)
            if monster_choice == 'thorror':
                fighter_component = fighter(hp=4, defense=5, power=8, xp=5)
                ai_component = BasicMonster()
                monster = Entity(x, y, '*', libtcod.darkest_blue, 'Tentacled Horror', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
            elif monster_choice == 'hhound':
                fighter_component = fighter(hp=10, defense=1, power=4, xp=3)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'h', libtcod.orange, 'Hellhound', blocks=True, render_order=RenderOrder.ACTOR,
                         fighter=fighter_component, ai=ai_component)
            else:
                fighter_component = fighter(hp=5, defense=0, power=2, xp=2)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'B', libtcod.celadon, 'Amorphous Blob', blocks=True, render_order=RenderOrder.ACTOR,
                         fighter=fighter_component, ai=ai_component)
            entities.append(monster)
            monsterssummoned = monsterssummoned + 1
        i = i+1
    return results
def cast_animate_dead(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    number = kwargs.get('number')
    monchances = {
        'undead':10-number,
        'undeads':1
    }
    results = []
    target = None
    closest_distance = 10000
    for entity in entities:
        if entity.render_order == RenderOrder.CORPSE and entity.undead == False and entity != caster and entity.visible and get_blocking_entities_at_location(entities, entity.x, entity.y) is None:
            distance = caster.distance_to(entity)
            if distance < closest_distance:
                target = entity
                closest_distance = distance
                if distance < closest_distance:
                    target = entity
                    closest_distance = distance
    if target:
        results.append({'consumed': False, 'target': None, 'message': Message('The dead rise from their graves!')})
        monster_choice = random_choice_from_dict(monchances)
        if monster_choice == 'undead':
            target.name = 'Zombie'
            fighter_component = fighter(hp=5, defense=0, power=3, xp=1)
            ai_component = BasicMonster()
            target.char = '%'
            target.color = libtcod.dark_green
            target.render_order = RenderOrder.ACTOR
            target.blocks = True
            fighter_component.owner = target
            target.fighter = fighter_component
            target.ai = ai_component
            ai_component.owner = target
            target.moncaster = None
            target.undead = True
        else:
            entity.name = 'Greater Zombie'
            fighter_component = fighter(hp = 10, defense = 0, power = 4, xp = 2)
            ai_component = BasicMonster()
            target.char = '%'
            target.color = libtcod.green
            target.render_order = RenderOrder.ACTOR
            target.blocks = True
            fighter_component.owner = target
            target.fighter = fighter_component
            target.ai = ai_component
            ai_component.owner = target
            target.moncaster = None
            target.undead = True
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('The dead continue to slumber.')})
    return results

def cast_magic_missile(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    results = []
    target = None
    if not libtcod.map_is_in_fov(fov_map, target_x, target_y)and not kwargs.get('ismon'):
        results.append({'consumed': False, 'message': Message('You can not target a tile you can not see.')})
        return results
    for entity in entities:
        if entity.x == target_x and entity.y == target_y and (entity.ai or kwargs.get('ismon')):
            findamage = max(1, damage - entity.fighter.defense)
            results.append({'consumed': True, 'target': target, 'message': Message(
                'The {0} is hit by the magical missile! {1} damage!'.format(entity.name, findamage))})
            results.extend(entity.fighter.take_damage(findamage))
            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.')})
    return results

def cast_disintigrate(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    results = []
    target = None
    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You can not target a tile you can not see.')})
        return results
    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            findamage = damage - entity.fighter.defense
            results.append({'consumed': True, 'target': target, 'message': Message(
                'The {0} screams as its atoms are rent in twain! {1} damage!'.format(entity.name, findamage))})
            results.extend(entity.fighter.take_damage(findamage))
            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.')})
    return results

def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    results = []
    if not libtcod.map_is_in_fov(fov_map, target_x, target_y) and not kwargs.get('ismon'):
        results.append({'consumed': False, 'message': Message('You can not target a tile you can not see.')})
        return results
    results.append({'consumed': True, 'message': Message('The fireball explodes, doing {0} damage'.format(damage))})
    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            findamage = max(1, damage - entity.fighter.defense)
            results.append({'message': Message('The {0} is burned, taking {1} damage!'.format(entity.name, findamage))})
            results.extend(entity.fighter.take_damage(findamage))
    return results

def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You can not target a tile you can not see.')})
        return results
    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, max(0, 6 - entity.fighter.defense))
            confused_ai.owner = entity
            entity.ai = confused_ai
            results.append({'consumed': True, 'message': Message('The {0}\'s eyes glaze over.'.format(entity.name))})
            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.')})
    return results