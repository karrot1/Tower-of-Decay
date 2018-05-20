import libtcodpy as libtcod

from warfighter import *
from inventory import Inventory
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from GameMap import Map
from render_functions import RenderOrder

def get_constants():
    window_title = 'Reverse Crawl'
    screen_width = 80
    screen_height = 25

    bar_width = 20
    panel_height = 5
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height -1

    map_width = 80
    map_height = screen_height - panel_height

    room_max_size = 10
    room_min_size = 5
    max_rooms = 15

    max_monsters_per_room = 3
    max_items_per_room = 2
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': libtcod.darker_grey,
        'dark_ground': libtcod.darker_grey,
        'light_wall': libtcod.grey,
        'light_ground': libtcod.grey
    }
    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithim': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'colors': colors
    }

    return constants

def get_game_variables(constants):
    inventory_component = Inventory(20)
    fighter_component = fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component,
                    inventory=inventory_component)
    cursor = Entity(0, 0, 'X', libtcod.yellow, 'Cursor', blocks=False, render_order=RenderOrder.CURSOR, visible=False)
    entities = [player, cursor]
    game_map = Map(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_room'],
                      constants['max_items_per_room'])
    game_state = GameStates.PLAYERS_TURN

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    return player, entities, game_map, message_log, game_state, cursor