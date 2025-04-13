#jovian_cards/jovian_cards/README.md
# Jovian Cards: Game Concept and Implementation Guide

## Overview
Jovian Cards is a casual RPG card game where players collect heroes and battle enemies in a card-based system. The game features a roguelike progression with temporary card collections during runs and permanent hero upgrades between runs.

## Gameplay Features
- **Main Loop**: Battle enemies, progress through rooms, and encounter shops/events.
- **Boss Fights**: Minibosses halfway through a run and a final boss at the end.
- **Hero Progression**: Collect heroes and upgrade them permanently using currencies/materials.

## Directory Structure
```
jovian_cards
├── src
│   ├── main.py
│   ├── game.py
│   ├── ui
│   │   ├── __init__.py
│   │   ├── character_screen.py
│   │   ├── hero_detail_screen.py
│   │   ├── ui_elements.py
│   │   └── tooltip.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── hero.py
│   │   └── gear.py
│   └── utils
│       ├── __init__.py
│       ├── constants.py
│       └── resource_loader.py
├── data
│   ├── assets
│   │   ├── heroes
│   │   └── gear
│   ├── heroes
│   ├── player
│   └── gear
├── requirements.txt
└── README.md
```

## Setup Instructions
1. Clone the repository.
2. Install the required dependencies listed in `requirements.txt`.
3. Run the game using `python src/main.py`.

## Future Features
- Equipping gear.
- Transitioning between character collection and hero screens.