import libtcodpy as libtcod

def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 24: raise ValueError('cannot have a menu with more than 24 options')
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height
    window = libtcod.console_new(width, height)
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ')' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y+=1
        letter_index +=1
    x = int(screen_width/2 - width/2)
    y = int(screen_height/2 - height/2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, .7)

def inventory_menu(con, header, inventory, inventory_width, screen_width, screen_height):
    if len(inventory.items) == 0:
        options = ['Inventory is empty. Pick something up, wouldya?']
    else:
        options = []
        for item in inventory.items:
            if item.stack == False:
                options.append(item.name)
            else:
                options.append(item.name + '<' + str(item.stack_amount) + '>')
    menu(con, header, options, inventory_width, screen_width, screen_height)

def main_menu(con,screen_width, screen_height):

    libtcod.console_set_default_foreground(0, libtcod.red)
    #libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER, 'Reverse Crawl')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 11, libtcod.BKGND_NONE, libtcod.CENTER,
                             '______                              ______                                    ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 10, libtcod.BKGND_NONE, libtcod.CENTER,
                             '| ___ \\                             |  _  \\                                   ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 9, libtcod.BKGND_NONE, libtcod.CENTER,
                             '| |_/ /_____   _____ _ __ ___  ___  | | | |_   _ _ __   __ _  ___  ___  _ __  ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 8, libtcod.BKGND_NONE, libtcod.CENTER,
                             '|    // _ \\ \\ / / _ \\ \'__/ __|/ _ \\ | | | | | | | \'_ \\ / _` |/ _ \\/ _ \| \'_ \\ ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 7, libtcod.BKGND_NONE, libtcod.CENTER,
                             '| |\\ \\  __/\\ V /  __/ |  \\__ \\  __/ | |/ /| |_| | | | | (_| |  __/ (_) | | | |')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 6, libtcod.BKGND_NONE, libtcod.CENTER,
                             '\_| \\_\\___| \\_/ \\___|_|  |___/\\___| |___/  \\__,_|_| |_|\\__, |\\___|\\___/|_| |_|')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 5, libtcod.BKGND_NONE, libtcod.CENTER,
                             '                                                        __/ |                 ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             '                                                       |___/                  ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER,
                             'By Khalil Sheehan-Miles, with assistance from Justin Zinko')

    menu(con, '', ['Play a new game', 'Continue game', 'Quit'], 24, screen_width, screen_height)

def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)