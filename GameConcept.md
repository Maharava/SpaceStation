================================================================
STARBOUND EXILE: DERELICT AWAKENING
COMPREHENSIVE GAME CONCEPT GUIDE
================================================================

TABLE OF CONTENTS
1. Game Overview
2. Core Gameplay Loops
3. Game Systems
   3.1 Exploration & Combat
   3.2 Procedural Generation
   3.3 Drone System
   3.4 Survivor System
   3.5 Station Hub
   3.6 Progression & Upgrades
4. Technical Implementation
5. Development Roadmap
6. Project Structure

================================================================
1. GAME OVERVIEW
================================================================

"Starbound Exile: Derelict Awakening" is a sci-fi roguelite where players emerge as the sole survivor of a derelict space station. The game alternates between short, intense procedural missions and strategic hub management.

CORE PREMISE:
Players pilot their starship into procedurally generated sectors for 10-15 minute runs of exploration and combat, returning to their station hub to upgrade technology, rescue survivors, and manage a growing fleet of drones.

KEY FEATURES:
- Top-down, asteroids-style ship control during exploration/combat
- Visual novel-style station management between missions
- Procedurally generated missions and environments
- AI-controlled drone companions with specialized abilities
- Character-driven survivor recruitment system
- Freeform upgrade paths with meaningful progression
- Defined endgame goal of full station restoration

TARGET AUDIENCE:
- PC players initially (potential Android port later)
- Fans of roguelites, space exploration, and base management games
- Players who enjoy both action gameplay and strategic decision-making

VISUAL STYLE:
- Drawn/anime style artwork throughout
- Consistent sci-fi aesthetic between exploration and station sections

================================================================
2. CORE GAMEPLAY LOOPS
================================================================

MICRO LOOP (10-15 MINUTE MISSIONS):
1. Launch from station with equipped ship and selected drones
2. Navigate procedurally generated sector with WASD controls
3. Encounter and overcome various hazards (combat, environmental)
4. Complete mission objectives (explore, salvage, rescue, etc.)
5. Collect resources, technology, and rescue survivors/drones
6. Return to station or face resource loss upon death

MACRO LOOP (STATION MANAGEMENT):
1. Process collected resources and technology
2. Repair ship/drones
3. Interact with survivors through visual novel interface
4. Assign survivors to station modules
5. Upgrade ship capabilities and equipment
6. Repair and expand station facilities
7. Select next mission and prepare loadout

PROGRESSION LOOP:
1. Incrementally improve ship capabilities
2. Increase drone fleet size and diversity
3. Rescue more survivors with unique skills
4. Repair and expand station modules
5. Unlock new technology and crafting options
6. Access more challenging sectors with better rewards
7. Work toward endgame goal of full station restoration

================================================================
3. GAME SYSTEMS
================================================================

3.1 EXPLORATION & COMBAT
------------------------
PERSPECTIVE: Top-down view during exploration/combat phases

SHIP CONTROLS:
- WASD movement (asteroids-style physics without inertia)
- All weapons fire in predefined arc or auto fire and target on their own
- Direct control of ship weapons (other than auto-fire weapons)
- Resource collection mechanics (hard resources like salvage, tech, and soft resources like scan data)
- Environmental hazard interactions
- Puzzle solving

COMBAT MECHANICS:
- Player-controlled ship weapons
- Up to 3 AI-controlled drone companions (max number dependant on ship upgrades)
- Various enemy types with distinct behaviors
- Environmental dangers and obstacles
- Resource management during combat (shields, energy, fuel, etc.)

MISSION STRUCTURE:
- Clearly defined objectives generated procedurally
- Various mission types (rescue, salvage, combat, exploration, etc.)
- Dynamic events and challenges
- Risk/reward decisions throughout
- Extraction mechanics to return to station

3.2 PROCEDURAL GENERATION
------------------------
MISSION GENERATION:
- Missions are generated first, then appropriate layouts
- Varying difficulty levels affect rewards and challenges
- Mission types include (but not limited to) rescue, salvage, combat, and exploration
- Objectives tailored to mission type

MAP GENERATION:
- Procedurally generated sector layouts
- Various environment types (asteroid fields, nebulae, derelicts, black holes, other sci-fi esque ideas)
- Placement of objectives, hazards, and resources
- Dynamic events that alter gameplay (solar flares, etc.)
- Escalating difficulty based on progression

BALANCING RANDOMNESS:
- Core gameplay paths always viable
- Randomness focused on variety, not artificial difficulty
- Consistent risk/reward structure
- Random elements build upon established mechanics

3.3 DRONE SYSTEM
------------------------
DRONE TYPES:
- Combat drones (offensive capabilities)
- Scanner drones (reveal map, highlight resources, gather scan data, improve ship targeting)
- Repair drones (restore ship systems/health, boost hacking of drones)
- Collection drones (gather resources hard resources, salvage)
- Unique drones with specific abilities

DRONE CAPABILITIES:
- AI-controlled during missions (no direct player control)
- Maximum 3 drones per mission depending on ship capacity
- Drones can be damaged or lost during missions (losing a drone is rare/difficult)
- Collection (and some Unique) Drones provide resource protection on death (prevent total loss)

DRONE PROGRESSION:
- Drones can be upgraded with salvaged technology
- Specialized drones for specific mission types
- Drone Bay station module manages drone swarm
- Drones are found on missions and must be hacked to gain control for future use

