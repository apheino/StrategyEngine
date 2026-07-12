# Strategy Game Editor

A graphical tool for creating and editing maps, unit placements, and scenarios for the strategy game engine. This is a standalone editor that saves to the game's resource directories.

## Features

- **Visual Map Editor**: Paint terrain tiles with mouse clicks
- **Zoom and Pan**: Handle maps of any size (from 15x10 to 200x100+) with mouse wheel zoom and pan
- **Scenario Selector**: Easy navigation between scenarios with visual indicators
- **Auto-Load**: Scenarios load automatically when switching scenario numbers
- **Unit Placement**: Place and configure units with team assignment
- **Unit Type Creator**: Create new unit types directly in the editor
- **Unit Type Editor**: Edit existing units including projectile sprites
- **Terrain Type Creator**: Create custom terrain types with icons and passability
- **Terrain Type Editor**: Edit existing terrain definitions
- **Dynamic Loading**: Automatically loads all unit and terrain types
- **Terrain Mobility Display**: Shows passability info (Easy/Slow/Blocked) for each terrain
- **Scenario Management**: Save and load complete scenarios
- **Intuitive UI**: Three-panel interface with toolbar and status bar
- **Grid Resizing**: Dynamic grid size adjustment
- **Team Integration**: Uses game configuration for team colors and names

## Running the Editor

```bash
python editor.py
```

The editor will open in a new window with a visual interface.

## Interface Layout

```
┌──────────────────────────────────────────────────────────┐
│  TOOLBAR: Title, Mode, Scenario Number                   │
├────────┬──────────────────────────────────┬──────────────┤
│        │                                  │              │
│ LEFT   │        EDITING GRID             │    RIGHT     │
│ PANEL  │     (Click to edit)             │    PANEL     │
│        │                                  │              │
│ Tool   │   15x10 cells                   │  Controls    │
│ Select │   Terrain/Units shown           │  & Info      │
│        │                                  │              │
├────────┴──────────────────────────────────┴──────────────┤
│  STATUS BAR: Current selection and mode                  │
└──────────────────────────────────────────────────────────┘
```

### Left Panel
- **Terrain Mode**: Shows terrain types with color swatches
- **Units Mode**: Shows unit types and team selection
- Click to select what to place on the grid

### Center Grid
- Visual representation of your map
- **Left-click**: Place selected terrain/unit
- **Right-click**: Erase terrain/unit
- Terrain shown with colors
- Units shown as circles with team colors

### Right Panel
- **Controls reference**: Quick keyboard shortcuts
- **Statistics**: Grid size, unit count, scenario number

### Status Bar
- Shows currently selected terrain type or unit + team

## Controls

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **T** | Switch to Terrain editing mode |
| **U** | Switch to Units placement mode |
| **S** | Save current scenario |
| **L** | Load scenario (manual, auto-loads on scenario change) |
| **N** | New/Clear scenario |
| **[** | Previous scenario number |
| **]** | Next scenario number |
| **↑ ↓ ← →** | Pan camera (arrow keys) |
| **R** | Reset camera (auto-fit and center map) |
| **+** or **=** | Increase grid size |
| **-** | Decrease grid size |
| **1-6** | Quick-select terrain types |
| **Q** or **ESC** | Quit editor |

### Mouse Controls

| Action | Effect |
|--------|--------|
| **Left-click** on panel | Select terrain/unit type or click Edit button |
| **Left-click** on grid | Place selected item (zoom-aware) |
| **Right-click** on grid | Erase terrain/unit (zoom-aware) |
| **Mouse wheel** | Zoom in (scroll up) or zoom out (scroll down) |
| **Middle-click + drag** | Pan camera around map |
| **Click < >** in toolbar | Navigate between scenarios |

### Zoom and Pan (For Large Maps)

**Zoom:**
- **Mouse wheel up**: Zoom in (10%-300%)
- **Mouse wheel down**: Zoom out
- **Zoom indicator**: Shows current zoom percentage in bottom-left corner

**Pan:**
- **Middle mouse button + drag**: Pan camera
- **Arrow keys**: Pan 50 pixels in direction
- **R key**: Reset camera (auto-fit and center map)

**Auto-Fit:**
- When loading scenarios, camera automatically adjusts to show entire map
- Small maps (15x10): 100% zoom
- Large maps (200x100): ~11% zoom, entire map visible

### Scenario Selector

**Toolbar Controls:**
- **< button**: Previous scenario (or press **[** key)
- **> button**: Next scenario (or press **]** key)
- **Status**: Shows **(exists)** or **(new)** next to scenario number

