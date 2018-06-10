class Level:
    def __init__(self, current_level=1, current_xp=0, level_up_base=200, level_up_factor=150):
        self.current_level = current_level
        self.current_xp = current_xp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor

    @property
    def experiance_to_next_level(self):
        return self.level_up_base + self.current_level*self.level_up_factor

    @property
    def experiance_to_previous_level(self):
        return self.level_up_base + (self.current_level-1)*self.level_up_factor

    def add_xp(self, xp):
        self.current_xp += xp
        if self.current_xp >= self.experiance_to_next_level:
            self.current_xp -= self.experiance_to_next_level
            self.current_level += 1
            return 1
        elif self.current_xp < 0:
            self.current_xp = self.experiance_to_previous_level + self.current_xp
            self.current_level -= 1
            return 2
        else:
            return 0
