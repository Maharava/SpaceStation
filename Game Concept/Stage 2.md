Stage Two: Equipment System
Equipment Collection UI

* Inventory
 - The player inventory is stored in data/player/inventory.json, which contains the names of unequipped collected gear, its rarity and level. ALl gear now has a level mechanic.
 - A function to add an item to the players inventory needs to be created.
 - Three new data folders, data/items, data/items/stim and data/items/augment need to be made for the other two item classes. Data/gear will be moved into data/items
* Item inventory screen
 - When the player clicks on an equipment slot on the character screen, the stats at the bottom are moved up to replace the hero description, and the equipment slots are moved up to the top of the new inventory window. Tiles for the players collected gear *that fit that inventory window* are shown. Clicking on one will equip it into the slot, unequipping whatever may be there. Mousing over these item tiles provides tooltips.
 - Item icons should be small but readable, allowing five in a row from the left side of the screen up to the egde of the character image. A scrolling system is implemented should there not be enough space for all the rows of items.
 - The scrolling system will have both a scrollbar and accept scrollwheel
 - A small close icon will appear in the top left of this area to let the player return to the usual layout for the character details screen.
 - Items do not stack. Duplicate items will be shown as two separate tiles, to accommodate the implementation of levelling and merging
 - Item levels will appear as a small black number inside a white circle in the bottom right of the tile
* Equipment rarity
 - All equipment tiles now must have a coloured border that matches their rarity:
  - Common, Grey
  - Rare, Blue
  - Epic, Purple
  - Prototype, Black
* Equipping Mechanics
 - Right clicking a piece of unequipped equipment first checks if there's something equipped in that slot. If there is, it is removed from the hero's data and their stats are reduced/listed abilities corrected for the removal. That piece of gear is then stored in the inventory. The piece of right clicked gear is then equipped, its stat boosts added to the player and its special ability (if any) added to the characters listed abilities.
 - Players may right click an equipment slot to unequip the item there.
 - Equipment slots always show the correctly equipped item 
 - data/player/heroes.json is updated with the equipped items of the heroes in the correct slots, and data/player/inventory.json is updated whenever gear is removed from or added to the inventory.
 - If there is nothing in a slot the player is right clicking, nothing happens.
 - There should be no occassion where the player can try to equip an itme to the wrong slot, as the only items that should be shown should fit the slot the player originally clicked on.
 - Items know which slot to go to due to their .jsons, which will need an entry called "slot" that matches "augment","gear" or "stim"
* Hero listed abilities
 - As some gear grant special abilities, heroes need to track what abilities they have. The player/heroes data json will be used for this.
 - A map or dictionary will be created, mapping ability names from gear to function/script calls. Placeholder code will be created for now. This will be stored in utils/abilities/, along with the (eventual) ability scripts
 - There are currently no plans for how the actual scripts/abilities/code will be implemented during runs
 - There is no way to see what abilities a hero has apart from mousing over the equipped items.
 - The heroes.json will store the abilities as the ability names, allowing easy matching to functions with the new mapping scripts.
* Equipment Tooltips Enhancement
 - Tooltip font size is to be reduced
 - Instead of tooltips saying 'Attack +5', the word 'Attack' will be replaced with attack.png in data/assets/gui - likewise for defence and health. Only if these images can't be found will the word ('Attack') be written
 - If an item has an ability, it will have the ability name and description show in the tooltip
 - A central json, data/heroes/abilitis.json, will be created, which will contain the ability names, images and descriptions. 

 To test this, two new items will be added:
 Stim - Lact-X, +15 HP, Rare, Ability: "Enhance Production. Each turn, heal 2% of your HP."
 Augment - Nervous System Boost, +10 attack, Rare, Ability: "Reflex Tuning. At the end of your turn, attack once more."

 These will use the new inventory_add function to be added at the start of the game.
 A new function called while_testing needs to be created somewhere it can be called at game start (but after everything is initialized) where code needed for development and testing is stored. The addition on the test items and the equipping of sweat band to Ganymede need to be placed exclusively in this function.

