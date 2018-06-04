import os
import shelve

def save_game(player, entities, game_map, message_log, game_state, cursor, levellist, floorentities, dstairxy, ustairxy, floor, highest_floor):
    with shelve.open('savegame', 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['cursor_index'] = entities.index(cursor)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state
        data_file['levellist'] = levellist
        data_file['floorentities'] = floorentities
        data_file['dstairxy'] = dstairxy
        data_file['ustairxy'] = ustairxy
        data_file['floor'] = floor
        data_file['highest_floor'] = highest_floor


def load_game():
    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError
    with shelve.open('savegame', 'r') as data_file:
        cursor_index = data_file['cursor_index']
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']
        levellist = data_file['levellist']
        floorentities = data_file['floorentities']
        dstairxy = data_file['dstairxy']
        ustairxy = data_file['ustairxy']
        floor = data_file['floor']
        highest_floor = data_file['highest_floor']

    player = entities[player_index]
    cursor = entities[cursor_index]


    return player, entities, game_map, message_log, game_state, cursor, levellist, floorentities, dstairxy, ustairxy, floor, highest_floor
