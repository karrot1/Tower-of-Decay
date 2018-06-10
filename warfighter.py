import libtcodpy as libtcod
from game_messages import Message
class fighter:
    def __init__(self, hp, defense, power, xp=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else: bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else: bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else: bonus = 0

        return self.base_defense + bonus


    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})
        return results

    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense
        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(self.owner.name.capitalize(), target.name), libtcod.white)})
        targetequip = target.equipment
        if targetequip and target.name == "Player":
            itemdamaged = False
            if targetequip.off_hand:
                itemdamaged = True
                damitem = targetequip.off_hand
            elif targetequip.armor:
                itemdamaged = True
                damitem = targetequip.armor
            if itemdamaged:
                results.append({'message': Message('Your {0} is damaged by the blow.'.format(damitem.name),libtcod.white)})
                if (damage > 0):
                    results.extend(damitem.equippable.takedamage(self.power - damage))
                else:
                    results.extend(damitem.equippable.takedamage(self.power))
        if self.owner.equipment and self.owner.name.capitalize() == "Player":
            if self.owner.equipment.main_hand:
                itemdamage = target.fighter.defense
                if itemdamage == 0:
                    itemdamage = 1
                results.append({'message': Message('Your {0} is damaged by the blow.'.format(self.owner.equipment.main_hand.name),libtcod.white)})
                results.extend(self.owner.equipment.main_hand.equippable.takedamage(itemdamage))
        return results

    def heal(self, amount):
        originalhp = self.hp;
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        healamount = self.hp - originalhp
        return {'message': Message('You are healed for ' + str(healamount) + ' HP.')}