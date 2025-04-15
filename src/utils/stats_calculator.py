import copy
from utils.item_manager import calculate_item_stats

def calculate_combined_stats(base_stats, equipment, hero_data=None):
    """Calculate hero stats based on base stats, level, and equipped items"""
    # Use current_stats (which includes level bonuses) if available, 
    # otherwise start with base_stats
    if hero_data and 'current_stats' in hero_data:
        result = copy.deepcopy(hero_data['current_stats'])
    else:
        # Calculate level-based stats if hero_data is provided
        result = copy.deepcopy(base_stats)
        if hero_data:
            level = hero_data.get('level', 1)
            if level > 1:
                # Apply per-level stat increases
                for stat in result:
                    level_stat = f"{stat.lower()}_level"
                    if level_stat in hero_data:
                        result[stat] += hero_data[level_stat] * (level - 1)
    
    # Apply equipment bonuses
    if not equipment:
        return result
    
    for slot, item in equipment.items():
        if not item:
            continue
        
        # Calculate actual item stats based on level
        actual_stats = calculate_item_stats(item)
        
        # Apply stats to result
        for stat, value in actual_stats.items():
            if stat in result:
                result[stat] += value
            else:
                result[stat] = value
    
    return result