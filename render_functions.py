import libtcodpy as libtcod

from enum import Enum

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

def render_all(con, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
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
        draw_entity(con, entity, fov_map)
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.console_print_ex(con, 1, screen_height - 2, libtcod.BKGND_NONE, libtcod.LEFT,
                             'HP: {0:02}/{1:02}'.format(player.fighter.hp, player.fighter.max_hp))
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)