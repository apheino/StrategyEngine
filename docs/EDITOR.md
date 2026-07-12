# Strategy Game Editor

A graphical tool for creating and editing maps, unit placements, and scenarios for the strategy game engine. This is a standalone editor that saves to the game's resource directories.

![Editor Interface](editor_screenshot.png)

## Features

- **Visual Map Editor**: Paint terrain tiles with mouse clicks
- **Unit Placement**: Place and configure units with team assignment
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
| **L** | Load scenario |
| **N** | New/Clear scenario |
| **+** or **=** | Increase grid size |
| **-** | Decrease grid size |
| **1-6** | Quick-select terrain types |
| **Q** or **ESC** | Quit editor |

### Mouse Controls

| Action | Effect |
|--------|--------|
| **Left-click** on panel | Select terrain/unit type |
| **Left-click** on grid | Place selected item |
| **Right-click** on grid | Erase terrain (resets to grass) or remove unit |

## Editing Workflow

### Creating a New Map

1. **Start the editor**: `python editor.py`
2. **Set grid size**: Press `+` or `-` to adjust dimensions
3. **Paint terrain**:
   - Press `T` for terrain mode
   - Click terrain type in left panel
   - Click on grid to paint
   - Use 1-6 keys for quick terrain selection
4. **Place units**:
   - Press `U` for units mode
   - Select unit type (soldier, archer, knight, catapult)
   - Select team (Blue Alliance, Red Empire, etc.)
   - Click on grid to place
5. **Save**: Press `S` to save scenario

### Editing an Existing Scenario

1. Start the editor
2. Press `L` to load scenario
3. Edit as needed
4. Press `S` to save changes

### Creating Multiple Scenarios

The editor uses `scenario_number` to determine which files to save/load:
- Currently editing scenario 1 (default)
- Files saved as `map_1.txt` and `units_1.json`
- To create scenario 2, 3, etc., you'll need to change `self.scenario_number` in code or add UI controls

## Terrain Types

| # | Name | Color | Passability | Description |
|---|------|-------|-------------|-------------|
| 0 | Grass | Green | Easy | Standard terrain, no movement penalty |
| 1 | Water | Blue | Blocked | Impassable, units cannot enter |
| 2 | Mountain | Brown | Blocked | Impassable, blocks line of sight |
| 3 | Forest | Dark Green | Slow | Slows movement, reduces visibility |
| 4 | Sand | Tan | Easy | Desert terrain, no penalty |
| 5 | Road | Gray | Easy | Built paths, could have bonus |

**Note**: Terrain types are stored by passability in the map file:
- `0` = Easy passable
- `1` = Slow passable
- `2` = Blocked

## Unit Types

Available units (must have sprites and JSON definitions):
- **Soldier**: Balanced infantry
- **Archer**: Ranged attacker
- **Knight**: Heavy cavalry
- **Catapult**: Siege artillery

Units are placed with:
- **Type**: What kind of unit
- **Team**: Which team controls it (uses game_config.json)
- **Position**: Grid coordinates

## File Output

The editor saves two files for each scenario:

### Map File: `resources/maps/map_N.txt`
```
10 15
0 0 0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 0 0 0 0 0 0 0 0
...
```
- First line: height width
- Following lines: passability values (0=easy, 1=slow, 2=blocked)

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

### "Module not found" error
Make sure you're running from the strategy game directory with the virtual environment activated:
```bash
cd /path/to/strategy
source venv/bin/activate  # or venv\Scripts\activate on Windows
python editor.py
```

### Scenario doesn't load in game
- Check that both map and units files exist
- Verify JSON format in units file
- Ensure terrain passability values are 0, 1, or 2
- Make sure unit types match existing definitions

### Units not visible
- Check that team IDs match game_config.json
- Verify units are within grid bounds
- Ensure unit types are spelled correctly

### Can't save files
- Check that `resources/maps/` directory exists
- Verify write permissions
- Look for error messages in terminal

## Extending the Editor

### Adding New Terrain Types

Edit `TERRAIN_TYPES` dictionary in `editor.py`:
```python
TERRAIN_TYPES = {
    6: {"name": "Lava", "color": (255, 100, 0), "passability": 2},
    # Add more...
}
```

### Adding New Unit Types

1. Create unit JSON definition in `resources/units/`
2. Add sprites for the unit
3. Add unit name to `UNIT_TYPES` list in `editor.py`

### Adding Scenario Number UI

Currently scenario number is hardcoded. To add UI control:
1. Add number input field in right panel
2. Add +/- buttons to change scenario number
3. Update status bar to show current scenario

### Adding Scenario Description Editor

Add text input for scenario description:
1. Capture text input events
2. Store in `self.scenario_description`
3. Save to units JSON file

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
