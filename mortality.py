import libtcodpy as libtcod

from game_states import *
from render_functions import RenderOrder

def death(player, entity):
    entity.char = '%'
    entity.color = libtcod.dark_red
    if player == True:
        return 'You died!', GameStates.PLAYER_DEAD
    else:
        entity.render_order = RenderOrder.CORPSE
        death_message = '{0} dies!'.format(entity.name.capitalize())
        entity.blocks = False
        entity.fighter = None
        entity.ai = None
        entity.name = 'remains of ' + entity.name
        return death_message

def kill_monster(monster):
    death_message = '{0} dies!'.format(monster.name.capitalize())
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    return death_message