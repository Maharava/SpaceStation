# src/utils/item_manager.py
import os
import json
from utils.inventory_manager import inventory_add, inventory_remove, get_inventory, ensure_dict_format
from utils.currency import remove_currency, check_amount
from utils.resource_loader import DATA_DIR

def load_config():
    """Load configuration values"""
    config_path = os.path.join(os.path.dirname(DATA_DIR), "config.json")
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        # Fallback default values
        return {
            "max_levels": {
                "common": 5,
                "rare": 10,
                "epic": 15,
                "prototype": 20
            },
            "essence_costs": {
                "common": 100,
                "rare": 200,
                "epic": 400,
                "prototype": 800
            },
            "level_costs": {
                "common": 50,
                "rare": 100,
                "epic": 200,
                "prototype": 400
            },
            "level_bonuses": {
                "stim": {"HP": 5},
                "gear": {"Armour": 2},
                "augment": {"Attack": 2}
            }
        }

# Load config once at module level
CONFIG = load_config()

# Maximum item level based on rarity
MAX_LEVELS = CONFIG.get("max_levels", {
    "common": 5,
    "rare": 10,
    "epic": 15,
    "prototype": 20
})

# Essence cost formulas by rarity
def get_essence_cost(rarity, level):
    base_cost = CONFIG.get("essence_costs", {}).get(rarity, 100)
    level_cost = CONFIG.get("level_costs", {}).get(rarity, 50)
    
    if level <= 1:
        return base_cost
    else:
        return base_cost + (level_cost * (level - 1))

# Token cost by rarity and level
def get_token_cost(rarity, level):
    if rarity == "common":
        return 1
    elif rarity == "rare":
        return 1 if level <= 5 else 2
    elif rarity == "epic":
        return 2 if level <= 10 else 3
    elif rarity == "prototype":
        return 3 if level <= 15 else 4
    return 1

# Level-up stat bonuses from config
LEVEL_STAT_BONUSES = CONFIG.get("level_bonuses", {
    "stim": {"HP": 5},
    "gear": {"Armour": 2},
    "augment": {"Attack": 2}
})

# Rarity progression for merging
NEXT_RARITY = {
    "common": "rare",
    "rare": "epic",
    "epic": "prototype"
}

def calculate_item_stats(item):
    """Calculate actual stats for an item based on its level"""
    base_stats = item.get("stats", {}).copy()
    level = item.get("level", 1)
    slot = item.get("slot", "gear")
    
    if level <= 1:
        return base_stats
    
    # Apply level bonuses
    result = base_stats.copy()
    
    # Check if we should use level_scaling from item or default bonuses
    level_scaling = item.get("level_scaling", {})
    
    # If no level_scaling provided, use default bonuses
    if not level_scaling and slot in LEVEL_STAT_BONUSES:
        level_scaling = LEVEL_STAT_BONUSES[slot]
    
    # Apply the bonuses
    for stat, value in level_scaling.items():
        if stat in result:
            result[stat] += value * (level - 1)
    
    return result

def can_upgrade_item(item):
    """Check if an item can be upgraded (level not maxed and player has resources)"""
    level = item.get("level", 1)
    rarity = item.get("rarity", "common")
    slot = item.get("slot", "gear")
    
    # Check if level is at max
    if level >= MAX_LEVELS.get(rarity, 5):
        return False
    
    # Calculate costs
    essence_cost = get_essence_cost(rarity, level + 1)
    token_cost = get_token_cost(rarity, level + 1)
    
    # Check if player has enough resources
    has_essence = check_amount("essence", essence_cost)
    has_tokens = check_amount("upgrade_tokens", token_cost, slot)
    
    return has_essence and has_tokens

