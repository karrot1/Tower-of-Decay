import libtcodpy as libtcod

from input_handlers import *
from entity import *
from render_functions import *
from GameMap import *
from fov_functions import *
from game_states import *
from warfighter import *
from mortality import death
from game_messages import *
from inventory import *

def main():
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
    max_items_per_room = 50
    fov_algorithim = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': libtcod.darker_grey,
        'dark_ground': libtcod.darker_grey,
        'light_wall': libtcod.grey,
        'light_ground': libtcod.grey
    }
    inventory_component = Inventory(20)
    fighter_component = fighter(hp = 30, defense=2, power=5)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component,
                    inventory=inventory_component)
    cursor = Entity(0, 0, 'X', libtcod.yellow, 'Cursor', blocks=False, render_order=RenderOrder.CURSOR, visible=False)
    entities = [player, cursor]

    libtcod.console_set_custom_font('terminal8x12_gs_ro.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(screen_width, screen_height, 'Reverse Crawl', False)
    con = libtcod.console_new(screen_width, screen_height)
    panel = libtcod.console_new(screen_width, panel_height)
    game_map = Map(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    targeting_item = None

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithim)

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
                   bar_width, panel_height, panel_y, mouse, colors, game_state)
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
