# jovian_cards/src/utils/resource_loader.py

import os
import json
import pygame

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(DATA_DIR, "assets")

def load_image(image_path):
    # Check if it's a hero or gear image based on path
    if image_path.startswith("heroes/"):
        full_path = os.path.join(ASSETS_DIR, image_path)
    elif image_path.startswith("gear/"):
        full_path = os.path.join(ASSETS_DIR, image_path)
    else:
        full_path = os.path.join(ASSETS_DIR, image_path)
    
    if os.path.exists(full_path):
        return pygame.image.load(full_path)
    else:
        raise FileNotFoundError(f"Image not found: {full_path}")

def load_json(json_path):
    # Try to find the JSON in the data directory first
    full_path = os.path.join(DATA_DIR, json_path)
    
    if not os.path.exists(full_path):
        # If not found, try the provided path directly
        full_path = json_path
        
    if os.path.exists(full_path):
        with open(full_path, 'r') as file:
            return json.load(file)
    else:
        raise FileNotFoundError(f"JSON file not found: {full_path}")

def load_hero_data(hero_name):
    # Load hero from data/heroes/{hero_name}.json
    json_path = os.path.join("heroes", f"{hero_name.lower()}.json")
    return load_json(json_path)

def load_gear_data(gear_name):
    # Load gear from data/gear/{gear_name}.json
    json_path = os.path.join("gear", f"{gear_name.lower().replace(' ', '_')}.json")
    return load_json(json_path)

# Function to load heroes with dynamically generated image paths

def load_heroes():
    # Load all player heroes
    player_data = load_json(os.path.join("player", "heroes.json"))
    heroes = []
    
    for hero in player_data["heroes"]:
        hero_name = hero["name"].lower()
        hero_data = load_hero_data(hero_name)
        
        # Add player-specific data
        hero_data["level"] = hero["level"]
        hero_data["XP"] = hero["XP"]
        hero_data["rank"] = hero["rank"]
        
        # Generate image paths based on name and rank
        rank = hero_data["rank"]
        hero_data["images"] = {
            "portrait": f"{hero_name}_port_{rank}.png",
            "full_body": f"{hero_name}_{rank}.png",
            "back": f"{hero_name}_back_{rank}.png"
        }
        
        # Load equipment data
        equipment = []
        for item in hero.get("equipment", []):
            gear_data = load_gear_data(item["name"])
            gear_data["rarity"] = item["rarity"]
            equipment.append(gear_data)
        
        hero_data["equipment"] = equipment
        heroes.append(hero_data)
        
    return heroes

def create_hero_object(hero_name):
    # Create a Hero object from the hero data
    from models.hero import Hero
    
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
        if player_hero["name"].lower() == hero_name.lower():
            hero.level = player_hero["level"]
            hero.xp = player_hero["XP"]
            
            # Apply level-ups
            for _ in range(1, hero.level):
                hero.level_up()
            
            # Equip gear
            for item in player_hero.get("equipment", []):
                gear_data = load_gear_data(item["name"])
                from models.gear import Gear
                gear = Gear.load_from_json(gear_data)
                hero.equip(gear)
            
            break
    
    return hero