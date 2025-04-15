# src/utils/inventory_manager.py
import os
import json
import pygame
from utils.resource_loader import load_json, DATA_DIR

INVENTORY_PATH = os.path.join(DATA_DIR, "player", "inventory.json")

def get_inventory():
    """Load player's inventory from JSON file"""
    try:
        return load_json("player/inventory.json")
    except FileNotFoundError:
        # Create empty inventory if file doesn't exist
        inventory = {"items": []}
        save_inventory(inventory)
        return inventory

def save_inventory(inventory):
    """Save player's inventory to JSON file"""
    os.makedirs(os.path.join(DATA_DIR, "player"), exist_ok=True)
    with open(INVENTORY_PATH, 'w') as file:
        json.dump(inventory, file, indent=2)

def generate_item_id(item_name):
    """Generate unique ID for an item"""
    inventory = get_inventory()
    prefix = ''.join([word[0].lower() for word in item_name.split()])
    
    existing_ids = [item.get("id", "") for item in inventory["items"] 
                   if item.get("id", "").startswith(prefix)]
    
    existing_numbers = []
    for id_str in existing_ids:
        num_str = id_str[len(prefix):]
        if num_str.isdigit():
            existing_numbers.append(int(num_str))
    
    next_num = max(existing_numbers, default=0) + 1
    return f"{prefix}{next_num:03d}"

def ensure_dict_format(item):
    """Ensure item is in dictionary format"""
    if item is None:
        return None
        
    if hasattr(item, 'name'):  # Item object
        return {
            "name": item.name,
            "rarity": item.rarity,
            "image": item.image,
            "stats": item.stats,
            "ability": getattr(item, 'ability', "None"),
            "description": getattr(item, 'description', ""),
            "slot": item.slot_type,
            "level": getattr(item, 'level', 1),
            "id": getattr(item, 'id', generate_item_id(item.name))
        }
    elif isinstance(item, dict):
        item_copy = item.copy()
        
        if "type" in item_copy and "slot" not in item_copy:
            item_copy["slot"] = item_copy["type"]
        if "type" in item_copy:
            del item_copy["type"]
            
        if "ability" not in item_copy:
            item_copy["ability"] = "None"
        if "description" not in item_copy:
            item_copy["description"] = ""
        if "level" not in item_copy:
            item_copy["level"] = 1
        if "id" not in item_copy:
            item_copy["id"] = generate_item_id(item_copy["name"])
            
        return item_copy
    
    print(f"Warning: Unable to convert to dictionary: {type(item)}")
    return None

def inventory_add(item):
    """Add item to inventory"""
    inventory = get_inventory()
    
    item = ensure_dict_format(item)
    if not item:
        return False
    
    if "id" not in item:
        item["id"] = generate_item_id(item["name"])
    
    inventory["items"].append(item)
    save_inventory(inventory)
    return True

def inventory_remove(item_id):
    """Remove item from inventory by ID"""
    inventory = get_inventory()
    inventory["items"] = [item for item in inventory["items"] if item.get("id") != item_id]
    save_inventory(inventory)

def get_items_by_slot(slot_type):
    """Get all inventory items that fit in the given slot"""
    inventory = get_inventory()
    matching_items = []
    
    for item in inventory["items"]:
        if item.get("slot", "").lower() == slot_type.lower():
            full_item = ensure_dict_format(item)
            if full_item:
                matching_items.append(full_item)
            
            if len(matching_items) >= 20:  # Limit to prevent display issues
                break
                
    return matching_items

def get_tooltip_for_item(item):
    """Generate tooltip text for item dictionary"""
    item = ensure_dict_format(item)
    if not item:
        return "No item information available"
    
    stats_text = []
    for stat, value in item.get("stats", {}).items():
        stats_text.append(f"{stat}: +{value}")
    
    stats_str = "\n".join(stats_text)
    ability_text = f"\nAbility: {item.get('ability')}" if item.get("ability") and item["ability"] != "None" else ""
    description = f"\n{item.get('description', '')}" if item.get("description") and item["description"] != "None." else ""
    level_text = f"\nLevel: {item.get('level', 1)}"
    
    return f"{item['name']} ({item['rarity']})\n{stats_str}{ability_text}{description}{level_text}"

def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Handle close button
        if self.close_button.collidepoint(event.pos):
            return False
        
        # Handle equipment slot clicks
        for slot_type, rect in self.equipment_slots.items():
            if rect.collidepoint(event.pos):
                if event.button == 1:  # Left click
                    self.selected_slot = slot_type
                    self.load_inventory_items()
                    # Update equipment display and reset tooltips
                    self.update_equipment_display()
                    self.active_tooltip = False
                elif event.button == 3:  # Right click - unequip
                    if self.hero['equipment'].get(slot_type):
                        # Get the item and ensure it's a dictionary
                        item = ensure_dict_format(self.hero['equipment'][slot_type])
                        
                        # Add to inventory
                        inventory_add(item)
                        
                        # Remove from hero
                        self.hero['equipment'][slot_type] = None
                        
                        # Update heroes.json
                        self.save_hero_data()
                        
                        # Force reset tooltip
                        self.active_tooltip = False
                        
                        # Update equipment display THEN reload inventory
                        self.update_equipment_display(slot_type)
                        self.load_inventory_items()
                        self.update_equipment_display() # Force update equipment display
                    return True