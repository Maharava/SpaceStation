# src/utils/testing.py
import os
import json
from utils.inventory_manager import inventory_add, ensure_dict_format
from utils.resource_loader import load_json, load_item_data
from utils.currency import get_currencies, save_currencies
from models.item import Item

def while_testing():
    """Function to add test items and configurations for development"""
    print("Setting up test environment...")    
    # Ensure inventory is clear of test items (to avoid duplicates)
    clean_inventory_of_test_items()
    
    # Set testing currency values
    set_test_currencies()
    
    # Set Europa's level and XP
    set_europa_data()
    
    # Add test items to player inventory
    try:
        # Load Lact-X data as dictionary
        lact_x_data = load_item_data("lact_x", "stim")
        lact_x = ensure_dict_format(lact_x_data)
        inventory_add(lact_x)
        print("Added Lact-X to inventory")
        
        # Load Neural Interface data as dictionary
        nsb_data = load_item_data("neural_interface", "augment")
        nsb = ensure_dict_format(nsb_data)
        inventory_add(nsb)
        print("Added Neural Interface to inventory")
        
        # Equip Sweat Band to Ganymede
        equip_sweat_band_to_ganymede()
        
    except Exception as e:
        print(f"Error in while_testing: {e}")

def clean_inventory_of_test_items():
    """Remove test items to avoid duplicates"""
    try:
        inventory_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                     "data", "player", "inventory.json")
        
        if not os.path.exists(inventory_path):
            return
            
        with open(inventory_path, 'r') as f:
            inventory = json.load(f)
        
        # Remove test items by name
        test_items = ["Lact-X", "Neural Interface"]
        
        # Keep track of how many we've seen of each name
        kept_items = {}
        
        # Filter items - keep at most 2 of each test item
        filtered_items = []
        for item in inventory["items"]:
            name = item["name"]
            if name in test_items:
                kept_items[name] = kept_items.get(name, 0) + 1
                if kept_items[name] <= 2:  # Keep at most 2 of each test item
                    filtered_items.append(item)
            else:
                filtered_items.append(item)
        
        inventory["items"] = filtered_items
        
        with open(inventory_path, 'w') as f:
            json.dump(inventory, f, indent=2)
            
        print(f"Cleaned inventory: kept {', '.join([f'{n}:{c}' for n,c in kept_items.items()])}")
            
    except Exception as e:
        print(f"Error cleaning inventory: {e}")

def equip_sweat_band_to_ganymede():
    """Equip Sweat Band to Ganymede"""
    try:
        # Load heroes.json
        heroes_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                  "data", "player", "heroes.json")
        
        if not os.path.exists(heroes_path):
            print("Heroes file not found")
            return
            
        with open(heroes_path, 'r') as f:
            heroes_data = json.load(f)
        
        # Find Ganymede
        for hero in heroes_data["heroes"]:
            if hero["name"] == "Ganymede":
                # Ensure equipment is a dictionary
                if not isinstance(hero.get("equipment"), dict):
                    hero["equipment"] = {
                        "augment": None,
                        "gear": None,
                        "stim": None
                    }
                
                # Load Sweat Band data as dictionary
                try:
                    sweat_band_data = load_item_data("sweat_band", "gear")
                    sweat_band_dict = ensure_dict_format(sweat_band_data)
                    
                    hero["equipment"]["gear"] = sweat_band_dict
                    
                    # Add ability to heroes abilities list if it has one
                    if sweat_band_dict.get("ability") and sweat_band_dict["ability"] != "None":
                        if "abilities" not in hero:
                            hero["abilities"] = []
                        if sweat_band_dict["ability"] not in hero["abilities"]:
                            hero["abilities"].append(sweat_band_dict["ability"])
                            
                    print("Equipped Sweat Band to Ganymede")
                except Exception as e:
                    print(f"Error loading Sweat Band: {e}")
                break
        
        # Save updated hero data
        with open(heroes_path, 'w') as f:
            json.dump(heroes_data, f, indent=2)
            
    except Exception as e:
        print(f"Error equipping Sweat Band: {e}")

def set_test_currencies():
    """Set currencies to specific values for testing"""
    try:
        # Get current currencies
        currencies = get_currencies()
        
        # Set to testing values
        currencies["essence"] = 10000
        currencies["upgrade_tokens"]["gear"] = 6
        currencies["upgrade_tokens"]["augment"] = 6
        currencies["upgrade_tokens"]["stim"] = 6
        
        # Save updated currencies
        save_currencies(currencies)
        print("Set testing currencies: 10,000 essence, 6 of each upgrade token")
    except Exception as e:
        print(f"Error setting test currencies: {e}")

def set_europa_data():
    """Set Europa's level to 1 and XP to 15"""
    try:
        # Load heroes.json
        heroes_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                  "data", "player", "heroes.json")
        
        if not os.path.exists(heroes_path):
            print("Heroes file not found")
            return
            
        with open(heroes_path, 'r') as f:
            heroes_data = json.load(f)
        
        # Find Europa and set level/XP
        for hero in heroes_data["heroes"]:
            if hero["name"] == "Europa":
                hero["level"] = 1
                hero["XP"] = 15
                print("Set Europa's level to 1 and XP to 15")
                break
        
        # Save updated hero data
        with open(heroes_path, 'w') as f:
            json.dump(heroes_data, f, indent=2)
            
    except Exception as e:
        print(f"Error setting Europa data: {e}")