# Strategy Game - Python & Pygame

A turn-based strategy game built with Python and Pygame featuring grid-based combat, unit management, and tactical gameplay.

## Features

### Menu System & Campaign
- ✅ **Main menu** with campaign and skirmish modes
- ✅ **Story campaign system** with JSON-based narrative
- ✅ **Scenario selection** for skirmish play
- ✅ **Victory/defeat screens** with progression
- ✅ **State machine architecture** for clean state management

### Core Systems
- ✅ **Grid-based map system** with customizable terrain
- ✅ **Pathfinding system** (BFS) for realistic movement around obstacles
- ✅ **Fog of war** with vision range and tactical visibility
- ✅ **Animated units** with health-based animation variants
- ✅ **Combat system** with attack, hurt, and death animations
- ✅ **Projectile system** for ranged attacks
- ✅ **Smooth movement animation** with configurable speed and rotation
- ✅ **Health bars** showing unit status with color coding
- ✅ **Turn-based gameplay** with player vs AI
- ✅ **Unit movement system** with multiple moves per turn
- ✅ **Unit hover tooltips** showing stats for all units
- ✅ **File-based unit attributes** for easy balancing
- ✅ **Scenario management** with separate map and unit files
- ✅ **Interactive controls** with mouse and keyboard input

### Game Mechanics
- **Player Units** (Team 0) - Full control with point-and-click movement and attacks
- **Enemy Units** (Team 1) - AI placeholder ready for implementation
- **Fog of War**:
  - **Vision range**: Each unit type has different vision (4-7 cells)
  - **Circular vision**: Uses Euclidean distance for realistic visibility
  - **Persistent exploration**: Terrain stays visible once seen
  - **Enemy visibility**: Only visible when in current vision range
  - **Vision visualization**: Light blue overlay shows selected unit's vision
  - **Toggle visibility**: Press P to see full map at 75% opacity
- **Movement System**:
  - **Multiple moves per turn**: Units can move multiple times until mobility exhausted
  - **Mobility consumption**: Each move deducts mobility based on distance
  - **Partial moves**: Move 1-2 spaces and still have moves remaining
  - **Auto-reselection**: Unit stays selected if mobility remains
- **Combat System**:
  - Attack system with range checking (melee and ranged)
  - **Line of sight**: Direct fire requires clear LOS, indirect fire can shoot over obstacles
  - **Hit chance probability**: Attacks can miss based on unit accuracy (75%-98%)
  - **Damage variance**: Gaussian distribution for realistic damage variation
  - **Health degradation**: 
    - Mobility decreases for all units
    - Attack power decreases for melee units
    - Projectile count decreases for ranged units (fewer arrows but same power each)
  - **Multi-projectile attacks**: Units can fire multiple projectiles (e.g., archer volleys)
  - Damage formula: max(1, attacker.effective_attack_power - defense)
  - Projectiles for ranged attacks (arrows, spears, magic bolts)
  - **Damage display**: Toggle with H key to see damage numbers on screen
  - Health-based animation variants (100%, 50%, 25% health)
  - Hurt animation on taking damage
  - Death animation when health reaches 0
- **Terrain Types**:
  - **Sand/Shoreline** (icon_1) - Easy passable, normal movement
  - **Grassland** (icon_2) - Easy passable, normal movement
  - **Swamp/Rough** (icon_3) - Slow passable, halved mobility when starting from
  - **Mountain/Water** (icon_4) - Blocked, impassable
- **Unit Attributes**: Health, Attack, Defense, Mobility, Range, Vision Range, Projectile Speed
- **Unit Types**: 
  - **Soldier** (Melee) - 100 HP, 22 Attack, 6 Defense, Range 1, Mobility 3, Vision 5, 95% hit chance
  - **Archer** (Ranged) - 80 HP, 12 Attack, 3 Defense, Range 3, Mobility 5, Vision 7, 75% hit chance, 3 projectiles
  - **Knight** (Heavy) - 150 HP, 30 Attack, 12 Defense, Range 1, Mobility 2, Vision 4, 98% hit chance

### Visual Features
- **Camera Controls**: Pan with drag, zoom with mouse wheel toward viewport center
- **Unit Animations**:
  - Idle, move, and attack animations with health-based variants
  - Smooth interpolated movement between cells
  - Unit rotation to face movement direction
  - Horizontal flipping for leftward movement
- **Combat Visuals**:
  - Attack animations trigger on attack
  - Projectile flight with rotation
  - Hurt animation (red flash) when taking damage
  - Death animation plays fully before unit removal
