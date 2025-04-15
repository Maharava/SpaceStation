# jovian_cards/src/models/hero.py
from utils.constants import LEVEL_UP_XP
from utils.inventory_manager import inventory_add

class Hero:
    # Move hardcoded growth rate to class constant
    GROWTH_RATE = 0.05
    
    def __init__(self, name, description, level_1_stats, images):
        self.name = name
        self.description = description
        self.base_stats = level_1_stats  # Store original level 1 stats
        self.stats = level_1_stats.copy()  # Current stats
        self.level = 1
        self.xp = 0
        self.rank = 1  # Add rank attribute
        self.current_health = level_1_stats.get("HP", 0)  # Track current health
        self.equipment = {
            "augment": None,
            "gear": None,
            "stim": None
        }
        self.abilities = []
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
        # Increase stats by growth rate per level
        for stat in self.stats:
            base_value = self.base_stats[stat]
            level_bonus = base_value * self.GROWTH_RATE * (self.level - 1)
            self.stats[stat] = round(base_value + level_bonus)
        
        # Update current health when max HP changes
        if "HP" in self.stats:
            # If at full health before, stay at full health
            was_at_full = (self.current_health == self.stats["HP"] - round(self.base_stats["HP"] * self.GROWTH_RATE))
            if was_at_full:
                self.current_health = self.stats["HP"]
            else:
                # Otherwise add the health difference
                hp_increase = round(self.base_stats["HP"] * self.GROWTH_RATE)
                self.current_health += hp_increase

    def equip(self, item):
        # Validate slot type
        if item.slot_type not in self.equipment:
            return False
            
        slot_type = item.slot_type
        
        # Unequip any existing item in this slot
        if self.equipment[slot_type]:
            self.unequip(slot_type)
            
        # Equip the new item
        self.equipment[slot_type] = item
        
        # Apply item effects
        item.apply_effects(self)
        
        return True

    def unequip(self, slot_type):
        # Validate slot type
        if slot_type not in self.equipment:
            return None
            
        item = self.equipment[slot_type]
        if item:
            # Remove item effects
            item.remove_effects(self)
            
            # Add item back to inventory
            inventory_add(item)
            
            # Remove from equipment
            self.equipment[slot_type] = None
            return item
            
        return None

    def get_stats(self):
        return {
            "name": self.name,
            "description": self.description,
            "level": self.level,
            "xp": self.xp,  # Fix inconsistency in capitalization
            "rank": self.rank,  # Add rank to stats
            "stats": self.stats,
            "equipment": self.equipment,
            "abilities": self.abilities,
            "current_health": self.current_health  # Add current health
        }
        
    def heal(self, amount):
        """Heal the hero by the specified amount, up to max HP"""
        max_hp = self.stats.get("HP", 0)
        self.current_health = min(self.current_health + amount, max_hp)
        return amount
        
    def take_damage(self, amount):
        """Apply damage to the hero, respecting armor"""
        armor = self.stats.get("Armour", 0)
        reduced_damage = max(1, amount - armor)  # Always take at least 1 damage
        self.current_health = max(0, self.current_health - reduced_damage)
        return reduced_damage