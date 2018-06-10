from random import randint
import libtcodpy as libtcod
from stairs import *
from tile import *
from rectangle import *
from entity import *
from warfighter import *
from ai import *
from item import *
from item_functions import *
from random_utils import *
from equipment import EquipmentSlots
from Equippable import Equippable

class Map:
    def __init__(self, width, height, dungeon_level = 1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]


        return tiles

    def create_room(self, room):
        #goes through tiles in room and sets them to be floor
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            #generates random rooms
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            #generates random on map location
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)
            new_room = Rect(x, y, w, h)
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                #if it did not break, room is valid
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()
                center_of_last_room_x = new_x
                center_of_last_room_y = new_y
                if num_rooms == 0:
                    #player starts in first room cuz we don't have stairs or entrances just yet
                    player.x = new_x
                    player.y = new_y
                else:
                    #if it isn't the first room it needs a tunnel to connect it to a older room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    if randint(0, 1) == 1:
                        #first horizontal, then vertical
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        #first vertical, then horizontal
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                #add room to list
                self.place_entities(new_room, entities)
                rooms.append(new_room)
                num_rooms += 1
        stairs_component = Stairs(self.dungeon_level + 1)
        up_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '<', libtcod.white, 'stairs up', render_order = RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(up_stairs)
        if (self.dungeon_level > 1):
            downstairs_component = Stairs(self.dungeon_level -1)
            down_stairs = Entity(player.x, player.y, '>', libtcod.white, 'stairs down',
                               render_order=RenderOrder.STAIRS, stairs=downstairs_component, downstairs=True)
            entities.append(down_stairs)
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def place_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level([[2, 1],[3,4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)
        #gets a random number of monsters
        min_monsters = 1
        if (room.x1-room.x2 <6 ) and (room.y1 - room.y2 < 6):
            min_monsters = 0
        number_of_monsters = randint(min_monsters, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)
        monster_chances = {
            'skeleton': 80,
            'lich': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
        }
        item_chances = {
            'healing_potion': 35,
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level),
            'sword': from_dungeon_level([[5, 4]], self.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], self.dungeon_level),
            'health_ring': from_dungeon_level([[5, 1]], self.dungeon_level),
            'armor': from_dungeon_level([[5, 4]], self.dungeon_level)
        }
        item_chance = {'healing_potion': 70, 'fireball_scroll': 10, 'confusion_scroll': 10, 'smite_scroll': 10}
        for i in range(number_of_monsters):
            #chose random location to place them
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 + 1, room.y2 -1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)
                if monster_choice == 'skeleton':
                    fighter_component = fighter(hp = 20, defense = 0, power = 4, xp = 1)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 's', libtcod.white, 'Skeleton', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai= ai_component)
                else:
                    fighter_component = fighter(hp=30, defense=2, power=8, xp =5)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'L', libtcod.purple, 'Lich', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai= ai_component)
                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 + 1, room.y2 -1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chance)
                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=5)
                    item = Entity(x, y, '!', libtcod.red, 'Major Healing Potion', render_order = RenderOrder.ITEM, item=item_component, stack=True)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, damage=12, radius = 3)
                    item = Entity(x, y, '?', libtcod.lightest_yellow, 'Scroll of Fireball', render_order=RenderOrder.ITEM,
                      item=item_component, stack=True)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True)
                    item = Entity(x, y, '?', libtcod.lightest_yellow, 'Scroll of Confusion', render_order=RenderOrder.ITEM,
                              item=item_component, stack=True)
                elif item_choice == 'sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity(x, y, '/', libtcod.sky, 'Sword', equippable=equippable_component)
                elif item_choice == 'shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus = 1)
                    item = Entity(x, y, '[', libtcod.grey, 'Shield', equippable=equippable_component)
                elif item_choice == 'health_ring':
                    equippable_component = Equippable(EquipmentSlots.RING, max_hp_bonus=10)
                    item = Entity(x, y, 'o', libtcod.sky, 'Ring of Health', equippable=equippable_component)
                elif item_choice == 'armor':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, defense_bonus = 2)
                    item = Entity(x, y, '[', libtcod.darker_gray, 'Chain Mail', equippable=equippable_component)
                else:
                    item_component = Item(use_function=cast_smite, damage=20, maximum_range=5)
                    item = Entity(x, y, '?', libtcod.lightest_yellow, 'Scroll of Smite', render_order=RenderOrder.ITEM,
                                  item=item_component, stack=True)

                entities.append(item)

    def next_floor(self, player, cursor, message_log, constants):
        self.dungeon_level += 1
        entities = [player, cursor]
        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)
        #player.fighter.heal(player.fighter.max_hp//2)
        #message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))
        return entities