# Jovian Cards: Game Concept and Implementation Guide

## Overview
Jovian Cards is a casual RPG card game where players collect heroes and battle enemies in a card-based system. The game features a roguelike progression with temporary card collections during runs and permanent hero upgrades between runs.

## Gameplay Features
- **Main Loop**: Battle enemies, progress through rooms, and encounter shops/events.
- **Boss Fights**: Minibosses halfway through a run and a final boss at the end.
- **Hero Progression**: Collect heroes and upgrade them permanently using currencies/materials.

## Implementation Guide

### Stage One: Character Screen
This stage focuses on creating a character selection screen.

#### Features
1. **Hero Selection**:
   - Display unlocked heroes as clickable tiles with portraits.
   - Clicking a hero shows their full image, stats, and equipment.
   - A back button returns to the character selection screen.

2. **Hero Stats**:
   - **HP**: Maximum health (tracked only during runs).
   - **Armour**: Defensive stat.
   - **Attack**: Offensive stat.
   - **XP**: Experience points.
   - **Level**: Hero's current level.

3. **Equipment Slots**:
   - **Enhancement**: Boosts Attack.
   - **Gear**: Enhances Armour.
   - **Stim**: Enhances HP.
   - Each item has a rarity tier (common, rare, epic, prototype) and a secondary ability.

4. **Tooltips**:
   - Mousing over equipment slots shows a tooltip with slot purpose or equipped gear details.

5. **Navigation**:
   - A non-functional "Home" button on the character collection screen.

#### Data Structure
- **Hero Data**:
  - `data/heroes`: JSON files with base stats (e.g., level 1 stats, name, description, image names).
  - `data/player/heroes`: A single JSON file listing collected heroes and their current stats/equipment.

- **Gear Data**:
  - `data/gear`: JSON files for each gear item, including stats for each rarity tier, name, description, ability, and image name.

- **Assets**:
  - `data/assets/heroes`: Hero images (portraits, full body, back images).
  - `data/assets/gear`: Gear images.

#### Example Data
**Hero JSON (data/heroes/europa.json)**:
```json
{
  "name": "Europa",
  "description": "A brave warrior from the Jovian moons.",
  "level_1_stats": {
    "HP": 100,
    "Armour": 30,
    "Attack": 30
  },
  "images": {
    "portrait": "europa_port.png",
    "full_body": "europa.png",
    "back": "europa_back.png"
  }
}
```

**Gear JSON (data/gear/sweat_band.json)**:
```json
{
  "name": "Sweat Band",
  "rarity": "common",
  "stats": {
    "Armour": 5
  },
  "ability": "Soak up",
  "image": "sweat_band.png"
}
```

#### Initial Heroes
1. **Europa**:
   - HP: 100, Armour: 30, Attack: 30, XP: 0, Level: 1.
   - No equipment.
2. **Ganymede**:
   - HP: 110, Armour: 25, Attack: 30, XP: 0, Level: 1.
   - Equipped with Sweat Band (common).

#### Completion Criteria
- Hero portraits load as clickable tiles.
- Clicking a hero displays their full body, stats, and equipment.
- Back button returns to the hero collection screen.
- Tooltips display on equipment slots.
- "Home" button is present but non-functional.

#### Dependencies
- Python 3.10+
- Libraries: `pygame`, `json`, `os`.

#### Future Features
- Equipping gear.
- Transitioning between character collection and hero screens.

### Directory Structure
```
data/
├── assets/
│   ├── heroes/
│   └── gear/
├── heroes/
├── player/
│   └── heroes.json
└── gear/
```
```
```

### Notes
- Placeholder functionality for equipping gear and home screen navigation will be added in future stages.
```