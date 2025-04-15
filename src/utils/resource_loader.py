# jovian_cards/src/utils/resource_loader.py

import os
import json
import pygame
import importlib

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(DATA_DIR, "assets")

# Cache dictionaries
_image_cache = {}
_json_cache = {}
_abilities_cache = None

def load_image(image_path):
    # Check cache first
    if (image_path in _image_cache):
        return _image_cache[image_path]
    
    # Simplified path handling
    full_path = os.path.join(ASSETS_DIR, image_path)
    
    if (os.path.exists(full_path)):
        image = pygame.image.load(full_path)
    else:
        # Try to load from gui folder for icons
        gui_path = os.path.join(ASSETS_DIR, "gui", image_path)
        if (os.path.exists(gui_path)):
            image = pygame.image.load(gui_path)
        else:
            print(f"Warning: Image not found: {full_path}")
            # Return a simple colored surface as a placeholder
            image = pygame.Surface((32, 32))
            image.fill((200, 200, 200))
    
    # Cache the result
    _image_cache[image_path] = image
    return image

def load_json(json_path):
    # Check cache first
    if (json_path in _json_cache):
        return _json_cache[json_path]
    
    # Try to find the JSON in the data directory first
    full_path = os.path.join(DATA_DIR, json_path)
    
    if (not os.path.exists(full_path)):
        # If not found, try the provided path directly
        full_path = json_path
        
    if (os.path.exists(full_path)):
        with open(full_path, 'r') as file:
            data = json.load(file)
            _json_cache[json_path] = data
            return data
    else:
        raise FileNotFoundError(f"JSON file not found: {full_path}")

def load_hero_data(hero_name):
    # Load hero from data/heroes/{hero_name}.json
    json_path = os.path.join("heroes", f"{hero_name.lower()}.json")
    return load_json(json_path)

def load_item_data(item_name, slot_type):
    # Load item from data/items/{slot_type}/{item_name}.json
    json_path = os.path.join("items", slot_type.lower(), f"{item_name.lower().replace(' ', '_')}.json")
    return load_json(json_path)

def load_heroes():
    # Load all player heroes
    player_data = load_json(os.path.join("player", "heroes.json"))
    heroes = []
    
    for hero in player_data["heroes"]:
        hero_name = hero["name"].lower()
        hero_data = load_hero_data(hero_name)
        
        # Add player-specific data
        hero_data["level"] = hero["level"]
        hero_data["XP"] = hero.get("XP", 0)
        hero_data["rank"] = hero["rank"]
        
        # Generate image paths - portrait no longer includes rank
        rank = hero_data["rank"]
        hero_data["images"] = {
            "portrait": f"{hero_name}_port.png",
            "full_body": f"{hero_name}_{rank}.png",
            "back": f"{hero_name}_back_{rank}.png"
        }
        
        # Initialize equipment dictionary
        if (isinstance(hero.get("equipment"), dict)):
            hero_data["equipment"] = hero["equipment"]
        else:
            # Convert from old list format to new dict format
            hero_data["equipment"] = {
                "augment": None,
                "gear": None,
                "stim": None
            }
            
            # Process equipment if it exists in list format
            for item in hero.get("equipment", []):
                if (isinstance(item, dict) and "name" in item):
                    # Determine slot type
                    slot_type = item.get("type", "gear")  # Default to gear
                    try:
                        item_data = load_item_data(item["name"], slot_type)
                        item_data["rarity"] = item["rarity"]
                        hero_data["equipment"][slot_type] = item_data
                    except FileNotFoundError:
                        print(f"Item data not found for: {item['name']}")
        
        # Copy abilities if present
        if ("abilities" in hero):
            hero_data["abilities"] = hero["abilities"]
        else:
            hero_data["abilities"] = []
            
        heroes.append(hero_data)
        
    return heroes

def create_hero_object(hero_name):
    # Fix circular import by using dynamic import
    Hero = getattr(importlib.import_module("models.hero"), "Hero")
    Item = getattr(importlib.import_module("models.item"), "Item")
    
    hero_data = load_hero_data(hero_name)
    hero = Hero(
        hero_data["name"],
        hero_data["description"],
        hero_data["level_1_stats"],
        hero_data["images"]
    )
    
    # Load player data to get current level and XP
    player_data = load_json(os.path.join("player", "heroes.json"))
    for player_hero in player_data["heroes"]:
        if (player_hero["name"].lower() == hero_name.lower()):
            hero.level = player_hero["level"]
            hero.xp = player_hero.get("XP", 0)
            
            # Apply level-ups
            for _ in range(1, hero.level):
                hero.level_up()
            
            # Equip gear
            for item in player_hero.get("equipment", []):
                if (isinstance(item, dict) and "name" in item):
                    slot_type = item.get("type", "gear")
                    try:
                        item_data = load_item_data(item["name"], slot_type)
                        gear = Item.load_from_json(item_data)
                        hero.equip(gear)
                    except FileNotFoundError:
                        print(f"Item data not found for: {item['name']}")
            
            break
    
    return hero

# Add caching support for abilities
def load_abilities():
    global _abilities_cache
    if (_abilities_cache is None):
        _abilities_cache = load_json(os.path.join("abilities", "abilities.json"))
    return _abilities_cache

def get_item_image_path(item_type, image_name):
    """Get the correct path for an item image with the new folder structure"""
    return f"items/{item_type}/{image_name}"