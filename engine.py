import libtcodpy as libtcod
from input_handlers import *
from entity import *

def main():
    screen_width = 80
    screen_height = 25

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@'. libcod.white)
    npc = Entity(int(screen_width / 2-5), int(screen_height / 2), '@'. libcod.yellow)
    entities = [npc, player]

    libtcod.console_set_custom_font('terminal8x12_gs_ro.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(screen_width, screen_height, 'Reverse Dungeon', False)
    con = libtcod.console_new(screen_width, screen_height)
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        libtcod.console_flush()
        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        if move:
            dx, dy = move
            player.move(dx, dy)
        if exit:
            return True
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()