**Auto-Load:**
- When you switch to an existing scenario, it loads automatically
- When you switch to a new scenario number, map and units clear for fresh start
- No need to press **L** anymore!

## Editing Workflow

### Working with Multiple Scenarios

The editor supports managing up to 99 scenarios:

1. **Navigate**: Use **< >** buttons or **[ ]** keys to change scenario number
2. **Auto-Load**: Existing scenarios load automatically when selected
3. **Edit**: Make changes to map and units
4. **Save**: Press **S** to save (overwrites existing or creates new)
5. **Visual Feedback**: 
   - **(exists)** in yellow: Scenario files found
   - **(new)** in green: Scenario doesn't exist yet

**Example Workflow:**
```
Start editor → Scenario 1 (auto-loaded)
Press ] → Scenario 2 (auto-loaded if exists)
Edit map...
Press S → Saves Scenario 2
Press ] → Scenario 3 (auto-loaded)
Press ] → Scenario 4 (new, blank map)
Build new map...
Press S → Saves new Scenario 4
```

### Creating a New Map

1. **Start the editor**: `python editor.py`
2. **Select scenario number**: Use **< >** or **[ ]** to choose unused number
3. **Set grid size**: Press **+** or **-** to adjust dimensions (5x5 to 50x50)
4. **Paint terrain**:
   - Press **T** for terrain mode
   - Click terrain type in left panel
   - Click on grid to paint
   - Use **1-6** keys for quick terrain selection
   - For large maps: Use **mouse wheel** to zoom, **middle-drag** to pan
5. **Place units**:
   - Press **U** for units mode
   - Select unit type (soldier, archer, knight, etc.)
   - Select team (Blue Alliance, Red Empire)
   - Click on grid to place
   - Zoom in for precise placement on large maps
6. **Save**: Press **S** to save scenario

### Editing an Existing Scenario

1. Start the editor
2. Use **[ ]** keys or click **< >** to navigate to scenario number
3. Scenario loads automatically
4. **Navigate large maps**: 
   - Zoom with mouse wheel
   - Pan with middle-drag or arrow keys
   - Press **R** to reset view
5. Edit map and units as needed
6. Press **S** to save changes

### Editing Large Maps (200x100)

For large scenarios like Scenario 3:

1. Load scenario (auto-loads at ~11% zoom showing full map)
2. **Zoom in** to area you want to edit (scroll wheel)
3. **Pan** to specific location (middle-drag or arrows)
4. Make edits (clicks are zoom-aware)
5. **Zoom out** or press **R** to see full map
6. Save when done

## Terrain Types

The editor automatically loads terrain types from `resources/terrains.json`.

### Built-in Terrains

Each terrain type displays its mobility characteristics in the editor.

| # | Name | Color | Mobility | Icon | Description |
|---|------|-------|----------|------|-------------|
| 0 | Grass | Green | **Easy** | grass | Standard terrain, no movement penalty |
| 1 | Water | Blue | **Blocked** | water | Impassable, units cannot enter |
| 2 | Mountain | Brown | **Blocked** | mountain | Impassable, blocks line of sight |
| 3 | Forest | Dark Green | **Slow** | forest | Slows movement, reduces visibility |
| 4 | Sand | Tan | **Easy** | sand | Desert terrain, no penalty |
| 5 | Road | Gray | **Easy** | road | Built paths, could have bonus |

**Mobility Labels:**
- **Easy**: Normal movement cost (passability = 0)
- **Slow**: Increased movement cost, usually 2x (passability = 1)
- **Blocked**: Cannot pass through (passability = 2)

### Creating Custom Terrain Types

You can create custom terrain types directly in the editor! This allows you to have multiple terrain types with the same passability level but different visuals.

**Steps to create terrain:**

1. Press `T` to enter Terrain mode (if not already)
2. Click the **"+ Create New Terrain"** button (green button below terrain list)
3. Fill out the terrain definition form:
   - **Name**: Terrain type name (e.g., "lava", "ice", "bridge")
   - **Mobility**: Click Easy/Slow/Block to set passability
   - **Color R/G/B**: RGB color values (0-255 each)
   - **Icon**: Icon identifier (for future sprite support)
4. Click **"Save Terrain"** or press Enter through all fields
5. The new terrain type is immediately available for painting!

**Form Interface:**

```
┌────────────────────────────────┐
│ Create Terrain                 │
├────────────────────────────────┤
│ Name:     [Lava__________]     │
│ Mobility: [Easy] [Slow] [Block]│
│ Color R:  [255__________]      │
│ Color G:  [100__________]      │
│ Color B:  [0____________]      │
│ Preview:  [████████████]       │  ← Live color preview
│ Icon:     [lava_________]      │
├────────────────────────────────┤
│ [Save Terrain]  [Cancel]       │
└────────────────────────────────┘
```