- **UI Elements**:
  - Color-coded health bars (green >60%, yellow 30-60%, red <30%)
  - Selection highlights (yellow border)
  - Valid move indicators (green overlay)
  - Attack target indicators (red overlay)
  - Vision range visualization (light blue overlay for selected unit)
  - Light gray fog of war on unexplored areas
  - Unit information tooltips on hover (blue=player, red=enemy)
  - Turn indicator with color coding
  - FPS counter
- **Display Options**:
  - Frameless window mode
  - Toggleable grid lines

### Available Scenarios
- **Scenario 1: The First Battle** - 10x10 small map, 12 units, tutorial-friendly
- **Scenario 2: The Narrow Valley** - 8x15 rectangular map, 13 units, variety testing
- **Scenario 3: The Great Plains Battle** - 200x100 large battle map, 39 units, varied terrain

In Campaign mode, scenarios are played in order with story context.
In Skirmish mode, any scenario can be selected directly.

## Installation

### Prerequisites
- Python 3.12+
- Virtual environment support

### Setup

1. Clone or download the project

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install pygame numpy
```

## Running the Game

```bash
python main.py
```

### Game Modes

**Campaign Mode:**
- Story-driven progression through all scenarios
- Narrative context for each battle
- Automatic advancement to next scenario on victory
- Play scenarios 1 → 2 → 3 in order

**Skirmish Mode:**
- Select any scenario to play
- No story context, pure tactical gameplay
- Ideal for practice or testing strategies

### Main Menu Navigation
- **Arrow Keys**: Navigate menu options
- **ENTER**: Select menu option
- **ESC**: Quit game or return to main menu

## Controls

### Mouse
- **Left-click**: Select unit / Move to destination / Attack enemy
- **Left-click + drag**: Pan the map (works anywhere on grid)
- **Mouse wheel**: Zoom in/out (zooms toward center of current view)
- **Hover**: View unit information tooltip

### Keyboard
- **SPACE**: End turn
- **G**: Toggle grid lines
- **H**: Toggle damage numbers display
- **P**: Toggle fog of war visibility (75% vs 100% opacity)
- **ESC**: Quit game

### Gameplay
1. **Main Menu**: Choose "New Campaign" or "Skirmish"
   - Campaign: Start story mode from scenario 1
   - Skirmish: Select any scenario to play
2. **Story Screen** (Campaign only): Read scenario introduction
   - Press ENTER to begin battle
3. **Select a unit**: Click on one of your units (player team, blue tooltip border)
4. **Move**: Click on a green highlighted cell to move there
   - Unit will move and deduct mobility based on distance
   - If mobility remains, unit stays selected and can move again
5. **Attack**: Click on a red highlighted enemy to attack (if in vision range)
6. **End turn**: Press SPACE when done to let enemy take their turn
7. **Vision**: Notice fog of war clearing as units move - only revealed areas visible
8. **Victory/Defeat**: Automatic detection when all units of one side are eliminated
   - Victory: Continue campaign, replay, or return to menu
   - Defeat: Retry scenario or return to menu

See [docs/GAMEPLAY.md](docs/GAMEPLAY.md) for detailed gameplay instructions.

## Project Structure

```
strategy/
├── main.py                 # Main game loop, state machine, and menu system
├── scenario.py             # Scenario management (map + units + game logic)
├── grid.py                 # Grid rendering and map management
├── unit.py                 # Unit class with animations and attributes
├── projectile.py           # Projectile class for ranged attacks
├── constants.py            # Game constants (colors, dimensions)
├── requirements.txt        # Python dependencies
│
├── resources/
│   ├── icons/             # Terrain tile icons (64x64 PNG)
│   │   ├── icon_1.png    # Sand/Shoreline (passable)
│   │   ├── icon_2.png    # Grassland (passable)
│   │   ├── icon_3.png    # Swamp/Rough terrain (slow)
│   │   └── icon_4.png    # Mountain/Water (blocked)
│   │
│   ├── stories/           # Campaign story files (JSON)
│   │   ├── scenario_1.json   # Story for scenario 1
│   │   ├── scenario_2.json   # Story for scenario 2
│   │   └── scenario_3.json   # Story for scenario 3
│   │
│   ├── maps/              # Map and unit configuration files (JSON)
│   │   ├── map_1.txt     # 10x10 small map
│   │   ├── map_2.txt     # 8x15 rectangular map
│   │   ├── map_3.txt     # 200x100 large battle map
│   │   ├── units_1.json  # Scenario 1 unit placement
│   │   ├── units_2.json  # Scenario 2 unit placement
│   │   ├── units_3.json  # Scenario 3 unit placement
│   │   └── units_1_tutorial.json  # Tutorial setup
│   │
│   ├── projectiles/       # Projectile sprite animations
│   │
│   └── units/             # Unit animations and attributes (JSON)
│       ├── soldier.json  # Soldier stats
│       ├── archer.json   # Archer stats
│       ├── knight.json   # Knight stats
│       ├── catapult.json # Catapult stats
│       ├── soldier_*.png # Soldier animations
│       ├── archer_*.png  # Archer animations
│       ├── knight_*.png  # Knight animations
│       └── catapult_*.png # Catapult animations
│
├── docs/                  # Documentation
│   ├── README.md         # Documentation index
│   ├── GAMEPLAY.md       # Gameplay instructions
│   ├── UNIT_SYSTEM.md    # Unit class documentation
│   ├── MAP_FORMAT.md     # Map file format
│   ├── UNITS_FORMAT.md   # Units file format
│   └── NEW_FEATURES.md   # Feature changelog
│
├── tests/                 # Test suite
│   ├── README.md         # Test documentation
│   ├── test_unit.py      # Unit class tests
│   ├── test_scenario.py  # Scenario loading tests
│   ├── test_movement.py  # Movement system tests
│   ├── test_unit_attributes.py  # Attribute loading tests
│   ├── test_health_bars.py  # Health bar tests
│   └── ...               # Additional test files
│
├── scripts/               # Utility scripts
│   ├── README.md         # Scripts documentation
│   ├── create_icons.py   # Generate terrain icons
│   ├── create_unit_animations.py  # Generate unit animations
│   ├── demo_units.py     # Unit demo
│   └── demo_scenario_variants.py  # Scenario demo
│
└── README.md             # This file
```

## File Formats

### Map Files (map_n.txt)
Define terrain with icon references and passability:
```
# Format: icon_id,passability
# 0=easy, 1=slow, 2=blocked
1,0 1,0 2,0
1,0 2,0 1,0
```
See [docs/MAP_FORMAT.md](docs/MAP_FORMAT.md)

### Units Files (units_n.txt)
Define unit placement:
```
# Format: unit_type,team,row,col
soldier,0,7,3
archer,1,2,5
knight,0,8,4
```
See [docs/UNITS_FORMAT.md](docs/UNITS_FORMAT.md)

## Unit Types

### Soldier (Blue)
- Balanced melee unit
- Attack: 20, Defense: 5
- Mobility: 3, Range: 1

### Archer (Green)
- Ranged unit
- Attack: 20, Defense: 5
- Mobility: 3, Range: 1

### Knight (Purple)
- Heavy unit
- Attack: 20, Defense: 5
- Mobility: 3, Range: 1

*Note: All units currently have identical stats. Differentiation is planned for future updates.*

## Development

### Running Tests

```bash
# Test scenario loading
python test_scenario.py

