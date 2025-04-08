@echo off
REM setup_assets.bat - Creates folder structure for Starbound Exile assets

echo Setting up asset folder structure...

REM Base directories
if not exist assets mkdir assets
if not exist assets\images mkdir assets\images
if not exist assets\audio mkdir assets\audio
if not exist assets\data mkdir assets\data

REM Image subdirectories
if not exist assets\images\ships mkdir assets\images\ships
if not exist assets\images\drones mkdir assets\images\drones
if not exist assets\images\station mkdir assets\images\station
if not exist assets\images\station\modules mkdir assets\images\station\modules
if not exist assets\images\ui mkdir assets\images\ui
if not exist assets\images\ui\buttons mkdir assets\images\ui\buttons
if not exist assets\images\ui\hud mkdir assets\images\ui\hud
if not exist assets\images\survivors mkdir assets\images\survivors
if not exist assets\images\resources mkdir assets\images\resources
if not exist assets\images\environment mkdir assets\images\environment
if not exist assets\images\environment\obstacles mkdir assets\images\environment\obstacles
if not exist assets\images\environment\poi mkdir assets\images\environment\poi

REM Audio subdirectories
if not exist assets\audio\sfx mkdir assets\audio\sfx
if not exist assets\audio\music mkdir assets\audio\music

REM Data files
if not exist assets\data\ship_upgrades.json (
    echo ^{^} > assets\data\ship_upgrades.json
    echo Created empty ship_upgrades.json
)
if not exist assets\data\drone_types.json (
    echo ^{^} > assets\data\drone_types.json
    echo Created empty drone_types.json
)

echo Asset folder structure setup complete!