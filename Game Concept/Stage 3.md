Stage 3 Implementation - Revised
Hero and Item improvements

New Currencies
Essence is a new tracked currency, attached to the player.
Upgrade Tokens is a second tracked currency, with a variation for each item (Gear, Augment and Stim)
Neural Patterns as the third and rarest currency, and can be used to recruit new heroes.
These are stored in data/player/currencies.json. Players will start with 1000 essence and 4 of each upgrade token, with no neural patterns
{
  "essence": 1000,
  "upgrade_tokens": {
    "gear": 4,
    "augment": 4,
    "stim": 4
  },
  "neural_patterns": 0
}
Currency transactions are handled by utils/currency.py script with functions: add_currency, remove_currency, check_amount
Currency UI elements are created only as needed (e.g., essence in top right of hero details and character roster)
Transactions fail if there's insufficient currency, with costs shown in red when unavailable
Essence is capped at 50,000, upgrade tokens at 50 each, and Neural patterns at 100
Item Improvements
Items have levels, starting at level 1, stored as a 'level' entry in player item JSON data
Maximum item level depends on rarity:
Common: Max level 5 (1 × 5)
Rare: Max level 10 (2 × 5)
Epic: Max level 15 (3 × 5)
Prototype: Max level 20 (4 × 5)
Upgrading costs Essence and Upgrade Tokens
Essence costs scale with rarity and level:
Common: 100 Essence + 50 per level after 1
Rare: 200 Essence + 100 per level after 1
Epic: 400 Essence + 200 per level after 1
Prototype: 800 Essence + 400 per level after 1
Upgrade Token costs:
Common: 1 token per upgrade
Rare: 1 token (levels 2-5), 2 tokens (levels 6-10)
Epic: 2 tokens (levels 2-10), 3 tokens (levels 11-15)
Prototype: 3 tokens (levels 2-15), 4 tokens (levels 16-20)
Level-up stat bonuses:
Stim items: +5 HP per level
Gear/Augment items: +2 Attack/Armor per level
Item stat calculation: Base stat + ((level-1) × bonus)
Example: Level 3 common gear with base 10 Armor = 10 + (2 × 2) = 14 Armor
Item stats are calculated when needed (only when equipping/unequipping items)
Item Merging:
Three identical items of the same rarity and name can be merged
Merging creates one item of the next rarity tier
The new item keeps the highest level from the three merged items
Merging progression: Common → Rare → Epic → Prototype
Prototype items cannot be merged
Item merging has no currency cost
No confirmation UI is needed for merging
Hero Improvements
Heroes gain XP from runs, which are not yet implemented
XP is stored in heroes.json with an xp field
A new function, add_xp will need to be made, adding XP to a given hero
When a Hero has accumulated enough XP, a 'level up' button will appear next to the XP bar on the hero details screen
Levelling up costs (new level*200) Essence
Heroes need 15×Current Level XP to level up, with XP resetting to 0 each level up
Levelling up increases stats according to the heroes JSON file, using entries like 'hp_level:' in data/heroes
When a Hero reaches level 10, they can be ranked up. This costs 5000×(current rank) essence
Ranking up boosts all base hero stats (excluding gear effects) by 25%
XP visual feedback is already implemented and current rank UI is sufficient
Numbers
All costs, for levelling heroes and items or ranking a hero up, have their base values stored in a new config.json in the root of the game for easy changes.
UI
Total essence is shown in the top right of the Hero Detail and Character Screen, using essence.png as an icon
UI icons need to be small, similar in size to the stat icons
Left clicking an item will bring up a small box with:
Cost to level-up in essence (red text if insufficient)
Upgrade token cost shown as X/Y (player amount/needed amount)
'Upgrade' button at the bottom
If item is max level, 'Max Level' is shown instead of upgrade options
Pressing upgrade reduces currencies and increases item level without closing the box
Upon levelling up equipped items, hero stats are recalculated with only the difference
Clicking anywhere else closes this upgrade window
Next to the 'Upgrade' button is a 'Scrap' button
If three identical items of same name and rarity exist, a 'Merge' button appears
Item names are consistent across rarities (e.g., Sweat Band (Common), Sweat Band (Rare))
Item Scrapping
Clicking 'Scrap' shows a confirmation window with resource rewards
Items grant Essence (20×rarity), upgrade tokens of the same class (0 for common, 1 for rare and epic, 2 for prototype)
Chance of Neural Patterns: 10%/20%/35%/55% by rarity, rolled when 'scrap' is clicked
Resource rewards show icons with % chance for Neural Patterns
Completion criteria
 Completion criteria:
 - Essence can be seen in the top right of the character roster and hero details screen
 - Clicking an item, equipped or otherwise, with the left mouse button shows the Upgrade/Scrap window, with correct costs shown. The game also checks for 2 duplicate items of the same rarity and creates the merge button if they exist. The upgrade window shows the correct amounts of Upgrade Tokens
 - Clicking 'upgrade' increases the level of the item by 1, does not close the window, and adjusts currency correctly. If the item is equipped, the game calculates the heroes stats, including the improvement. Stim items have their stat boosted by 5, 2 for the others.
 - The heroes stats are recalculated with the improved item (if it was equipped)
 - Item tooltips correctly show the items stats, including its level ups (if any) in the calculation
 - Clicking 'Scrap' removes the item from the inventory and grants the shown currencies. It also clses the window.
 - Clicking anywhere else on the screen closesthe window. Clicking on an item or equipment slot with the upgrade window open does not open a new window, just closes the current one.
 - Clicking 'Merge' unequips any of the items (if equipped, running all associated unequip code), adds a new item of the next tier at the same level as the highest input item, and removes the three items from the inventory.

Examples:
 - A Sweat Band (common) is level 2 (base Armour 5, level 2 adds 2, so Armour 7). It is upgraded to level 3, bringing the armour to 9. It is equipped, so the heroes stats are calculated again, increasing the armour by 2.
 - Three Lact-X (rare) are combined. Their levels aree 7, 5 and 1. If any of the Lact-X are equipped, they are unequipped and the heroes stats are recalculated. The new Lact-X (epic) is added to the inventory at level 7, and the three Lact-X (rare) are deleted.