**Keyboard Controls:**
- **Tab** or **Enter**: Next field
- **Backspace**: Delete character
- **ESC**: Cancel creation
- **Click**: Activate specific field or select passability

**Color Preview:**
The form shows a live preview of your terrain color as you type RGB values. This helps you visualize how the terrain will look on the map.

**Example Custom Terrains:**

1. **Lava** (Blocked like water, but red):
   - Name: "lava"
   - Mobility: Block
   - Color: RGB(255, 100, 0) - bright orange/red
   - Icon: "lava"
   - Use: Volcanic areas, impassable hazard

2. **Ice** (Slow like forest, but white/blue):
   - Name: "ice"
   - Mobility: Slow
   - Color: RGB(200, 230, 255) - light blue
   - Icon: "ice"
   - Use: Frozen terrain that slows movement

3. **Bridge** (Easy like grass, but gray):
   - Name: "bridge"
   - Mobility: Easy
   - Color: RGB(180, 160, 140) - brown-gray
   - Icon: "bridge"
   - Use: Crossing over water or valleys

4. **Swamp** (Slow, dark green):
   - Name: "swamp"
   - Mobility: Slow
   - Color: RGB(60, 80, 40) - murky green
   - Icon: "swamp"
   - Use: Wetlands that hinder movement

5. **Cliff** (Blocked, light brown):
   - Name: "cliff"
   - Mobility: Block
   - Color: RGB(160, 130, 100) - tan/brown
   - Icon: "cliff"
   - Use: Different visual from mountains

**Multiple Terrains, Same Passability:**

The key feature is that you can create multiple terrain types with the same passability. For example:
- **Water** (Blocked) - blue impassable liquid
- **Lava** (Blocked) - red impassable liquid
- **Chasm** (Blocked) - dark impassable pit

All three are impassable (passability = 2), but visually distinct with different colors and icons.

**Terrain File:**

Terrain definitions are saved to `resources/terrains.json`:

```json
{
  "0": {
    "name": "Grass",
    "color": [34, 139, 34],
    "passability": 0,
    "icon": "grass"
  },
  "6": {
    "name": "Lava",
    "color": [255, 100, 0],
    "passability": 2,
    "icon": "lava"
  }
}
```

Each terrain gets a unique ID (automatically assigned). The color is stored as RGB values, and the icon field is for future sprite support.

**Note**: Map files store passability values, not terrain IDs:
- `0` = Easy passable
- `1` = Slow passable  
- `2` = Blocked

### Editing Existing Terrain Types

You can edit any existing terrain type to change its properties:

**Steps to edit terrain:**

1. Press **T** to enter Terrain mode
2. Click the **"Edit"** button next to the terrain you want to modify
3. The form opens with all values pre-filled:
   - Name, RGB colors, passability, icon all loaded
4. Modify any values you want to change
5. Press Enter through fields or click Save
6. Terrain updates immediately

**What You Can Edit:**
- **Name**: Change terrain type name
- **Color**: Adjust RGB values for different appearance
- **Passability**: Change mobility type (Easy/Slow/Blocked)
- **Icon**: Update icon identifier

**Use Cases:**
- Tweak colors for better visual contrast
- Change passability for game balance
- Fix typos in terrain names
- Adjust terrain properties without recreating

## Unit Types

The editor automatically loads all unit types from `resources/units/*.json`.

### Built-in Units
- **Soldier**: Balanced infantry
- **Archer**: Ranged attacker
- **Knight**: Heavy cavalry
- **Catapult**: Siege artillery

### Creating Custom Unit Types

You can create new unit types directly in the editor!

**Steps to create a unit:**

1. Press `U` to enter Units mode
2. Click the **"+ Create New Unit Type"** button
3. Fill out the unit definition form:
   - **Name**: Unit type name (lowercase, e.g., "wizard", "tank")
   - **Health**: Maximum hit points (e.g., 100)
   - **Attack**: Base attack power (e.g., 20)
   - **Defense**: Damage reduction (e.g., 5)
   - **Range**: Attack range in cells (1=melee, 2+=ranged)
   - **Mobility**: Maximum movement per turn (e.g., 3)
   - **Vision**: Vision range in cells (e.g., 5)
   - **Proj Sprite**: Projectile sprite name (e.g., "arrow", "fireball") or "null" for melee
4. Click **"Save Unit"** or press Enter through all fields
5. The new unit type is immediately available for placement!

