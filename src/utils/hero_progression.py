# src/utils/hero_progression.py
import os
import json
import math
from utils.resource_loader import DATA_DIR
from utils.currency import check_amount, remove_currency

def load_config():
    """Load configuration values"""
    config_path = os.path.join(os.path.dirname(DATA_DIR), "config.json")
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        # Fallback default values
        return {
            "hero_level_up": {
                "xp_per_level": 15,
                "essence_cost_multiplier": 200
            },
            "hero_rank_up": {
                "min_level": 10,
                "essence_cost_multiplier": 5000,
                "stat_boost_percentage": 25
            }
        }

def add_xp(hero_data, amount):
    """Add XP to a hero and return if they can level up"""
    config = load_config()
    current_level = hero_data.get('level', 1)
    current_xp = hero_data.get('XP', 0)
    xp_required = current_level * config["hero_level_up"]["xp_per_level"]
    
    # Check if hero already has enough XP to level up
    if current_xp >= xp_required:
        return True  # Already can level up, don't add more XP
    
    # Add XP, but cap it at the required amount
    hero_data['XP'] = min(current_xp + amount, xp_required)
    
    # Save updated XP
    save_hero_data(hero_data)
    
    # Return True if can level up
    return hero_data['XP'] >= xp_required

def can_level_up(hero_data):
    """Check if hero has enough XP and player has enough essence to level up"""
    config = load_config()
    current_level = hero_data.get('level', 1)
    current_xp = hero_data.get('XP', 0)
    xp_required = current_level * config["hero_level_up"]["xp_per_level"]
    
    essence_cost = current_level * config["hero_level_up"]["essence_cost_multiplier"]
    
    return current_xp >= xp_required and check_amount("essence", essence_cost)

def get_level_up_cost(hero_data):
    """Get essence cost for leveling up"""
    config = load_config()
    current_level = hero_data.get('level', 1)
    return current_level * config["hero_level_up"]["essence_cost_multiplier"]

def level_up(hero_data):
    """Level up a hero if possible"""
    if not can_level_up(hero_data):
        return False
    
    # Get cost and remove essence
    essence_cost = get_level_up_cost(hero_data)
    if not remove_currency("essence", essence_cost):
        return False
    
    # Increase level and reset XP
    current_level = hero_data.get('level', 1)
    hero_data['level'] = current_level + 1
    hero_data['XP'] = 0
    
    # Apply stat increases
    if 'level_1_stats' in hero_data:
        base_stats = hero_data['level_1_stats']
        current_stats = hero_data.get('current_stats', base_stats.copy())
        
        for stat, value in current_stats.items():
            if f"{stat.lower()}_level" in hero_data:
                # Apply the stat increase per level defined in hero data
                current_stats[stat] += hero_data[f"{stat.lower()}_level"]
        
        hero_data['current_stats'] = current_stats
    
    # Recalculate combined stats
    from utils.stats_calculator import calculate_combined_stats
    hero_data['combined_stats'] = calculate_combined_stats(
        hero_data.get('current_stats', hero_data.get('level_1_stats', {})),
        hero_data.get('equipment', {})
    )
    
    # Save updated hero data
    save_hero_data(hero_data)
    
    return True

def can_rank_up(hero_data):
    """Check if hero can rank up (level 10+ and player has enough essence)"""
    config = load_config()
    current_level = hero_data.get('level', 1)
    current_rank = hero_data.get('rank', 1)
    
    if current_level < config["hero_rank_up"]["min_level"]:
        return False
    
    essence_cost = current_rank * config["hero_rank_up"]["essence_cost_multiplier"]
    
    return check_amount("essence", essence_cost)

def get_rank_up_cost(hero_data):
    """Get essence cost for ranking up"""
    config = load_config()
    current_rank = hero_data.get('rank', 1)
    return current_rank * config["hero_rank_up"]["essence_cost_multiplier"]

def rank_up(hero_data):
    """Rank up a hero if possible"""
    if not can_rank_up(hero_data):
        return False
    
    config = load_config()
    
    # Get cost and remove essence
    essence_cost = get_rank_up_cost(hero_data)
    if not remove_currency("essence", essence_cost):
        return False
    
    # Increase rank
    current_rank = hero_data.get('rank', 1)
    hero_data['rank'] = current_rank + 1
    
    # Apply stat boost (25% to base stats)
    boost_percentage = config["hero_rank_up"]["stat_boost_percentage"] / 100
    
    if 'level_1_stats' in hero_data:
        base_stats = hero_data['level_1_stats'].copy()
        for stat, value in base_stats.items():
            base_stats[stat] = math.ceil(value * (1 + boost_percentage))
        
        hero_data['level_1_stats'] = base_stats
        
        # Update current stats too if they exist
        if 'current_stats' in hero_data:
            current_stats = hero_data['current_stats']
            for stat, value in current_stats.items():
                current_stats[stat] = math.ceil(value * (1 + boost_percentage))
            
            hero_data['current_stats'] = current_stats
    
    # Recalculate combined stats
    from utils.stats_calculator import calculate_combined_stats
    hero_data['combined_stats'] = calculate_combined_stats(
        hero_data.get('current_stats', hero_data.get('level_1_stats', {})),
        hero_data.get('equipment', {})
    )
    
    # Save updated hero data
    save_hero_data(hero_data)
    
    return True

def get_xp_required(hero_data):
    """Get XP required to level up"""
    config = load_config()
    current_level = hero_data.get('level', 1)
    return current_level * config["hero_level_up"]["xp_per_level"]

def save_hero_data(hero_data):
    """Save hero data to heroes.json"""
    heroes_path = os.path.join(DATA_DIR, "player", "heroes.json")
    
    try:
        with open(heroes_path, 'r') as f:
            heroes_data = json.load(f)
            
        for i, hero in enumerate(heroes_data["heroes"]):
            if hero["name"] == hero_data["name"]:
                # Update relevant fields
                for key in ['level', 'rank', 'XP', 'level_1_stats', 'current_stats', 'combined_stats']:
                    if key in hero_data:
                        heroes_data["heroes"][i][key] = hero_data[key]
                break
                    
        with open(heroes_path, 'w') as f:
            json.dump(heroes_data, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Error saving hero data: {e}")
        return False