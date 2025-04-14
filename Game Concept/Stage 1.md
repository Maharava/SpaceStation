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
   - **Rank**: Hero's rank from 1-5, affecting appearance and stats.

3. **Equipment Slots**:
   - **Enhancement**: Boosts Attack.
   - **Gear**: Enhances Armour.
   - **Stim**: Enhances HP.
   - Each item has a rarity tier (common, rare, epic, prototype) and a secondary ability.

4. **Hero Ranks**:
   - Heroes start at Rank 1 and can progress to Rank 5.
   - Each rank increases base stats and changes hero appearance.
   - Hero images follow the naming convention: hero_X.png (where X is the rank number).
   - On the hero details screen, hero ranks are shown as small icons under the heroes name, 1 for each rank. The icones are data/assets/gui/jupiter.png. These icones are 512x512 and need to eb scaled down substantially without losing their quality

5. **Tooltips**:
   - Mousing over equipment slots shows a tooltip with slot purpose or equipped gear details.

6. **Navigation**:
   - A non-functional "Home" button on the character collection screen.

7. **GUI size**:
   - Ideal for common iPhone and Android screens

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

### Notes
- Placeholder functionality for equipping gear and home screen navigation will be added in future stages.
```
