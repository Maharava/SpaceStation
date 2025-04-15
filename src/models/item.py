# jovian_cards/src/models/item.py
import uuid

class Item:
    def __init__(self, name, rarity, stats, ability, description, image, slot_type, level=1, level_scaling=None, item_id=None):
        self.name = name
        self.rarity = rarity
        self.stats = stats
        self.ability = ability
        self.description = description
        self.image = image
        self.slot_type = slot_type.lower()  # Keep as slot_type for backward compatibility
        self.level = level
        self.level_scaling = level_scaling or {}
        self.id = item_id or f"{self.name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:6]}"
        
    def get_description(self):
        # Create description based on stats and ability
        stat_text = ", ".join([f"+{value} {stat}" for stat, value in self.stats.items()])
        ability_text = f"Ability: {self.ability}" if self.ability and self.ability != "None" else ""
        return f"{self.name} ({self.rarity}): {stat_text}. {ability_text}"
    
    def get_tooltip(self):
        # Create tooltip text for display in UI with stat icons
        stats_text = []
        for stat, value in self.stats.items():
            stats_text.append(f"{stat}: +{value}")
        
        stats_str = "\n".join(stats_text)
        
        ability_text = f"\nAbility: {self.ability}" if self.ability and self.ability != "None" else ""
        description = f"\n{self.description}" if self.description and self.description != "None." else ""
        level_text = f"\nLevel: {self.level}"
        
        return f"{self.name} ({self.rarity})\n{stats_str}{ability_text}{description}{level_text}"
    
    @staticmethod
    def load_from_json(data, level=1, item_id=None):
        return Item(
            data["name"],
            data["rarity"],
            data["stats"],
            data.get("ability", "None"),
            data.get("description", "None."),
            data["image"],
            data["slot"],
            level,
            data.get("level_scaling", {}),
            item_id
        )

    def apply_effects(self, hero):
        # Apply item stats to hero
        for stat, value in self.stats.items():
            if stat in hero.stats:
                hero.stats[stat] += value
        
        # Add ability to hero if it has one
        if self.ability and self.ability != "None":
            if not hasattr(hero, "abilities"):
                hero.abilities = []
            if self.ability not in hero.abilities:
                hero.abilities.append(self.ability)
                
    def remove_effects(self, hero):
        # Remove item stats from hero
        for stat, value in self.stats.items():
            if stat in hero.stats:
                hero.stats[stat] -= value
        
        # Remove ability from hero if it has one
        if self.ability and self.ability != "None":
            if hasattr(hero, "abilities") and self.ability in hero.abilities:
                hero.abilities.remove(self.ability)
                
    def to_dict(self):
        return {
            "name": self.name,
            "slot": self.slot_type,  # Change to slot (not type)
            "rarity": self.rarity,
            "level": self.level,
            "id": self.id
        }