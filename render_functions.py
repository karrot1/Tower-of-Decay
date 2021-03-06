import libtcodpy as libtcod
from enum import *


from game_states import *
from menus import *

class RenderOrder(Enum):
    CORPSE = auto()
    STAIRS = auto()
    ITEM = auto()
    ACTOR = auto()
    CURSOR = auto()
    SHOW_INVENTORY = auto()

def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)
    return get_names_at_x_y(x, y, entities, fov_map)

def get_names_at_x_y(x, y, entities, fov_map):
    names = [entity.name for entity in entities if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)
    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value)/maximum*total_width)
    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x+bar_width, y, total_width - bar_width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width/2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))

def render_pip(panel, x, y, symbol, color1, color2):
    libtcod.console_set_default_background(panel, color2)
    libtcod.console_rect(panel, x+1, y, 1, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_set_default_foreground(panel, color1)
    libtcod.console_print_ex(panel, x, y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}'.format(symbol))

def decide_color(item):
    number = 0
    if item:
        number = item.equippable.hp
    if number >75:
        return libtcod.blue
    elif number > 50:
        return libtcod.green
    elif number > 25:
        return libtcod.yellow
    elif number>0:
        return libtcod.red
    else:
        return libtcod.black

def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
               bar_width, panel_height, panel_y, mouse, colors, game_state):
    #draw the map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                if visible:
                    if wall:
                        libtcod.console_set_default_foreground(con, colors.get('light_wall'))
                        libtcod.console_put_char(con, x, y, '#', libtcod.BKGND_NONE)
                    else:
                        libtcod.console_set_default_foreground(con, colors.get('light_ground'))
                        libtcod.console_put_char(con, x, y, '.', libtcod.BKGND_NONE)
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_default_foreground(con, colors.get('dark_wall'))
                        libtcod.console_put_char(con, x, y, '#', libtcod.BKGND_NONE)
                    else:
                        libtcod.console_set_default_foreground(con, colors.get('dark_ground'))
                        libtcod.console_put_char(con, x, y, '.', libtcod.BKGND_NONE)
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        if entity.visible == True:
            draw_entity(con, entity, fov_map, game_map)
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    #prints message log
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y+=1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.red, libtcod.dark_grey)
    render_bar(panel, 1, 2, bar_width, 'MP', player.spellcaster.mp, player.spellcaster.max_mp, libtcod.blue, libtcod.dark_grey)
    render_pip(panel, screen_width-3, 1, '[', libtcod.sky, decide_color(player.equipment.armor))
    render_pip(panel, screen_width-3, 2, ']', libtcod.sky, decide_color(player.equipment.off_hand))
    render_pip(panel, screen_width-3, 3, '/', libtcod.sky, decide_color(player.equipment.main_hand))
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon level: {0}'.format(game_map.dungeon_level))
    libtcod.console_print_ex(panel, 1, 4, libtcod.BKGND_NONE, libtcod.LEFT, 'Character Level: {0}'.format(player.level.current_level))
    libtcod.console_set_default_foreground(panel, libtcod.light_grey)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map))
    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_text = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_text = 'Press the key next to an item to drop it, or Esc to cancel.\n'
        inventory_menu(con, inventory_text, player, 50, screen_width, screen_height)
    elif game_state == GameStates.CAST_SPELL:
        spellcasting_text = "Press the key next to a spell to cast it, or Esc to cancel.\n"
        spellcasting_menu(con, spellcasting_text, player, 50, screen_width, screen_height)
    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map, game_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or ((entity.stairs or entity.name == "exit" or entity.name == "Cursor") and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)