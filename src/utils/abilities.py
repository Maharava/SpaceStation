# src/utils/abilities.py
import json
import os
from utils.resource_loader import load_json, DATA_DIR, load_abilities

def load_abilities():
    """Load all ability definitions from JSON"""
    try:
        return load_json("heroes/abilities.json")
    except FileNotFoundError:
        return {}

def get_ability_description(ability_name):
    """Returns description for an ability"""
    try:
        abilities = load_json("heroes/abilities.json")
        if ability_name in abilities:
            return abilities[ability_name]["description"]
    except:
        pass
    return "No description available"

def apply_passive_healing(hero, amount):
    """Apply healing to hero."""
    hero.current_health = min(hero.current_health + amount, hero.max_health)
    return amount

def apply_extra_attack(hero, params, game_state=None):
    """Placeholder for extra attack abilities"""
    if game_state and game_state.current_phase == params.get("trigger", "turn_end"):
        print(f"{hero.name} attacks {params.get('attacks', 1)} extra time(s)!")
        # Actual attack logic would be here

def apply_damage_reduction(hero, params, game_state=None):
    """Placeholder for damage reduction abilities"""
    # This would be called when calculating damage
    print(f"{hero.name} has {params.get('reduction_percent', 0.1) * 100}% "
          f"{params.get('damage_type', 'all')} damage reduction")

# Dictionary mapping effect types to placeholder functions
ABILITY_FUNCTIONS = {
    "passive_healing": apply_passive_healing,
    "extra_attack": apply_extra_attack,
    "damage_reduction": apply_damage_reduction,
}

def apply_ability(hero, ability_name, game_state=None):
    """Apply an ability's effects to a hero during gameplay"""
    abilities = load_abilities()
    
    if ability_name in abilities:
        ability_data = abilities[ability_name]
        effect_type = ability_data["effect"]
        
        if effect_type in ABILITY_FUNCTIONS:
            # Call the appropriate function with the ability parameters
            ABILITY_FUNCTIONS[effect_type](hero, ability_data["params"], game_state)
            return True
    
    return False

# Simple mapping of ability names to placeholder functions
def placeholder_ability(*args, **kwargs):
    """Placeholder function for abilities that aren't implemented yet"""
    print(f"Ability triggered with args: {args}, kwargs: {kwargs}")
    return True

# Dictionary mapping ability names to functions
ABILITY_MAP = {
    "Enhance Production": placeholder_ability,
    "Reflex Tuning": placeholder_ability
}

def get_ability_function(ability_name):
    """Returns the function for a given ability name"""
    return ABILITY_MAP.get(ability_name, placeholder_ability)