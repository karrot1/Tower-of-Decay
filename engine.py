import libtcodpy as libtcod

from initialize_new_game import *
from input_handlers import *
from entity import *
from render_functions import *
from fov_functions import *
from game_states import *
from mortality import death
from game_messages import *
from data_loaders import *
from menus import *


def main():
    constants = get_constants()
    libtcod.console_set_custom_font('terminal8x12_gs_ro.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)
    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])
    player = None
    entities = []
    game_map = None
    game_state = None
    show_main_menu = True
    show_load_error_message = False
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(con, constants['screen_width'], constants['screen_height'])

            if show_load_error_message:
                message_box(con, 'Save game not found', 50, constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()
            action = handle_main_menu(key)
            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state, cursor = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN
                show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state, cursor = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break
        else:
            libtcod.console_clear(con)
            play_game(player, entities, game_map, message_log, game_state, con, panel, cursor, constants)

            show_main_menu = True


def play_game(player, entities, game_map, message_log, game_state, con, panel, cursor, constants):


    key = libtcod.Key()
    mouse = libtcod.Mouse()

    previous_game_state = game_state


    fov_recompute = True
    fov_map = initialize_fov(game_map)
    targeting_item = None

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'], constants['fov_algorithim'])

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, constants['screen_width'], constants['screen_height'],
                   constants['bar_width'], constants['panel_height'], constants['panel_y'], mouse, constants['colors'], game_state)
        libtcod.console_flush()
        clear_all(con, entities)

        action = handle_keys(key, game_state)
        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        inventory_index = action.get('inventory_index')
        drop_inventory = action.get('drop_inventory')
        exit = action.get('exit')
        targeted = action.get('targeted')
        fullscreen = action.get('fullscreen')

        player_turn_results = []
        if game_state == GameStates.TARGETING:
            if move:
                dx, dy = move
                cursor.move(dx, dy)
            if targeted:
                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map = fov_map, target_x = cursor.x, target_y = cursor.y)
                player_turn_results.extend(item_use_results)
                player_turn_results.append({'targeting_over': True})
        if game_state == GameStates.PLAYERS_TURN:
            if move:
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
            elif pickup:
                for entity in entities:
                    if sametile(player, entity):
                        if entity.render_order == RenderOrder.ITEM:
                            pickup_results = player.inventory.add_item(entity)
                            player_turn_results.extend(pickup_results)
                            break

                else:
                    message_log.add_message(Message('You pick up a large handful of air.'))
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY
        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY
        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item=player.inventory.items[inventory_index]
            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))
        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, message_log, game_state, cursor)
                return True
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        for player_turn_results in player_turn_results:
            message = player_turn_results.get('message')
            dead_entity = player_turn_results.get('dead')
            item_added = player_turn_results.get('item_added')
            item_consumed = player_turn_results.get('item_consumed')
            item_dropped = player_turn_results.get('item_dropped')
            targeting = player_turn_results.get('targeting')
            targeting_cancelled = player_turn_results.get('targeting_cancelled')
            targeting_over = player_turn_results.get('targeting_over')

            if message:
                message_log.add_message(message)
            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING
                targeting_item = targeting
                cursor.x = player.x
                cursor.y = player.y
                cursor.visible = True
                message_log.add_message(Message('Press a to select target.'))
            if dead_entity:
                if dead_entity == player:
                    message, game_state = death(True, dead_entity)
                else:
                    message = death(False, dead_entity)
                message_log.add_message(message)
            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN
            if item_consumed:
                game_state = GameStates.ENEMY_TURN
            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN
            if targeting_cancelled:
                message_log.add_message(Message('Targetting cancelled'))
            if targeting_cancelled or targeting_over:
                cursor.visible = False
                game_state = previous_game_state
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)
                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = death(True, dead_entity)
                            else:
                                message = death(True, dead_entity)
                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break
                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()
