import libtcodpy as libtcod
from game_states import *

def handle_movement_keys(key):
    key_char = chr(key.c)
    # movement
    if key.vk == libtcod.KEY_UP or key_char == 'w' or key.vk == libtcod.KEY_KP8:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'x' or key_char == libtcod.KEY_KP2:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'a' or key_char == libtcod.KEY_KP:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'd' or key_char == libtcod.KEY_KP:
        return {'move': (1, 0)}
    elif key_char == 'q' or key_char == libtcod.KEY_KP7:
        return {'move': (-1, -1)}
    elif key_char == 'e' or key_char == libtcod.KEY_KP9:
        return {'move': (1, -1)}
    elif key_char == 'z' or key_char == libtcod.KEY_KP1:
        return {'move': (-1, 1)}
    elif key_char == 'c' or key_char == libtcod.KEY_KP3:
        return {'move': (1, 1)}
    elif key_char == 's' or key_char == libtcod.KEY_KP5:
        return {'wait': True}
    return {'move': (0, 0)}

def handle_player_turn_keys(key):
    key_char = chr(key.c)
    movement = handle_movement_keys(key)
    if (movement != {'move': (0, 0)}):
        return movement
    if key_char == 'g':
        return {'pickup': True}
    elif key_char == 'i':
        return {'show_inventory': True}
    elif key_char == 'd':
        return {'drop_inventory': True}
    elif key_char == ',':
        return {'stairs_up': True}
    elif key_char == '.':
        return {'stairs_down': True}
    elif key_char == 'c':
        return{'show_character_screen': True}
    elif key_char == 'f':
        return{'cast_spell': True}
    result = quitscreen(key)
    return result

def quitscreen(key):
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit
        return {'exit': True}
    return{}

def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        result = handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        result = handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        result = handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        result = handle_inventory_keys(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        result = handle_character_screen(key)
    elif game_state == GameStates.CAST_SPELL:
        result = handle_spellcasting_keys(key)
    else:
        result = {}
    return result

def handle_main_menu(key):
    key_char = chr(key.c)
    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c':
        return {'exit': True}
    return quitscreen(key)

def handle_death(key):
    key_char = chr(key.c)
    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'exit': True}
    return quitscreen(key)

def handle_inventory_keys(key):
    index = key.c - ord('a')
    if index>= 0:
        return {'inventory_index': index}
    result = quitscreen(key)
    return result


def handle_spellcasting_keys(key):
    index = key.c - ord('a')
    if index>= 0:
        return {'spell_index': index}
    result = quitscreen(key)
    return result

def handle_player_dead_keys(key):
    key_char = chr(key.c)
    if key_char == 'i':
        return{'show_inventory': True}
    result = quitscreen(key)
    return result

def handle_targeting_keys(key):
    movement = handle_movement_keys(key)
    if (movement != {'move': (0, 0)}):
        return movement
    key_char = chr(key.c)
    if key_char == 'g':
        return{'targeted': True}
    result = quitscreen(key)
    return result

def handle_character_screen(key):
    return quitscreen(key)