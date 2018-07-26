import libtcodpy as libtcod

from game_messages import Message
from game_states import *
from render_functions import RenderOrder

def death(entity):
    if entity.undead == False:
        entity.char = '%'
        entity.color = libtcod.dark_red
        entity.render_order = RenderOrder.CORPSE
        death_message = Message('{0} dies!'.format(entity.name.capitalize()), libtcod.yellow)
        entity.blocks = False
        entity.fighter = None
        entity.ai = None
        entity.moncaster = None
        entity.name = 'remains of ' + entity.name
        return death_message
    else:
        entity.char = '%'
        entity.color = libtcod.white
        entity.render_order = RenderOrder.CORPSE
        death_message = Message('{0} dies again!'.format(entity.name.capitalize()), libtcod.yellow)
        entity.blocks = False
        entity.fighter = None
        entity.ai = None
        entity.moncaster = None
        entity.name = 'remains of ' + entity.name
        return death_message

def kill_monster(monster):
    death_message = '{0} dies!'.format(monster.name.capitalize())
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Remains of ' + monster.name
    return death_message

def destroy_item(equip):
    death_message = Message('Your {0} is destroyed!'.format(equip.name.capitalize()), libtcod.yellow)
    equip.char = '`'
    equip.color = libtcod.dark_grey
    equip.name = 'Remains of ' + equip.name
    return death_message
def end_item(equip):
    equip.equippable = None
    equip.item = None