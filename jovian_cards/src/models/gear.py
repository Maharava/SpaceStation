# jovian_cards/src/models/gear.py

class Gear:
    def __init__(self, name, rarity, stats, ability, image, slot_type):
        self.name = name
        self.rarity = rarity
        self.stats = stats
        self.ability = ability
        self.image = image
        # Enhancement, Gear, or Stim
        self.slot_type = slot_type.lower()  
        
    def get_description(self):
        # Create description based on stats and ability
        stat_text = ", ".join([f"+{value} {stat}" for stat, value in self.stats.items()])
        return f"{self.name} ({self.rarity}): {stat_text}. Ability: {self.ability}"
    
    @staticmethod
    def load_from_json(data):
        # Determine slot type based on which stat it affects
        slot_type = "gear"  # Default
        if "Attack" in data["stats"]:
            slot_type = "enhancement"
        elif "HP" in data["stats"]:
            slot_type = "stim"
        
        return Gear(
            data["name"],
            data["rarity"],
            data["stats"],
            data["ability"],
            data["image"],
            slot_type
        )

    def apply_effects(self, hero):
        for stat, value in self.stats.items():
            if hasattr(hero, stat):
                setattr(hero, stat, getattr(hero, stat) + value)