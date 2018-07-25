import libtcodpy as libtcod
import copy
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
from mortality import destroy_item, end_item
import os

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
    show_main_menu = 0
    show_load_error_message = False
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu == 0:
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
                if not os.path.isfile('savegame.dat'):
                    player, entities, game_map, message_log, game_state, cursor, levellist, floorentities, dstairxy, ustairxy, floor, highest_floor = get_game_variables(constants)
                    game_state = GameStates.PLAYERS_TURN
                    show_main_menu = 3
                else:
                    show_main_menu = 4
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state, cursor, levellist, floorentities, dstairxy, ustairxy, floor, highest_floor = load_game()
                    show_main_menu = 3
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break
        elif show_main_menu == 1 or show_main_menu == 2:
            try:
                os.remove('savegame.dat')
            except FileNotFoundError:
                filedeleted=True
            if show_main_menu == 1:
                victory_screen(con, constants['screen_width'], constants['screen_height'])
            else:
                game_over(con, constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()
            action = handle_death(key)
            new_game = action.get('new_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state, cursor, levellist, floorentities, dstairxy, ustairxy, floor, highest_floor = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN
                show_main_menu = 3
            elif exit_game:
                break
        elif show_main_menu == 4:

            areyousure(con, constants['screen_width'], constants['screen_height'])
            libtcod.console_flush()
            action = handle_sure(key)
            issure = action.get('sure')
            notsure = action.get('exit')
            if issure:
                player, entities, game_map, message_log, game_state, cursor, levellist, floorentities, dstairxy, ustairxy, floor, highest_floor = get_game_variables(
                    constants)
                game_state = GameStates.PLAYERS_TURN
                show_main_menu = 3
            if notsure:
                show_main_menu = 0

        else:
            libtcod.console_clear(con)
            show_main_menu = play_game(player, entities, game_map, message_log, game_state, con, panel, cursor, levellist, floorentities, dstairxy, ustairxy, floor, highest_floor, constants)



def play_game(player, entities, game_map, message_log, game_state, con, panel, cursor, levellist, floorentities, dstairxy, ustairxy, floor, highest_floor, constants):
    debug = False;
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    hasorb = False
    previous_game_state = game_state
    levelstodrain = math.floor(constants['top_level'] / constants['start_level'])

    fov_recompute = True
    fov_map = initialize_fov(game_map)
    targeting_item = None
    targeting_with_item = False

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
        wait = action.get('wait')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        inventory_index = action.get('inventory_index')
        spell_index = action.get('spell_index')
        drop_inventory = action.get('drop_inventory')
        stairs_up = action.get('stairs_up')
        stairs_down = action.get('stairs_down')
        show_character_screen = action.get('show_character_screen')
        exit = action.get('exit')
        targeted = action.get('targeted')
        cast_spell = action.get('cast_spell')
        fullscreen = action.get('fullscreen')

        player_turn_results = []
        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN
        if game_state == GameStates.TARGETING:
            if move:
                dx, dy = move
                cursor.move(dx, dy)
            if targeted:
                if (targeting_with_item == True):
                    targeting_results = player.inventory.use(targeting_item, entities=entities, fov_map = fov_map, target_x = cursor.x, target_y = cursor.y)
                else:
                    targeting_results = player.spellcaster.cast(targeting_spell, entities=entities, fov_map = fov_map, target_x = cursor.x, target_y = cursor.y)
                player_turn_results.extend(targeting_results)
                targeting_with_item = False
                player_turn_results.append({'targeting_over': True})
        if game_state == GameStates.PLAYERS_TURN:
            if stairs_up:
                for entity in entities:
                    if entity.stairs and entity.x == player.x and entity.y == player.y and entity.downstairs == False:
                        if floor == highest_floor:
                            levellist.append(copy.deepcopy(game_map))
                            floorentities.append(entities)
                            ustairxy.append([player.x, player.y])
                            floor = floor + 1
                            highest_floor = highest_floor + 1
                            entities = game_map.next_floor(player, cursor, message_log, constants)
                            fov_map = initialize_fov(game_map)
                            fov_recompute = True
                            libtcod.console_clear(con)
                            if ((floor % levelstodrain) == 0)and (player.level.current_level > 1):
                            #if True: #test code obviously
                                    player.level.add_xp(-1*player.level.experiance_to_previous_level)
                                    message_log.add_message(Message(
                                        'You grow weaker as you approach the Orb of Undeath. You are now level {0}'.format(
                                            player.level.current_level) + '.', libtcod.red))
                                    player.fighter.base_max_hp -= constants['hp_per_level']
                                    if (player.fighter.hp > constants['hp_per_level']):
                                        player.fighter.hp -= constants['hp_per_level']
                                    else:
                                        player.fighter.hp = 1
                                    player.spellcaster.delevel(constants['mp_per_level'])
                                    player.fighter.base_power -= constants['power_per_level']
                        else:
                            levellist[floor] = copy.deepcopy(game_map)
                            floorentities[floor] = entities
                            floor = floor+1
                            game_map = levellist[floor]
                            playerindex = entities.index(player)
                            cursorindex = entities.index(cursor)
                            entities = floorentities[floor]
                            player = entities[playerindex]
                            cursor = entities[cursorindex]
                            player.x = dstairxy[floor-1][0]
                            player.y = dstairxy[floor-1][1]
                            fov_map = initialize_fov(game_map)
                            fov_recompute = True
                            libtcod.console_clear(con)
                        break

                else:
                    message_log.add_message(Message('There are no stairs here.', libtcod.white))
            if stairs_down:
                for entity in entities:
                    if entity.stairs and entity.x == player.x and entity.y == player.y and entity.downstairs == True:
                        if floor == highest_floor:
                            levellist.append(copy.deepcopy(game_map))
                            floorentities.append(entities)
                            dstairxy.append([player.x, player.y])
                        else:
                            levellist[floor] = copy.deepcopy(game_map)
                            floorentities[floor] = entities
                        floor = floor-1
                        game_map = levellist[floor]
                        playerindex = entities.index(player)
                        cursorindex = entities.index(cursor)
                        entities = floorentities[floor]
                        player = entities[playerindex]
                        cursor = entities[cursorindex]
                        player.x = ustairxy[floor][0]
                        player.y = ustairxy[floor][1]
                        fov_map = initialize_fov(game_map)
                        fov_recompute = True
                        libtcod.console_clear(con)
                        break
                    elif entity.x == player.x and entity.y == player.y and entity.name == 'exit':
                        for item in player.inventory.items:
                            if item.name == "Orb of Undeath":
                                hasorb = True
                        if hasorb == False:
                            message_log.add_message(Message('You can not leave without the Orb! The fate of the world depends on it!.', libtcod.white))
                            break
                        else:
                            message_log.add_message(Message('You escape with the Orb of Undeath! You win!', libtcod.purple))
                            return 1
                else:
                    message_log.add_message(Message('There are no stairs here.', libtcod.white))
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
            elif wait:
                game_state = GameStates.ENEMY_TURN
            elif pickup:
                for entity in entities:
                    if sametile(player, entity):
                        if entity.render_order == RenderOrder.ITEM:
                            if entity.name == "Orb of Undeath":
                                hasorb = True
                            pickup_results = player.inventory.add_item(entity)
                            player_turn_results.extend(pickup_results)
                            break

                else:
                    message_log.add_message(Message('You pick up a large handful of air.'))
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY
        if cast_spell:
            previous_game_state = game_state
            game_state = GameStates.CAST_SPELL
        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY
        if spell_index is not None and spell_index < (player.spellcaster.spell_number):
            player_turn_results.extend(player.spellcaster.cast(spell_index +1, entities=entities, fov_map=fov_map))
        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item=player.inventory.items[inventory_index]
            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))
        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN, GameStates.CAST_SPELL):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, message_log, game_state, cursor, levellist, floorentities, dstairxy, ustairxy, floor, highest_floor)
                return 0
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            player_cast_spell = player_turn_result.get('player_cast_spell')
            item_dropped = player_turn_result.get('item_dropped')
            targeting_from_item = player_turn_result.get('targeting_item')
            targeting_from_spell = player_turn_result.get('targeting_spell')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            targeting_over = player_turn_result.get('targeting_over')
            xp = player_turn_result.get('xp')
            equip = player_turn_result.get('equip')
            itemdestroyed = player_turn_result.get('itemdestroyed')
            if message:
                message_log.add_message(message)
            if targeting_from_item:
                targeting_with_item = True
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING
                targeting_item = targeting_from_item
                cursor.x = player.x
                cursor.y = player.y
                cursor.visible = True
                message_log.add_message(Message('Press g to select target.'))
            if targeting_from_spell:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING
                targeting_spell = targeting_from_spell
                cursor.x = player.x
                cursor.y = player.y
                cursor.visible = True
                message_log.add_message(Message('Press g to select target.'))
            if dead_entity:
                if dead_entity == player:
                    if debug==False:
                        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                                   constants['screen_width'], constants['screen_height'],
                                   constants['bar_width'], constants['panel_height'], constants['panel_y'],
                                   mouse, constants['colors'], game_state)
                        return 2
                    else:
                        player.fighter.hp = player.fighter.max_hp
                        message = Message('You get better.', libtcod.red)
                else:
                    message = death(False, dead_entity)
                message_log.add_message(message)
            if itemdestroyed:
                player.inventory.drop_item(itemdestroyed)
                message = destroy_item(itemdestroyed)
                message_log.add_message(message)
                end_item(itemdestroyed)
            if item_added:
                previous_game_state = GameStates.ENEMY_TURN
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN
            if item_consumed:
                previous_game_state = GameStates.ENEMY_TURN
                game_state = GameStates.ENEMY_TURN
            if item_dropped:
                entities.append(item_dropped)
                previous_game_state = GameStates.ENEMY_TURN
                game_state = GameStates.ENEMY_TURN
            if equip:
                if (player.fighter.hp > player.fighter.max_hp):
                    player.fighter.hp = player.fighter.max_hp
                equip_results = player.equipment.toggle_equip(equip)
                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        message_log.add_message(Message('You equipped the {0}'.format(equipped.name)))
                    if dequipped:
                        message_log.add_message(Message('You removed the {0}'.format(dequipped.name)))
                game_state = GameStates.ENEMY_TURN
            if targeting_cancelled:
                message_log.add_message(Message('Targetting cancelled'))
            if targeting_cancelled or targeting_over:
                cursor.visible = False
                game_state = previous_game_state
            if player_cast_spell:
                previous_game_state = GameStates.ENEMY_TURN
                game_state = GameStates.ENEMY_TURN
            if xp:
                leveled_up = player.level.add_xp(xp)
                if (xp < 0):
                    message_log.add_message(Message('You lose {0} XP'.format(abs(xp))))
                else:
                    message_log.add_message(Message('You gain {0} XP'.format(abs(xp))))
                if leveled_up == 1:
                    message_log.add_message(Message(
                        'You grow stronger! You reached level {0}'.format(
                            player.level.current_level) + '!', libtcod.yellow))
                    player.fighter.base_max_hp += constants['hp_per_level']
                    player.fighter.hp += constants['hp_per_level']
                    player.fighter.base_power += constants['power_per_level']
                    player.spellcaster.levelup(constants['mp_per_level'])
                elif leveled_up == 2:
                    if player.level.current_level > 0:
                        message_log.add_message(Message(
                            'You grow weaker. You are now level {0}'.format(
                                player.level.current_level) + '.', libtcod.red))
                        player.fighter.base_max_hp -= constants['hp_per_level']
                        if (player.fighter.hp > constants['hp_per_level']):
                            player.fighter.hp -= constants['hp_per_level']
                        else:
                            player.fighter.hp = 1
                        player.fighter.base_power -= constants['power_per_level']
                        player.spellcaster.delevel(constants['mp_per_level'])
                    else:
                        player.level.current_level = 1
                        message_log.add_message(Message(
                            'You can grow no weaker. You stay level {0}'.format(
                                player.level.current_level) + '.', libtcod.red))

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')
                        itemdestroyed = enemy_turn_result.get('itemdestroyed')
                        if message:
                            message_log.add_message(message)
                        if itemdestroyed:
                            player.inventory.drop_item(itemdestroyed)
                            message = destroy_item(itemdestroyed)
                            message_log.add_message(message)
                            end_item(itemdestroyed)
                        if dead_entity:
                            if dead_entity == player:
                                if debug == False:
                                    render_all(con, panel, entities, player, game_map, fov_map, fov_recompute,
                                               message_log,
                                               constants['screen_width'], constants['screen_height'],
                                               constants['bar_width'], constants['panel_height'], constants['panel_y'],
                                               mouse, constants['colors'], game_state)
                                    return 2
                                else:
                                    player.fighter.hp = player.fighter.max_hp
                                    message = Message('You get better.', libtcod.red)
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
