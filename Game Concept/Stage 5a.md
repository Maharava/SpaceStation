## Stage 5
Stage 5 is the combat system, card battler, and the overall 'run' aspect of the game. It will be broken into stages:
 - 5a
  - The player is able to access the story mode of the game and select an unlocked raid (the new name for runs)
  - The game will load the first battle of the raid, inclduing the players deck, and unique hero cards. There is no gameplay, just the ability to see it.
  - The player can quit the raid.
- 5b
 - The player can play cards against the enemies, achieving card effects. There is no way to progress, even if the enemies are defeated.
 - Player will be able to end turn. The enemies won't take any actions on their turn, instead passing straight back to the player.
 - This allows testing of the card effects and triggers.
- 5c
 - Enemies will have abilities set and be able to take turns.
 - The player will be able to have an actual battle on the first stage of the raid, with victory and defeat implemented (both returning the player to the raid select screen).
- 5d
 - rewards for victory implemented, including essence, the ability to add a new card to the deck, and possible upgrade tokens.
 - Player is able to advance through the battles, with them getting progressively more difficult.
5e
 - Implementation of the special events that can occur during raids - card upgrade, card removal, healing, bonus treasue
 - Implementation of mini bosses and bosses
 - implementation of raid complete victory, unlocking the next raid, and rewards

This document is for ## 5a ##. Do not implement or wokr on any other stage.

## Implementation

* Raid Screen
 - The 'Deploy' button on the home screen now goes to a new Raid screen
 - The raid screen's background is set from ``data/assets/ui/backgrounds`` and is named ``raid_X.png``, with X being the number of the raid chosen. If no raid has yet been chosen, the ``raid_0.png`` is used.
 - There will be four clickable buttons on this screen, one for each raid. The first button, ``Io`` works, with the rest called ``Coming soon``.
 - Clicking a raid button (the ''Coming Soon'' ones currently do nothing) will change the background, and create a dialogue box with the basic story. this is taken from data/assets/raids, ``io_raid.json`` (for the Io raid). This json is the home repository of all the Io raid data. A confirmation '`Deploy'` and ``Back`` button will appear, with back closing the dialogue window and returning the background to default.
 - Clicking the ``Deploy`` button will go to the battle screen, loading data from Io's JSON to populate. The JSON will contain:
  - An entry for each stage of the raid (10 stages total), including a dialogue entry that can be blank.
  - An entry for each enemy (up to three) for each stage of the raid, which contains:
   - Name, .png, HP, attack, armour
   - Nothing else this implementation
## Battle Screen
 - If there is a dialogue entry for this stage, the screen will go black and the dialogue will show. The player may click past it to go straight to the battle screen. The bottom right of the black screen will say 'Click to advance', while the dialogue text will be centered.
 - The players starting deck will load and shuffle, with the data/assets/ui/deck.png icon appearing in the bottom left. This icon will have a small number in a circle showing how many cards are left. The deck is shuffled, and four cards are drawn. They will be displayed in the middle of the screen, using their images from data/assets/cards.
 - Mousing over a card scales it up slightly, and creates tooltips on its right side for any special effects the card has.
 - the back of the currently selected hero is shown in the centre of the screen, with the cards drawn on top.
 - The enemies are across the top half of the screen
 - Hero stats (Hp as a health bar, with Attack and Armour showing the value with thir icons just below it) sits in the top left of the screen, along with the heroes portrait.
## Cards
 - Cards are only used in raids. The player starts with a deck of 14 Basic cards which are the same every raid, plus 2 unique cards from their selected hero. Cards collected during the raid by winning battles only persist for the raid and are lost when the raid ends.
 - The basic deck is contained as a list in each heroes JSON file.
 - There is no card collection or deck building mechanic.
 - Card data is stored in data/cards as .jsons.
 - All cards can be upgarded once, improving their abilities, via a special event (only implementation needed is the field for the upgrade)

## Battle Mechanics
 - The player has three energy, restoring to three at the start of each turn.
 - Playing a card costs 1 energy. Some cards may refund the energy spent when they're played
 - Cards may do damage (using the heroes Attack stat), block damage (granting the hero armour based on their armour stat), or apply buffs/debuffs. The target of a played card is always the centre enemy. Some cards may hit all enemies.
 - Arrows to either side of the enemies allow the player to 'rotate' them, moving the enemy order around.
 - Buffs and debuffs give flat effects, not stacking. They lose one charge each time - stacking them increases the number of turns they last. Some cards may interact with the number of buff/debuff stacks.
 - The buffs and debuffs are:
  - Haste, player only buff, gives +1 energy
  - Targeted, universal debuff, increases damage taken by 25%
  - Adrenaline, universal buff, increases all damage dealt by 15%
  - Shields, universal buff, at start of turn gain defence x1 (same as the card)
  - Lash out, universal buff, at end of turn attack once
  - Shellshock, universal debuff, lowers defence by 25%
  - Blinded, universal debuff, 50% chance any attack fails
  - Stunned, universal debuff, lowers attack by 25%
  - Injured, universal debuff, at end of turn reduces HP by 5% of max
  - Hypo-spray, universal buff, at end of turn heals 5% HP
 - Buffs and debuffs counters reduce at the end of the opposite sides turn - eg, if the player gives a debuff to an enemy, it's counter goes down at the end of the debuffs turn
## Card JSON Structure
See Card List.md

## UI
 - In addition to the position of the hero, enemies and cards, a pause icon will exist in the top left. Clicking it pauses the game, creating a semi-transparent black rectangle over most of the screen, with two buttons - reums or quit. Quit returns the player to the raid select screen.



 WORK
 Missing Technical Details
File Organization: data/raids, a new folder, then broken down (eg data/raids/io, data/raids/hamburger, etc)
Hero Integration: Hero selection will be on the raid select page. Unlocked heroes will have their portraits on the left hand side. Clicking one will select them, bordering them in red. You cannot click 'Deploy' until you've chosen a hero.
Asset Requirements: We'll work it out as we go

How are the raid buttons positioned and styled?TBA
What's the exact appearance of the dialogue box for raid stories? - clean and simple, same as our other boxes


How are multiple enemies positioned? Is there a specific arrangement for 1-3 enemies? - 1st enemy always in middle, second always to the left of them, 3rd on the right of them
What are the exact dimensions/positions for the card display area? - come up with what would work best. Cards will be 512x768 and should be scaled down
How much scaling should occur when mousing over cards? - make them readable, maybe +25% to start with. Only one card should be scaled up at a time.
Where exactly is the deck positioned in relation to other UI elements? - Bottom left corner.
Visual Representations:

How should buffs/debuffs be displayed visually in this non-playable implementation? - They can't be used in battle, list this for future implementation (5b)
How should energy be visually represented? - energy will use data/assets/ui/energy.png to thr right of the deck, with a counter in bold white font for the energy you have left.
What's the exact styling for the hero health bar and stats display? - Portrait to the left. Health bar to the right of it, slightly below the top of the portrait, and stats in a row under that, the bottom of the stats being slightly above the bottom of the portrait


Raid Data: How is raid unlock status tracked and stored? - add it to the player jsons.
Deck Construction: What's the exact process for building the initial deck from basic cards plus hero cards? - the hero chosen will have their starting deck in their json as a list of card ids. 
Hero-Specific Cards: How are hero-specific cards structured in the data files compared to basic cards? - exact same way

Data Structure: Create a simple, flexible json structure for raid data