def upgrade_item(item, is_equipped=False, hero_data=None):
    """Upgrade an item's level if possible"""
    if not can_upgrade_item(item):
        return False
    
    level = item.get("level", 1)
    rarity = item.get("rarity", "common")
    slot = item.get("slot", "gear")
    
    # Calculate costs
    essence_cost = get_essence_cost(rarity, level + 1)
    token_cost = get_token_cost(rarity, level + 1)
    
    # Remove currencies
    if not remove_currency("essence", essence_cost):
        return False
    if not remove_currency("upgrade_tokens", token_cost, slot):
        # Refund essence if token removal fails
        remove_currency("essence", -essence_cost)
        return False
    
    # Upgrade the item
    item["level"] = level + 1
    
    # If item is equipped, recalculate hero stats
    if is_equipped and hero_data:
        from utils.stats_calculator import calculate_combined_stats
        base_stats = hero_data.get('current_stats', hero_data.get('level_1_stats', {}))
        hero_data['combined_stats'] = calculate_combined_stats(base_stats, hero_data.get('equipment', {}))
    
    return True

def get_item_scrap_rewards(item):
    """Calculate rewards for scrapping an item"""
    rarity = item.get("rarity", "common")
    slot = item.get("slot", "gear")
    
    # Rarity values: common=1, rare=2, epic=3, prototype=4
    rarity_values = {"common": 1, "rare": 2, "epic": 3, "prototype": 4}
    rarity_value = rarity_values.get(rarity, 1)
    
    # Calculate essence reward: 20 × rarity
    essence = 20 * rarity_value
    
    # Calculate token rewards
    tokens = 0 if rarity == "common" else (1 if rarity in ["rare", "epic"] else 2)
    
    # Neural pattern chance
    neural_pattern_chance = {
        "common": 10,
        "rare": 20,
        "epic": 35,
        "prototype": 55
    }.get(rarity, 0)
    
    return {
        "essence": essence,
        "tokens": tokens,
        "token_type": slot,
        "neural_pattern_chance": neural_pattern_chance
    }

def scrap_item(item):
    """Scrap an item and give player rewards"""
    import random
    
    rewards = get_item_scrap_rewards(item)
    
    # Add essence
    remove_currency("essence", -rewards["essence"])  # Negative to add
    
    # Add tokens if any
    if rewards["tokens"] > 0:
        remove_currency("upgrade_tokens", -rewards["tokens"], rewards["token_type"])
    
    # Roll for neural pattern
    if random.randint(1, 100) <= rewards["neural_pattern_chance"]:
        remove_currency("neural_patterns", -1)  # Add 1
    
    # Remove item from inventory
    inventory_remove(item["id"])
    
    return rewards

def find_mergeable_items():
    """Find sets of three identical items that can be merged"""
    inventory = get_inventory()
    items_by_name_rarity = {}
    
    for item in inventory.get("items", []):
        if item.get("rarity") == "prototype":
            continue  # Prototype items can't be merged
            
        key = (item.get("name"), item.get("rarity"))
        if key not in items_by_name_rarity:
            items_by_name_rarity[key] = []
        
        items_by_name_rarity[key].append(item)
    
    mergeable_sets = {}
    for key, items in items_by_name_rarity.items():
        if len(items) >= 3:
            mergeable_sets[key] = items[:3]  # Take first 3 items
    
    return mergeable_sets

def merge_items(items):
    """Merge 3 identical items into 1 higher rarity item"""
    if not items or len(items) < 3:
        return None
    
    # All items should have same name and rarity
    name = items[0].get("name")
    rarity = items[0].get("rarity")
    
    if rarity == "prototype":
        return None  # Can't merge prototypes
    
    # Find highest level
    highest_level = max(item.get("level", 1) for item in items)
    
    # Determine next rarity
    next_rarity = NEXT_RARITY.get(rarity)
    if not next_rarity:
        return None
    
    # Create new item with next rarity
    new_item = items[0].copy()
    new_item["rarity"] = next_rarity
    new_item["level"] = highest_level
    
    # Remove the old items
    for item in items:
        inventory_remove(item["id"])
    
    # Add the new item to inventory
    inventory_add(new_item)
    
    return new_item