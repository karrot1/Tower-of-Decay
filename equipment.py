from equipment_slots import EquipmentSlots

class Equipment:
    def __init__(self, main_hand=None, off_hand = None, ring = None, armor = None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.ring = ring
        self.armor = armor

    @property
    def max_hp_bonus(self):
        bonus = 0
        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus
        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus
        if self.ring and self.ring.equippable:
            bonus += self.ring.equippable.max_hp_bonus
        if self.armor and self.armor.equippable:
            bonus += self.armor.equippable.max_hp_bonus
        return bonus

    @property
    def power_bonus(self):
        bonus = 0
        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus
        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus
        if self.ring and self.ring.equippable:
            bonus += self.ring.equippable.power_bonus
        if self.armor and self.armor.equippable:
            bonus += self.armor.equippable.power_bonus
        return bonus

    @property
    def defense_bonus(self):
        bonus = 0
        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus
        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus
        if self.ring and self.ring.equippable:
            bonus += self.ring.equippable.defense_bonus
        if self.armor and self.armor.equippable:
            bonus += self.armor.equippable.defense_bonus
        return bonus

    def toggle_equip(self, item):
        results = []
        slot = item.equippable.slot
        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == item:
                self.main_hand = None
                results.append({'dequipped': item})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})
                self.main_hand = item
                results.append({'equipped': item})
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == item:
                self.off_hand = None
                results.append({'dequipped': item})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})
                self.off_hand= item
                results.append({'equipped': item})
        elif slot == EquipmentSlots.RING:
            if self.ring == item:
                self.ring = None
                results.append({'dequipped': item})
            else:
                if self.ring:
                    results.append({'dequipped': self.ring})
                self.ring= item
                results.append({'equipped': item})
        elif slot == EquipmentSlots.ARMOR:
            if self.armor == item:
                self.armor = None
                results.append({'dequipped': item})
            else:
                if self.armor:
                    results.append({'dequipped': self.armor})
                self.armor= item
                results.append({'equipped': item})
        return results