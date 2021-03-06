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

def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty. Pick something up, wouldya?']
    else:
        options = []
        for item in player.inventory.items:
            if item.stack == False:
                if item.equippable:
                    if player.equipment.main_hand == item or player.equipment.off_hand == item or player.equipment.ring == item or player.equipment.armor == item:
                        options.append('{0} (Durability: {1}) (equipped)'.format(item.name, item.equippable.hp))
                    else:
                        options.append('{0} (Durability: {1})'.format(item.name, item.equippable.hp))
                else:
                    options.append('{0}'.format(item.name))
            else:
                options.append(item.name + '<' + str(item.stack_amount) + '>')
    menu(con, header, options, inventory_width, screen_width, screen_height)


def spellcasting_menu(con, header, player, inventory_width, screen_width, screen_height):
    options = []

    if player.spellcaster.cl >=1:
        options.append("Level 1: Magic Missile")

    if player.spellcaster.cl >=2:
        options.append("Level 2: Confusion")
    if player.spellcaster.cl >=3:
        options.append("Level 3: Smite")
    if player.spellcaster.cl >=4:
        options.append("Level 4: Fireball")
    if player.spellcaster.cl >=5:
        options.append("Level 5: Disintegrate")
    menu(con, header, options, inventory_width, screen_width, screen_height)

def main_menu(con,screen_width, screen_height):

    libtcod.console_set_default_foreground(0, libtcod.green)
    #libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER, 'Reverse Crawl')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 11, libtcod.BKGND_NONE, libtcod.CENTER,
                             ' _____                               __  ______                     ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 10, libtcod.BKGND_NONE, libtcod.CENTER,
                             '|_   _|                             / _| |  _  \\                    ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 9, libtcod.BKGND_NONE, libtcod.CENTER,
                             '  | | _____      _____ _ __    ___ | |_  | | | |___  ___ __ _ _   _ ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 8, libtcod.BKGND_NONE, libtcod.CENTER,
                             '  | |/ _ \\ \\ /\\ / / _ \\ \'__|  / _ \\|  _| | | | / _ \\/ __/ _` | | | |')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 7, libtcod.BKGND_NONE, libtcod.CENTER,
                             '  | | (_) \\ V  V /  __/ |    | (_) | |   | |/ /  __/ (_| (_| | |_| |')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 6, libtcod.BKGND_NONE, libtcod.CENTER,
                             '  \\_/\\___/ \\_/\\_/ \\___|_|     \\___/|_|   |___/ \\___|\\___\\__,_|\\__, |')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 5, libtcod.BKGND_NONE, libtcod.CENTER,
                             '                                                               __/ |')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             '                                                             |___/')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER,
                             'By Khalil Sheehan-Miles, with assistance from Justin Zinko')

    menu(con, '', ['Play a new game', 'Continue game', 'Quit'], 24, screen_width, screen_height)

def areyousure(con,screen_width, screen_height):

    libtcod.console_set_default_foreground(0, libtcod.white)

    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'Are you sure? This will delete your previous save.')
    menu(con, '', ['Yes, I am sure.', 'No, take me back!'], 24, screen_width, screen_height)

def victory_screen(con,screen_width, screen_height):

    libtcod.console_set_default_foreground(0, libtcod.purple)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 9, libtcod.BKGND_NONE, libtcod.CENTER,
                             '__   __            _    _ _       _ ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 8, libtcod.BKGND_NONE, libtcod.CENTER,
                             '\\ \\ / /           | |  | (_)     | |')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 7, libtcod.BKGND_NONE, libtcod.CENTER,
                             ' \\ V /___  _   _  | |  | |_ _ __ | |')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 6, libtcod.BKGND_NONE, libtcod.CENTER,
                             '  \\ // _ \\| | | | | |/\\| | | \'_ \\| |')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 5, libtcod.BKGND_NONE, libtcod.CENTER,
                             '  | | (_) | |_| | \\  /\\  / | | | |_|')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             '  \\_/\\___/ \\__,_|  \\/  \\/|_|_| |_(_)')

    menu(con, '', ['Play a new game', 'Quit'], 24, screen_width, screen_height)

def game_over(con,screen_width, screen_height):

    libtcod.console_set_default_foreground(0, libtcod.red)

    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 9, libtcod.BKGND_NONE, libtcod.CENTER,
                             ' _____                        _____                ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 8, libtcod.BKGND_NONE, libtcod.CENTER,
                             '|  __ \\                      |  _  |               ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 7, libtcod.BKGND_NONE, libtcod.CENTER,
                             '| |  \\/ __ _ _ __ ___   ___  | | | |_   _____ _ __ ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 6, libtcod.BKGND_NONE, libtcod.CENTER,
                             '| | __ / _` | \'_ ` _ \\ / _ \\ | | | \\ \\ / / _ \\ \'__|')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 5, libtcod.BKGND_NONE, libtcod.CENTER,
                             '| |_\\ \\ (_| | | | | | |  __/ \\ \\_/ /\\ V /  __/ |   ')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             '\\____/\\__,_|_| |_| |_|\\___|  \\___/  \\_/ \\___|_| ')

    menu(con, '', ['Play a new game', 'Quit'], 24, screen_width, screen_height)

def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)

def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Character Sheet')
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Level: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'XP: {0}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'XP to Level: {0}'.format(player.level.experiance_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Attack: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Defense: {0}'.format(player.fighter.defense))

    x = (screen_width // 2) - (character_screen_width //2)
    y = (screen_height // 2)- (character_screen_height // 2)
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)