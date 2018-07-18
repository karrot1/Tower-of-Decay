class Equippable:
    def __init__(self, slot, power_bonus=0, max_hp_bonus =0, defense_bonus = 0, hp = 100):
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        self.hp = hp

    def takedamage(self, damage):
        results = []
        self.hp -= damage
        if self.hp <= 0:
            results.append({'itemdestroyed': self.owner})
        return results