**Projectile Sprite Field:**
- **For melee units** (range=1): Use "null" (no projectile)
- **For ranged units** (range≥2): Use sprite name:
  - "arrow" - Arrow projectile (archers)
  - "boulder" - Rock projectile (catapults)
  - "fireball" - Magic projectile (wizards)
  - Custom sprite names for your own projectile images

**Form Fields (All Available):**
The form shows 8 editable fields:
1. Name
2. Health (max_health)
3. Attack (attack_power)
4. Defense
5. Range (attack_range)
6. Mobility (max_mobility)
7. Vision (vision_range)
8. Proj Sprite (projectile_sprite)

**Example Custom Units:**
- **Wizard**: High attack range, low health, magic projectiles (projectile_sprite: "fireball")
- **Tank**: Very high health/defense, low mobility, melee (projectile_sprite: "null")
- **Scout**: High mobility and vision, low combat stats, melee (projectile_sprite: "null")
- **Healer**: Special unit with support abilities

The unit definition is saved to `resources/units/{name}.json` and can be used in the game immediately.

### Editing Existing Unit Types

You can edit any existing unit type to modify its stats:

**Steps to edit unit:**

1. Press **U** to enter Units mode
2. Click the **"Edit"** button next to the unit you want to modify
3. The form opens with all values pre-filled:
   - Name, health, attack, defense, range, mobility, vision, projectile sprite
4. Modify any values you want to change
5. Press Enter through fields or click Save
6. Unit updates immediately in both editor and game

**What You Can Edit:**
- **All 8 core stats**: Name, health, attack, defense, range, mobility, vision, projectile sprite
- **Name changes**: If you change the name, old file is deleted, new file created
- **Projectile sprites**: Change "null" to "arrow" to make melee unit ranged, or vice versa

**Use Cases:**
- Balance adjustments: Increase/decrease health or attack
- Range tuning: Change unit from melee to ranged or adjust range
- Projectile changes: Switch sprite for visual variety
- Fix typos: Rename units by editing name field
- Create variants: Edit and rename to create similar unit types

**Example Edit Workflow:**
```
1. Click "Edit" button next to "archer"
2. Change health from 80 to 100
3. Change projectile_sprite from "arrow" to "fireball"
4. Change name from "archer" to "fire_archer"
5. Save → Old archer.json deleted, fire_archer.json created
```

### Unit Placement

Units are placed with:
- **Type**: What kind of unit (from available types)
- **Team**: Which team controls it (uses game_config.json)
- **Position**: Grid coordinates

## File Output

The editor saves two files for each scenario:

### Map File: `resources/maps/map_N.txt`

**Format (Game-Compatible):**
```
# Map 1: 15x10
# Format: icon_id,passability (0=easy, 1=slow, 2=blocked)
#
1,0 1,0 1,0 2,2 2,2 2,2 1,0 1,0 1,0 1,0 1,0 1,0 1,0 1,0 1,0
1,0 1,0 1,0 2,2 2,2 2,2 1,0 1,0 1,0 1,0 1,0 1,0 1,0 1,0 1,0
...
```

