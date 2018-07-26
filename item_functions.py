import libtcodpy as libtcod
from ai import *
from render_functions import RenderOrder
from random_utils import *
from warfighter import *

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

def cast_animate_dead(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    number = kwargs.get('number')
    monchances = {
        'undead':10-number,
        'undeads':1
    }
    results = []
    target = None
    closest_distance = 10000
    for entity in entities:
        if entity.render_order == RenderOrder.CORPSE and entity.undead == False and entity != caster and entity.visible:
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
            fighter_component = fighter(hp=15, defense=1, power=3, xp=1)
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
            entity.name = 'Undead Stalker'
            fighter_component = fighter(hp=15, defense=1, power=4, xp=2)
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