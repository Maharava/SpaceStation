Stage Two: Equipment System
Equipment Collection UI

* Inventory
 - The player inventory is stored in data/player/inventory.json, which contains the names of unequipped collected gear, its rarity and level. ALl gear now has a level mechanic.
 - A function to add an item to the players inventory needs to be created. Items do not stack, so each is added separately. This function is called ```inventory_add```
 - Three new data folders, data/items, data/items/stim and data/items/augment need to be made for the other two item classes. Data/gear will be moved into data/items
* Changed Hero Detail Screen
 - The hero detail screen is now more compact. The hero name and rank remains along the top, and there is a transparent white rectangle behind it. This rectangle covers the left half of the screen with a border around its edges.
 - Directly under the Hero name is a black bar. The bar has white text showing X/Y - X being the current XP and Y being the required amount for next level (20). The black bar fills up with a blue line (that's slightly smaller than the bar) as XP increases. The Hero level is shown after the XP bar
 - Under this is the stats. The data/assets/ui icons, hp.png, attack.png, armour.png are used in place of text. These are in a row, with the heroes stat value shown next to them (eg, hp.png 125 attack.png 30, etc). Every time a mouse button is clicked (right or left), the stat values are checked and updated.
 - Directly below this is the three equipment slots - Augment, Gear and Stim. These will always show whatever item is equipped in that slot.
 - Under these is the Inventory window.
* Item inventory screen
 - the Inevntory window shows all the players unequipped items. 
 - Item icons should be small but readable, allowing five in a row from the left side of the screen up to the egde of the character image. A scrolling system is implemented should there not be enough space for all the rows of items.
 - The scrolling system will have both a scrollbar and accept scrollwheel
 - Items do not stack. Duplicate items will be shown as two separate tiles, to accommodate the implementation of levelling and merging
 - Item levels will appear as a small black number inside a circle in the bottom right of the tile. The circle's colour will match the items rarity
 - If there is an item equuipped, the equipment slots white backound changes to match the colour rarity
* Inventory mechanics
 - All items are stord and loaded as dictionaries.
* Item rarity
 - All equipment tiles now must have a coloured border that matches their rarity:
  - Common, Grey
  - Rare, Blue
  - Epic, Purple
  - Prototype, Black
* Equipping Mechanics
 - Right clicking a piece of unequipped equipment OR an equipment slot first checks if there's something equipped in the relevant slot by running ```check_equipped```. This function checks if their is equipment in that slot. If their is, it unequips, caling ``inventory_add`` with the item that's in the slot, emptying the slot of its item, then calling ``calculate_stats`` to update the hero stats. Next it calls ``update_graphic``, which will force the equipment slot to check if it has anything equipped, and adjust its graphic accordingly.  Finally, ``update_player`` is called, which saves the currently empty slot to data/player/heroes.json.
 - If an unequipped item was right clicked, the game next runs ``equip_item``, passing the relevant slot as a variable, and destroys itself, removing itself from the inventory with ``inventory_remove``. ``equip_item`` then adds the item to the equipment slot, calls ``calculate_stats`` and ``update_graphic``. Finally, ``update_player`` is called, which saves the currently equipped item to data/player/heroes.json.
 - All other items shift their location to account for the empty slot.
 - Equipment slots always show the correctly equipped item 
 - data/player/heroes.json is updated with the equipped items of the heroes in the correct slots, and data/player/inventory.json is updated whenever gear is removed from or added to the inventory (``remove_inventory`` and ``add_inventory``).
 - If there is nothing in a slot the player is right clicking, nothing happens.
 - Items know which slot to go to due to their .jsons, which will need an entry called "slot" that matches "augment","gear" or "stim"
* Hero listed abilities
 - As some gear grant special abilities, heroes need to track what abilities they have. The player/heroes data json will be used for this.
 - A dictionary will be created, mapping ability names from gear to function/script calls. Placeholder code will be created for now. This will be stored in utils/abilities/, along with the (eventual) ability scripts
 - There are currently no plans for how the actual scripts/abilities/code will be implemented during runs
 - There is no way to see what abilities a hero has apart from mousing over the equipped items.
 - The heroes.json will store the abilities as the ability names, allowing easy matching to functions with the new mapping scripts.
* Equipment Tooltips Enhancement
 - When moused over, equipment and item slots will call ``tooltip()``. For empty equipment slots, it will just show the name of the slot and what it improves. For filled equipment slots or item slots, it shows the name and rarity of the item, the stat value (using the UI icon) and the name and description of its ability (if any)


Completion criteria:
 - New folder structure (at minimum other folders as necessary):
  - data/heroes/abilities.json
  - data/items/gear/
  - data/items/augment/
  - data/items/stim/
  - data/player/inventory.json
 - Item ability data implemented in the relevant item jsons, and the ability lists added to the heroes.json. Inventory json added to data/player
 - Placeholder ability code added to the most relevant folder, and a utils/ script created mapping ability names to the relevant (placeholder) code
 - Player right clicking an equipment slot with something equipped removes it, updates the graphic, updates the stats, and adds it to the inventory.
 - Player right clicking on an item has it check the relevant slot (unequipping as above if needed), then adds the item to the slot, removes it from inventory, updates graphics, updates stats.
 - Back button to return to character roster remains and works
 - Mousing over an equipment or item slot will show a tooltip
 - Hero stats and abilities update as items are equipped/unequipped
 
 Future implementation
 - Hero and Item levelling
 - Resources for levelling
 - Hero rank ups
 - Switch between heroes from the character details screen
 - Item merging and scrapping