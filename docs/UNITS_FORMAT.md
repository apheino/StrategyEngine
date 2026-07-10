# Units File Format

## File Organization

Units files are stored in `resources/maps/` as `units_n.json` where `n` matches the scenario/map number.

Each scenario consists of:
- **Map file**: `resources/maps/map_n.txt` (defines terrain)
- **Units file**: `resources/maps/units_n.json` (defines starting forces)

## Format Specification

Units files use JSON format with the following structure:
```json
{
  "scenario": 1,
  "description": "Standard battle on 10x10 map",
  "teams": [
    {
      "id": 0,
      "name": "Blue",
      "description": "Player team starting at bottom",
      "units": [
        {"type": "soldier", "row": 7, "col": 3},
        {"type": "archer", "row": 8, "col": 2}
      ]
    }
  ]
}
```

### Field Definitions

**Top-level fields:**
- **scenario** (integer): Scenario number matching the map
- **description** (string): Description of the scenario
- **difficulty** (string, optional): Difficulty level (e.g., "tutorial", "easy", "hard")
- **map_size** (object, optional): Map dimensions for reference
- **teams** (array): Array of team configurations

**Team object:**
- **id** (integer): Team/player number
  - `0` = Blue team (typically bottom/left)
  - `1` = Red team (typically top/right)
  - Can support more teams (2, 3, etc.)
- **name** (string): Team display name
- **description** (string): Team description or deployment notes

**Unit object:**
- **type** (string): Type of unit to create
  - Available types: `soldier`, `archer`, `knight`, `catapult`
  - Must match a unit type with files in `resources/units/`
- **row** (integer): Grid row position (0-based, top to bottom)
- **col** (integer): Grid column position (0-based, left to right)

### Format Rules

- Position must be within map bounds
- Multiple units cannot occupy the same cell (not enforced in file, but gameplay should handle this)
- Teams array can have any number of teams
- Units array can have any number of units

## Example

```json
{
  "scenario": 1,
  "description": "Standard battle on 10x10 map",
  "teams": [
    {
      "id": 0,
      "name": "Blue",
      "description": "Player team starting at bottom",
      "units": [
        {"type": "soldier", "row": 7, "col": 3},
        {"type": "archer", "row": 8, "col": 2},
        {"type": "knight", "row": 8, "col": 5}
      ]
    },
    {
      "id": 1,
      "name": "Red",
      "description": "Enemy team starting at top",
      "units": [
        {"type": "soldier", "row": 2, "col": 3},
        {"type": "archer", "row": 1, "col": 2},
        {"type": "knight", "row": 1, "col": 5}
      ]
    }
  ]
}
```

## Current Unit Files

### units_1.json (Map 1: 10×10)
- 12 units total
- Team 0: 2 soldiers, 2 archers, 2 knights (bottom formation)
- Team 1: 2 soldiers, 2 archers, 2 knights (top formation)

### units_2.json (Map 2: 8×15 rectangular)
- 13 units total
- Team 0: 2 soldiers, 2 archers, 2 knights, 1 catapult (left side)
- Team 1: 2 soldiers, 2 archers, 2 knights (right side)

### units_3.json (Map 3: 200×100 large map)
- 39 units total
- Large-scale battle with multiple deployment zones

## Scenario Variants

The separate file structure allows multiple unit configurations per map:

```
map_1.txt               <- Same terrain
units_1.json            <- Standard mode
units_1_tutorial.json   <- Tutorial setup (fewer units)
units_1_hard.json       <- Hard mode (many enemy units)
units_1_skirmish.json   <- Balanced PvP setup
```

## Loading in Code

```python
from scenario import Scenario

# Load scenario 1 (loads map_1.txt and units_1.json)
scenario = Scenario(scenario_number=1)

# Load with custom units file
scenario = Scenario(scenario_number=1, units_file="units_1_tutorial.json")

# Access units
for unit in scenario.units:
    print(f"{unit.unit_type} at {unit.position}")

# Get unit at position
unit = scenario.get_unit_at(row=5, col=3)

# Get all units for a team
blue_team = scenario.get_units_by_team(0)
```

## Validation

When loading, the Scenario class:
- Validates positions are within map bounds
- Warns about invalid formats
- Skips malformed lines
- Continues loading valid units even if some fail

## Future Enhancements

Possible additions to unit file format:
- Custom unit stats per placement
- Starting health/mobility
- Unit facing direction
- Special equipment/items
- AI behavior hints
- Unit groups/formations
- Victory conditions
- Starting resources

Example extended format:
```
unit_type,team,row,col,health,facing,item
soldier,0,7,3,100,north,sword
archer,0,8,2,80,north,longbow
```
