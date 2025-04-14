Stage 3 Implementation
Hero and Item improvements

* New Currencies
 - Essence is a new tracked currency, attached to the player. 
 - Upgrade Tokens is a second tracked currency, with a variation for each item (Gear, Augment and Stim)
 - Neural Patterns as the third
* Item Improvements
 - Items start at level 1, with a maximum level equal to their rarity x 5 (Common = 1, Rare = 2, Epic = 3, Prototype = 4)
 - Upgrading an item costs Essence and the relevant Upgrade Tokens, with costs increasing for both. Upgrading a common item to Level 2 costs 100 Essence and a single Upgrade Token. Higher rarities cost more
 - Three Items of the same type and rarity can be merged, removing them from the players inventory and adding a new item of a higher rarity tier. The new item will keep the highest level of the three items used to merge.
 - Prototype items cannot be merged.
 - Items levelling up grant +5 HP or +2 Attack/Armour per level.
* Hero Improvements
 - Heroes gain XP from runs, which are not yet implemnted. 
 - When a Hero has accumulated enough XP, a 'level up' button will appear next to their name on the character details screen. Levelling up costs (new level*200) Essence.
 - Levelling up increases stats according to the heroes .json file, which will need a 'stat level up' section.
 - When a Hero reaches level 10, they can be ranked up. This costs 5000x(current rank) essence. Ranking up boosts all base hero stats(excluding gear effects) by 25%.
* Numbers
 - All costs, for levelling heroes and items or ranking a hero up, have their base values stored in a new config.json in the root of the game for easy changes.
* UI
 - Total essence is shown in the top right of the Hero Detail and Character Screen.
 - When the inventory window is open, the associated upgrade tokens are shown under the equipment slot.
 - Left clicking an item - in the inventory or in the equipment slots - will bring up a small box with the cost to level-up in essence (red text if the player doesn't have enough) and the upgrade token cost shown as X/Y, with X the players amount and Y the amount needed. A button, 'upgrade', sits at the bottom of this box. Pressing it reduces the associated currencies appropriately and increases the level of the item, but doesn't close the box. A check is needed to make sure the click doesn't activate the button repeatedly.
 - Clicking anywhere else closes this upgrade window.
 - If an item is max level, it will say so here.
 - Next to the 'Upgrade' button will sit a 'Scrap' button
 - If the game detects two other items of the same name and rarity, a third  button, 'Merge' will appear, showing the cost in essence of the merge. Clicking it will unequip the item (if equipped or, if unequipped but one of the other two is equipped, unequipping that), save the highest level amongst them, and remove the from the player inventory, before adding the next rarity tier up, at the saved level, to the players inventory.
 - Item names are not unique to thr rarity level - eg, Sweat Band (Common), Sweat Band (Rare), etc. making it easy to find the next tier
 - The newly added item, if above level 1, will need its stats adjusted for the level ups (eg, a level6 common Sweat Band, a Level 4 and a Level 1 are merged, making a level 6 Rare Sweat Band. The Rare Sweat Band has its stats increased as if it had gone up 5 levels)
* Item Scrapping
 - Next to the Upgrade button when left clicking is the 'Scrap' button. Clicking this will create a confirmation window, which will show the player the resource rewards. If the player clicks yes, the item is removed from their inventory, and they are given the resources.
 - Items grant Essence (20xrarity), upgrade tokens of the same class (0 for common, 1 for rare and epic, 2 for prototype) and a chance of granting Neural Patterns (5%,10%,15% and 20% for each rarity)