Completion criteria:
 - New folder structure (at minimum other folders as necessary):
  - data/heroes/abilities.json
  - data/items/gear/
  - data/items/augment/
  - data/items/stim/
  - data/player/inventory.json
 - Two new items implemented
 - Item ability data implemented in the relevant item jsons, and the ability lists added to the heroes.json. Inventory json added to data/player
 - Placeholder ability code added to the most relevant folder, and a utils/ script created mapping ability names to the relevant (placeholder) code
 - Both new items added to players inventory
 - Player clicking an equipment slot moves the stats window up to replace the hero descriptopn and creates an inventory window, showing inventory items. Equipment slots move to the top of this new window. Close button returning to the stats and description window in the top left. Only inventory items that match the equipment slot clicked are shown.
 - Clicking another equipment slot with the inventory open will clear it of items and instead show the items that fit that slot
 - Right clicking an equipment slot with an item in it while the inventory window is open unequips it, adding the item back to the players inventory. The inventory window updates with the new item.
 - Right clicking an item in the inventory window attempts to equip it by first checking if the slot is full. If the slot is full, the equipped item is unequipped (as above). When the slot is empty/if it's already empty, the right clicked item is equipped and remvoed from the inventory. The UI updates immediately.
 - Tooltips for item names, description and abilities for all inventory items.
 - Hero stats and abilities update as items are equipped/unequipped
 - Clicking the close icon removes the inventory screen and moves the stats window back to its initial spot, moves the equipment slots back to where they belong, and re-shows the description window.
 - Ganymede's equipped item is to be removed from the .json
 - while-testing is created, and called after the game is initialized. It adds the two new items to the players inventory, and equips Ganymede with the sweat band via the equip function.

Example structures (that should be changed as needed to fit the code and goals):
Inventory Structure:
{
  "items": [
    {
      "name": "Sweat Band",
      "type": "gear",
      "rarity": "common",
      "level": 1,
      "id": "sw001"
    },
    {
      "name": "Lact-X",
      "type": "stim",
      "rarity": "rare",
      "level": 1,
      "id": "lx001"
    },
    {
      "name": "Lact-X",
      "type": "stim",
      "rarity": "rare",
      "level": 2,
      "id": "lx002"
    }
  ]
}
Updated Item Structure:
{
  "name": "Sweat Band",
  "slot": "gear",
  "rarity": "common",
  "stats": {
    "Armour": 5
  },
  "ability": "None",
  "description": "None.",
  "image": "sweat_band.png",
  "level_scaling": {
    "Armour": 2
  }
}
Abilities structure:
{
  "Enhance Production": {
    "description": "Each turn, heal 2% of your HP.",
    "image": "enhance_production.png",
    "effect": "passive_healing",
    "params": {
      "healing_percent": 0.02,
      "trigger": "turn_end"
    }
  },
  "Reflex Tuning": {
    "description": "At the end of your turn, attack once more.",
    "image": "reflex_tuning.png",
    "effect": "extra_attack",
    "params": {
      "attacks": 1,
      "trigger": "turn_end"
    }
  },
}
Updated Heroes
{
  "heroes": [
    {
      "name": "Europa",
      "level": 1,
      "rank": 1,
      "stats": {
        "HP": 100,
        "Armour": 30,
        "Attack": 30
      },
      "xp": 0,
      "equipment": {
        "gear": null,
        "stim": null,
        "augment": null
      },
      "abilities": []
    },
  ]
}

Ability Mapping
# Dictionary mapping effect types to placeholder functions
ABILITY_FUNCTIONS = {
    "passive_healing": apply_passive_healing,
    "extra_attack": apply_extra_attack,
    "damage_reduction": apply_damage_reduction,
    # Add more as needed
}

def apply_ability(hero, ability_name, game_state=None):
    """Apply an ability's effects to a hero during gameplay"""
    # Load ability data
    with open("data/heroes/abilities.json", "r") as f:
        abilities = json.load(f)
    
    if ability_name in abilities:
        ability_data = abilities[ability_name]
        effect_type = ability_data["effect"]
        
        if effect_type in ABILITY_FUNCTIONS:
            # Call the appropriate function with the ability parameters
            ABILITY_FUNCTIONS[effect_type](hero, ability_data["params"], game_state)
            return True
    
    return False

# Placeholder ability effect functions
def apply_passive_healing(hero, params, game_state):
    """Placeholder for passive healing abilities"""
    if game_state and game_state.current_phase == params.get("trigger", "turn_end"):
        healing_amount = int(hero.stats["HP"] * params.get("healing_percent", 0.02))
        print(f"{hero.name} healed for {healing_amount} HP")
        # Actual healing would happen here

def apply_extra_attack(hero, params, game_state):
    """Placeholder for extra attack abilities"""
    if game_state and game_state.current_phase == params.get("trigger", "turn_end"):
        print(f"{hero.name} attacks {params.get('attacks', 1)} extra time(s)!")
        # Actual attack logic would be here

def apply_damage_reduction(hero, params, game_state):
    """Placeholder for damage reduction abilities"""
    # This would be called when calculating damage
    print(f"{hero.name} has {params.get('reduction_percent', 0.1) * 100}% "
          f"{params.get('damage_type', 'all')} damage reduction")

 Future implementation
 - Hero and Item levelling
 - Resources for levelling
 - Hero rank ups
 - Switch between heroes from the character details screen
 - Item merging and scrapping