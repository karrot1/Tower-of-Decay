from random import randint
import libtcodpy as libtcod

from tile import *
from rectangle import *
from entity import *
from warfighter import *
from ai import *

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
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

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room):
        rooms = []
        num_rooms = 0
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
                self.place_entities(new_room, entities, max_monsters_per_room)
                rooms.append(new_room)
                num_rooms += 1

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def place_entities(self, room, entities, max_monsters_per_room):
        #gets a random number of monsters
        min_monsters = 1
        if room.x1-room.x2 < 6 or room.y1 - room.y2 < 6:
            min_monsters = 0
        number_of_monsters = randint(min_monsters, max_monsters_per_room)

        for i in range(number_of_monsters):
            #chose random location to place them
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 + 1, room.y2 -1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    fighter_component = fighter(hp = 10, defense = 0, power = 3)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 's', libtcod.white, 'Skeleton', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai= ai_component)
                else:
                    fighter_component = fighter(hp=20, defense=2, power=4)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'L', libtcod.purple, 'Lich', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai= ai_component)
                entities.append(monster)