3.4 SURVIVOR SYSTEM
------------------------
SURVIVOR MECHANICS:
- Survivors found during missions (sometimes randomly in any mission, sometimes missions are to find them)
- Most found survivors 'move on'(not collected, small chance of 'collecting' them)
- Collecting survivors is effectively a gacha mechanic
- Each survivor has unique personality and backstory
- Survivors provide both narrative content and gameplay benefits
- Visual novel style interactions at station
- Relationship building and development over time

SURVIVOR BENEFITS:
- Specialized skills for station operations
- Unique crafting abilities
- Mission support capabilities
- Unlock special technology or station modules
- Provide narrative context and story progression

SURVIVOR MANAGEMENT:
- Station capacity limits number of survivors
- Assignment to specific station modules
- Development of skills and relationships over time
- Potential conflicts or collaborative opportunities

3.5 STATION HUB
------------------------
NAVIGATION:
- Map-style layout showing available rooms
- Visual novel-style interaction within each room
- No free-roaming exploration within station

CORE MODULES:
- Shipyard: Ship upgrades and customization
- Drone Bay: Drone management, repair, and upgrades
- Quarters: Survivor housing and interaction
- Hydroponics: Food and medicine production
- Scanning Array: Mission intel and sector influence
- Salvage Bay: Resource processing and crafting
- Archive Vault: Research and story progression

MODULE INTERACTIONS:
- Modules affect each other's capabilities
- Module upgrades impact overall station functionality
- Survivor assignments affect module efficiency
- Resource allocation decisions between modules
- Most modules need to be built/repaired before they can be used

3.6 PROGRESSION & UPGRADES
------------------------
TECH PROGRESSION:
- Freeform upgrade paths with some dependencies
- Tiered technology advancement (basic upgrades required for advanced)
- Ship, drone and station upgrades available
- Specialized tech paths for different playstyles

RESOURCE MANAGEMENT:
- Various resource types with different applications
- Strategic decisions between ship and station upgrades
- Resource scarcity driving mission selection
- Crafting system for converting resources

DEATH MECHANICS:
- Resource loss on mission failure
- Difficulty and drone protection affects loss severity
- Hard runs risk total resource loss
- Easy runs or protective drones reduce resource loss

ENDGAME:
- Defined endpoint when station is fully restored
- Progressive narrative culmination
- Achievement system for varied playstyles
- New Game+ potential for future development

================================================================
4. TECHNICAL IMPLEMENTATION
================================================================

ENGINE APPROACH:
- Custom-built system without commercial engine
- Focus on efficient top-down physics and rendering
- Streamlined implementation of visual novel elements
- Modular code design for system expansion

TECHNICAL ARCHITECTURE:
- Core physics system for ship movement (asteroids-style)
- Entity component system for game objects
- Procedural generation algorithms for missions and maps
- AI systems for drones and enemies
- Persistent data management for progression
- Resource management and economy balancing
- Visual novel framework for station interactions

DEVELOPMENT PRIORITIES:
- Core ship movement and combat first
- Basic procedural generation second
- Station interface and upgrade systems third
- Narrative and character development elements last

VISUAL IMPLEMENTATION:
- Consistent anime/drawn art style
- Clear UI distinction between modes
- Efficient asset management for varied content
- Cohesive visual language throughout

================================================================
5. DEVELOPMENT ROADMAP
================================================================

PHASE 1: MINIMUM VIABLE PRODUCT
- Ship controls and basic combat
- Simple procedural map generation
- Core resource collection
- Basic station interface (menu-driven)
- Ship upgrade pathway
- 2 drone types
- Single survivor character

PHASE 2: CORE SYSTEMS EXPANSION
- Full drone AI implementation
- Multiple mission types
- Enhanced procedural generation
- Basic survivor system with 3-5 characters
- Visual novel station interface
- Expanded upgrade options
- Death/resource loss mechanics

PHASE 3: CONTENT AND DEPTH
- Complete station module implementation
- Full drone roster with specializations
- Expanded survivor roster with unique stories
- Inter-module station interactions
- Advanced tech progression paths
- Balance tuning and economy refinement

PHASE 4: POLISH AND COMPLETION
- Narrative arc implementation
- Endgame content and objectives
- Achievement system
- Performance optimization
- Bug fixing and user experience improvements
- Preparation for potential Android port

================================================================
6. PROJECT STRUCTURE
================================================================

starbound_exile/
├── assets/
│   ├── images/
│   │   ├── ships/
│   │   ├── drones/
│   │   ├── station/
│   │   ├── ui/
│   │   └── survivors/
│   ├── audio/
│   │   ├── sfx/
│   │   └── music/
│   └── data/
│       ├── ship_upgrades.json
│       └── drone_types.json
├── docs/
│   └── GameConcept.md
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── game.py
│   │   ├── input_handler.py
│   │   └── physics.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── ship.py
│   │   ├── drones/
│   │   │   ├── __init__.py
│   │   │   ├── drone_base.py
│   │   │   ├── combat_drone.py
│   │   │   └── scanner_drone.py
│   │   ├── resources.py
│   │   └── survivors.py
│   ├── world/
│   │   ├── __init__.py
│   │   ├── procedural/
│   │   │   ├── __init__.py
│   │   │   └── map_generator.py
│   │   └── mission.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── menu.py
│   │   ├── hud.py
│   │   └── station_interface.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── helpers.py
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_physics.py
│   └── test_map_generator.py
├── .gitignore
├── README.md
├── requirements.txt
└── main.py

================================================================
END OF DOCUMENT
================================================================
