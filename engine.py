import libtcodpy as libtcod

from input_handlers import *
from entity import *
from render_functions import *
from GameMap import *
from fov_functions import *
from game_states import *
from warfighter import *
from mortality import death

def main():
    screen_width = 80
    screen_height = 25

    map_width = 80
    map_height = 20

    room_max_size = 10
    room_min_size = 5
    max_rooms = 15

    max_monsters_per_room = 3

    fov_algorithim = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': libtcod.darker_grey,
        'dark_ground': libtcod.darker_grey,
        'light_wall': libtcod.grey,
        'light_ground': libtcod.grey
    }
    fighter_component = fighter(hp = 30, defense=2, power=5)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, fighter=fighter_component)
    entities = [player]

    libtcod.console_set_custom_font('terminal8x12_gs_ro.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(screen_width, screen_height, 'Reverse Crawl', False)
    con = libtcod.console_new(screen_width, screen_height)

    game_map = Map(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithim)

        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        libtcod.console_flush()
        clear_all(con, entities)

        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        player_turn_results = []
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True
            game_state = GameStates.ENEMY_TURN
        if exit:
            return True
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        for player_turn_results in player_turn_results:
            message = player_turn_results.get('message')
            dead_entity = player_turn_results.get('dead')
            if message:
                print(message)
            if dead_entity:
                if dead_entity == player:
                    message, game_state = death(True, dead_entity)
                else:
                    message = death(False, dead_entity)
                print(message)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            print(message)
                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)
                            print(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break
                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()
