from item_functions import *
class spellcaster:
    def __init__(self, mp, casterl):
        self.base_max_mp = mp
        self.mp = mp
        self.base_cl = casterl
        self.spell_number = 5

    @property
    def max_mp(self):
        if self.owner and self.owner.equipment:
            bonus = 0 #add code for mana bonuses when that is added to game
        else: bonus = 0

        return self.base_max_mp + bonus

    @property
    def cl(self):
        if self.owner and self.owner.equipment:
            bonus = 0
        else: bonus = 0

        return self.base_cl + bonus

    def delevel(self, mpdown):
        self.base_cl-=1
        self.alter_mp(-mpdown)
        self.base_max_mp -=mpdown

    def levelup(self, mpdown):
        self.base_cl+=1
        self.alter_mp(mpdown)
        self.base_max_mp +=mpdown

    def alter_mp(self, amount):
        self.mp += amount
        if self.mp > self.max_mp:
            self.mp = self.max_mp
        if self.mp < 0:
            self.mp = 0

    def cast(self, index, **kwargs):
        results = []
        if self.owner.spellcaster.mp < index + 1 and not(kwargs.get('target_x') or kwargs.get('target_y')):
            results.append({'message': Message('You don\'t have enough MP to cast that.')})
            return results
        if not(kwargs.get('target_x') or kwargs.get('target_y')) and not index == 1:
            self.owner.spellcaster.alter_mp((index + 1)*-1)
        if index == 0:
            #magic missile
            if not(kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting_spell': 0})
        elif index == 1:
            results.extend(cast_smite(self.owner, damage=20, maximum_range=5, **kwargs))
            results.append({'player_cast_spell': 1})
        elif index == 2:
            if not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting_spell': 2})
            else:
                results.extend(cast_confuse(self.owner, **kwargs))
                results.append({'player_cast_spell': 1})
        elif index == 3:
            if not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting_spell': 3})
            else:
                results.extend(cast_fireball(self.owner, damage=12, radius = 3, **kwargs))
                results.append({'player_cast_spell': 1})
        else:
            if not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting_spell': 4})
        return results