# Test movement system
python test_movement.py

# Test unit class
python test_unit.py

# Test grid sizing
python test_grid_size.py
```

### Creating New Content

**Generate placeholder icons:**
```bash
python create_icons.py
```

**Generate placeholder unit animations:**
```bash
python create_unit_animations.py
```

**Create new scenario:**
1. Create `resources/maps/map_3.txt` (terrain)
2. Create `resources/maps/units_3.txt` (unit placement)
3. Load with: `Scenario(scenario_number=3)`

## Roadmap

### Planned Features
- [ ] Combat system with attack animations
- [ ] Enemy AI implementation
- [ ] Unit health bars
- [ ] Multiple actions per turn (move + attack)
- [ ] Special abilities per unit type
- [ ] Unit stat differentiation
- [ ] Victory/defeat conditions
- [ ] Campaign mode
- [ ] Save/load game state
- [ ] Sound effects and music
- [ ] Menu system
- [ ] Multiplayer support

### Known Issues
- Enemy AI is placeholder only
- All unit types have identical stats
- No attack/combat implementation yet
- Units can only perform one action per turn

## Technical Details

- **Engine**: Pygame 2.6.1
- **Python**: 3.12.3
- **Grid System**: Dynamic sizing based on map files
- **Animation**: Sprite-based with configurable frame rates
- **Rendering**: Zoom and pan with proper scaling

## License

This is a personal project for learning and experimentation.

## Credits

Built as a learning project for turn-based strategy game development with Python and Pygame.
