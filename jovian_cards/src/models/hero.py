# jovian_cards/src/models/hero.py

# Fix import
from utils.constants import LEVEL_UP_XP

class Hero:
    def __init__(self, name, description, level_1_stats, images):
        self.name = name
        self.description = description
        self.base_stats = level_1_stats  # Store original level 1 stats
        self.stats = level_1_stats.copy()  # Current stats
        self.level = 1
        self.xp = 0
        self.equipment = {
            "enhancement": None,
            "gear": None,
            "stim": None
        }
        self.images = images

    def add_xp(self, amount):
        self.xp += amount
        # Check if level up is possible
        next_level = self.level + 1
        if next_level in LEVEL_UP_XP and self.xp >= LEVEL_UP_XP[next_level]:
            self.level_up()
            return True
        return False

    def level_up(self):
        self.level += 1
        # Increase stats by 5% per level
        growth_rate = 0.05
        for stat in self.stats:
            base_value = self.base_stats[stat]
            level_bonus = base_value * growth_rate * (self.level - 1)
            self.stats[stat] = round(base_value + level_bonus)

    def equip(self, gear):
        # Unequip any existing gear in this slot
        if self.equipment[gear.slot_type]:
            self.unequip(gear.slot_type)
            
        # Equip the new gear
        self.equipment[gear.slot_type] = gear
        
        # Apply gear stats
        for stat, value in gear.stats.items():
            if stat in self.stats:
                self.stats[stat] += value

    def unequip(self, slot_type):
        gear = self.equipment[slot_type]
        if gear:
            # Remove gear stats
            for stat, value in gear.stats.items():
                if stat in self.stats:
                    self.stats[stat] -= value
            self.equipment[slot_type] = None

    def get_stats(self):
        return {
            "name": self.name,
            "description": self.description,
            "level": self.level,
            "XP": self.xp,
            "stats": self.stats,
            "equipment": self.equipment
        }