from warfighter import *
from inventory import Inventory
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from GameMap import Map
from render_functions import RenderOrder
from level import Level
from equipment import *
from Equippable import *
from equipment_slots import *
from spellcaster import *

def get_constants():
    window_title = 'Tower of Decay'
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
    start_level = 5
    room_max_size = 10
    room_min_size = 5
    max_rooms = 25
    top_level = 20
    max_monsters_per_room = 3
    max_items_per_room = 2
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
    hp_per_level = 20
    mp_per_level = 5
    power_per_level = 2
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
        'colors': colors,
        'top_level': top_level,
        'start_level': start_level,
        'hp_per_level': hp_per_level,
        'mp_per_level': mp_per_level,
        'power_per_level': power_per_level
    }

    return constants

def get_game_variables(constants):
    inventory_component = Inventory(20)
    starting_level = 5
    level_component = Level(current_level = starting_level)
    equipment_componet = Equipment()
    fighter_component = fighter(hp=starting_level*constants['hp_per_level'], defense=0, power=starting_level*constants['power_per_level'])
    spellcaster_component = spellcaster(mp = starting_level*constants['mp_per_level'], casterl = starting_level)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component,
                    inventory=inventory_component, level = level_component, equipment=equipment_componet, spellcaster=spellcaster_component)
    cursor = Entity(0, 0, 'X', libtcod.yellow, 'Cursor', blocks=False, render_order=RenderOrder.CURSOR, visible=False)
    entities = [player, cursor]
    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus = 5)
    fsword = Entity(0, 0, '/', libtcod.red, 'Flaming Sword', render_order=RenderOrder.ITEM, equippable=equippable_component)
    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=4)
    mshield = Entity(0, 0, '[', libtcod.white, 'Mirror Shield',render_order=RenderOrder.ITEM, equippable=equippable_component)
    equippable_component = Equippable(EquipmentSlots.ARMOR, defense_bonus=6)
    parmor = Entity(0, 0, '[', libtcod.light_gray, 'Plate Armor', render_order=RenderOrder.ITEM, equippable=equippable_component)

    player.inventory.add_item(fsword)
    player.equipment.toggle_equip(fsword)
    player.inventory.add_item(mshield)
    player.equipment.toggle_equip(mshield)
    player.inventory.add_item(parmor)
    player.equipment.toggle_equip(parmor)

    game_map = Map(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities, constants['top_level'])
    game_state = GameStates.PLAYERS_TURN

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])
    floor = 0
    highest_floor = 0
    levellist = {10000:[0,0]}
    floorentities = {10000:[0,0]}
    dstairxy = {10000:[0,0]}
    ustairxy = {10000:[0,0]}
    return player, entities, game_map, message_log, game_state, cursor, levellist, floorentities, dstairxy, ustairxy, floor, highest_floor