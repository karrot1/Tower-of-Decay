from item_functions import *
from random_utils import *

class moncaster:
    def __init__(self, spelllist):
        self.spelllist = spelllist

    def cast(self, target, entities, fov_map):
        results = []
        castspell = random_choice_from_dict(self.spelllist)
        if castspell == 'fireball':\
            results.extend(cast_fireball(entities = entities, fov_map=fov_map, damage=10, radius=2, target_x = target.x, target_y = target.y, ismon = True))
        return results