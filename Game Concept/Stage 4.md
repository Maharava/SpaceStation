# Stage 4 Implementation - Home Screen
Central Game Hub & Navigation

## Home Screen Implementation
The home screen serves as the central hub connecting all game systems. It provides navigation to existing features and placeholders for upcoming features.

### Core Components
- Character Roster button leading to the existing character selection screen
- "Start Run" button (placeholder for future battle system)
- "Develop" button for future hero gacha
- Currency display showing Essence, Upgrade Tokens, and Neural Patterns
- "Secretary" system, allowing the player to choose a collected hero to appear on this screen
- Basic interactions with "Secretary" (clicking shows dialogue)

### UI Layout
- Background image loaded from `data/assets/ui/home_screen.png` (will be provided)
- Navigation buttons positioned along bottom of screen
- Currencies displayed at top middle
- Secretary character appears on left side of home screen (full-body image)
- Same resolution and scaling as previous stages

### Secretary System
- Hero is set as secretary via a small round button on bottom right of hero details screen (data/assets/ui/sec_button.png)
- Secretary dialogue options stored in hero core JSONs, different for each rank (5-10 options per rank, with more for higher ranks)
- When clicked (with 5-second cooldown), secretary says random dialogue
- Dialogue appears in semi-transparent grey box that fades after 5 seconds

#### Secretary Dialogue Format
```json
"dialogue": {
  "rank1": [
    "Hello, I'm new here!",
    "Nice to meet you.",
    "I'm still learning...",
    "What should we do today?",
    "I hope I can be helpful."
  ],
  "rank2": [
    "I'm getting stronger!",
    "Let's go on an adventure!",
    "I've been training hard.",
    "Do you need anything from me?",
    "The other heroes are nice.",
    "Have you seen my new skills?"
  ],
  // More ranks with more dialogue options
}
```

### Required Files
A new `screens` folder will organize all screen-related files:
- `screens/home_screen.py`: Main home screen implementation
- `screens/character_screen.py`: Move existing character roster code here
- `screens/hero_detail_screen.py`: Move existing hero detail code here
- `utils/screen_manager.py`: Handle transitions between screens
- `config/home_screen.json`: Store UI positioning information

### Navigation System
The screen manager will use a stack-based approach:
- When opening a new screen, it gets pushed onto the stack
- Back button pops the top screen from the stack
- Home button clears the stack and pushes only the home screen
- Game entry point changed to start at home screen

## Optional Quality Improvements
These smaller improvements enhance the existing stages:

### Save System
- Create a proper save/load system using `utils/save_manager.py`
- Auto-save when changes are made to heroes/inventory
- Add a small save indicator animation when auto-saving occurs

## Completion Criteria
- Home screen loads as the initial game screen
- Character roster button navigates to the character screen
- Back button from character screen returns to home screen
- Start Run and Develop buttons exist with a "Coming Soon" tooltip
- All currencies are displayed on the home screen
- Secretary system functions with dialogue based on hero rank
- Screen transitions are smooth, instant and bug-free
- All existing features from previous stages remain functional

## Future Implementation
- Battle system with card mechanics
- Run progression system
- Shop interface from home screen
- Daily rewards and challenges
- Achievement system

## Refactoring Risks:
Moving existing functionality to new files could break current features
Potential for circular imports

## Secretary Dialogue Box:
Text overflow handling for different dialogue lengths
Positioning that works with all possible secretaries

## Navigation Edge Cases:
What happens when rapidly switching screens?
How to prevent multiple screen instances?