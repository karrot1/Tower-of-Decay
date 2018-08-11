from item_functions import *
from random_utils import *

class moncaster:
    def __init__(self, spelllist, power):
        self.spelllist = spelllist
        self.power = power

    def cast(self, target, entities, fov_map, game_map):
        results = []
        castspell = random_choice_from_dict(self.spelllist)
        if castspell == 'fireball':
            results.extend(cast_fireball(entities = entities, fov_map=fov_map, damage=self.power+4, radius=2, target_x = target.x, target_y = target.y, ismon = True))
        elif castspell == 'magic_missile':
            results.extend(cast_magic_missile(entities = entities, damage=self.power, target_x = target.x, target_y = target.y, ismon = True))
        elif castspell == 'animate_dead':
            results.extend(cast_animate_dead(self.owner, entities = entities, number=self.power, player=target))
        elif castspell == 'summon_demon':
            results.extend(summon_demons(self.owner, entities = entities, number=self.power-2, gamemap=game_map))
        return results