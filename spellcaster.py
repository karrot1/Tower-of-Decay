class spellcaster:
    def __init__(self, mp, casterl):
        self.base_max_mp = mp
        self.mp = mp
        self.base_cl = casterl

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


    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})
        return results


    def alter_mp(self, amount):
        self.mp += amount
        if self.mp > self.max_mp:
            self.mp = self.max_mp
        if self.mp < 0:
            self.mp = 0