- **Comment lines** (start with #): Map info and format description
- **Data lines**: Space-separated `icon_id,passability` pairs
  - `icon_id`: Terrain icon number (1-based)
  - `passability`: 0=easy, 1=slow, 2=blocked
- **No dimensions line**: Game infers dimensions from data

**Important**: The editor saves in the format the game expects. Older versions had a bug where they saved dimensions on the first line, causing loading issues.

### Units File: `resources/maps/units_N.json`
```json
{
  "scenario": 1,
  "description": "New scenario",
  "teams": [
    {
      "id": 0,
      "name": "Blue Alliance",
      "description": "Player-controlled forces",
      "units": [
        {"type": "soldier", "row": 5, "col": 3},
        {"type": "archer", "row": 6, "col": 4}
      ]
    },
    {
      "id": 1,
      "name": "Red Empire",
      "description": "Enemy forces",
      "units": [
        {"type": "soldier", "row": 2, "col": 10},
        {"type": "knight", "row": 3, "col": 9}
      ]
    }
  ]
}
```

## Tips and Best Practices

### Map Design

1. **Size Matters**: 
   - Small maps (10×10): Quick battles, good for testing
   - Medium maps (15×15): Standard scenarios
   - Large maps (30×30+): Epic battles, need scrolling

2. **Terrain Variety**:
   - Mix terrain types for visual interest
   - Use water/mountains as natural barriers
   - Create choke points with impassable terrain
   - Use forests for tactical positioning

3. **Balance**:
   - Place units symmetrically for fair battles
   - Give each team similar starting positions
   - Consider vision ranges when placing units

### Unit Placement

1. **Team Balance**:
   - Equal number of units per team (usually)
   - Mix unit types for tactical depth
   - Consider unit ranges and roles

2. **Starting Positions**:
   - Place teams on opposite sides
   - Leave space between teams for gameplay
   - Avoid placing units on blocked terrain

3. **Testing**:
   - Save and test in the actual game
   - Adjust based on gameplay balance
   - Iterate until it feels right

## Troubleshooting

### Game Goes Straight to Victory Screen

**Symptom**: When you play a scenario you edited, the game immediately shows victory screen without any gameplay.

**Cause**: The scenario was saved with an old version of the editor that used the wrong map format. The game misread the map dimensions, causing all units to be rejected as "out of bounds", leaving no enemy units.

**Fix**:
1. Open the editor: `python editor.py`
2. Navigate to the broken scenario using **[ ]** keys or **< >** buttons
3. Press **S** to re-save the scenario in the correct format
4. Test in the game - should work now!

**Technical Details**: 
- Old format: `"10 15"` on first line (dimensions)
- Correct format: `"1,0 2,1 3,0"` (icon,passability pairs)
- Game expects the second format only

### "Module not found" error
Make sure you're running from the strategy game directory with the virtual environment activated:
```bash
cd /path/to/strategy
source venv/bin/activate  # or venv\Scripts\activate on Windows
python editor.py
```

### Scenario doesn't load in game
- Check that both map and units files exist (`map_N.txt` and `units_N.json`)
- Verify JSON format in units file
- Ensure terrain passability values are 0, 1, or 2
- Make sure unit types match existing definitions in `resources/units/`
- Verify units are not out of map bounds

### Units not visible
- Check that team IDs match game_config.json (0 for player, 1 for enemy)
- Verify units are within grid bounds (row < height, col < width)
- Ensure unit types are spelled correctly and files exist

### Large Map Performance
- Maps up to 200x100 should work fine
- Use zoom and pan controls for comfortable editing
- Press **R** to reset view if you get lost
- The editor only renders visible cells for performance

### Can't save files
- Check that `resources/maps/` directory exists
- Verify write permissions
- Look for error messages in terminal
- Ensure scenario number is between 1-99

## Extending the Editor

### Adding New Terrain Types

**Easy Method (Recommended)**: Use the built-in terrain creator:
1. Press **T** for terrain mode
2. Click **"+ Create New Terrain"** button
3. Fill in the form and save

**Manual Method**: Edit `resources/terrains.json`:
```json
{
  "6": {
    "name": "Lava",
    "color": [255, 100, 0],
    "passability": 2,
    "icon": "lava"
  }
}
```

### Adding New Unit Types

**Easy Method (Recommended)**: Use the built-in unit creator:
1. Press **U** for units mode
2. Click **"+ Create New Unit Type"** button
3. Fill in the form including projectile sprite
4. Save

**Manual Method**: Create JSON file in `resources/units/`:
```json
{
  "max_health": 100,
  "attack_power": 20,
  "defense": 5,
  "attack_range": 1,
  "max_mobility": 3,
  "speed": 2.0,
  "projectile_sprite": null,
  "vision_range": 5
}
```

### Already Implemented Features

✓ **Scenario Number UI**: Use **< >** buttons or **[ ]** keys in toolbar  
✓ **Auto-load Scenarios**: Scenarios load automatically when switching  
✓ **Zoom and Pan**: Mouse wheel and middle-drag for large maps  
✓ **Edit Existing Items**: Edit buttons for units and terrains  
✓ **Projectile Sprites**: Configurable in unit forms

## Integration with Game

The editor is **completely separate** from the game code:

- **Standalone**: Run independently with `python editor.py`
- **No game dependency**: Editor doesn't load game engine
- **Shared formats**: Uses same file formats as game
- **Config integration**: Uses `game_config.json` for teams

Files created by the editor are immediately usable in the game. Just:
1. Create scenario in editor
2. Save it
3. Select it in game's scenario menu

## Future Enhancements

Potential additions:
- [ ] Campaign editor (link scenarios together)
- [ ] Scenario description text editor
- [ ] Scenario number selector UI
- [ ] Minimap view for large maps
- [ ] Copy/paste regions
- [ ] Undo/redo system
- [ ] Terrain brush size selection
- [ ] Fill tool for large areas
- [ ] Victory condition editor
- [ ] Preview mode (see without editing)
- [ ] Export/import scenarios
- [ ] Scenario validation checks

## Credits

Part of the Strategy Game Engine project.
Editor created as a standalone tool for map and scenario creation.
