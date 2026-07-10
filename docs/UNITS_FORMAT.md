# Units File Format

## File Organization

Units files are stored in `resources/maps/` as `units_n.txt` where `n` matches the scenario/map number.

Each scenario consists of:
- **Map file**: `resources/maps/map_n.txt` (defines terrain)
- **Units file**: `resources/maps/units_n.txt` (defines starting forces)

## Format Specification

Each line defines one unit placement:
```
unit_type,team,row,col
```

### Field Definitions

- **unit_type** (string): Type of unit to create
  - Available types: `soldier`, `archer`, `knight`
  - Must match a unit type with animation files in `resources/units/`

- **team** (integer): Team/player number
  - `0` = Blue team (typically bottom/left)
  - `1` = Red team (typically top/right)
  - Can support more teams (2, 3, etc.)

- **row** (integer): Grid row position (0-based, top to bottom)

- **col** (integer): Grid column position (0-based, left to right)

### Format Rules

- Lines starting with `#` are comments (ignored)
- Empty lines are ignored
- Position must be within map bounds
- Multiple units cannot occupy the same cell (not enforced in file, but gameplay should handle this)
- Order doesn't matter (units load in file order)

## Example

```
# units_1.txt - Basic 10x10 map setup
# Format: unit_type,team,row,col

# Blue team (bottom)
soldier,0,7,3
archer,0,8,2
knight,0,8,5

# Red team (top)
soldier,1,2,3
archer,1,1,2
knight,1,1,5
```

## Current Unit Files

### units_1.txt (Map 1: 10×10)
- 12 units total
- Team 0: 2 soldiers, 2 archers, 2 knights (bottom formation)
- Team 1: 2 soldiers, 2 archers, 2 knights (top formation)

### units_2.txt (Map 2: 8×15 rectangular)
- 12 units total
- Team 0: 2 soldiers, 2 archers, 2 knights (left side)
- Team 1: 2 soldiers, 2 archers, 2 knights (right side)

## Scenario Variants

The separate file structure allows multiple unit configurations per map:

```
map_1.txt       <- Same terrain
units_1a.txt    <- Easy mode (few enemy units)
units_1b.txt    <- Normal mode
units_1c.txt    <- Hard mode (many enemy units)
units_1_tutorial.txt  <- Tutorial setup
units_1_skirmish.txt  <- Balanced PvP setup
```

## Loading in Code

```python
from scenario import Scenario

# Load scenario 1 (loads map_1.txt and units_1.txt)
scenario = Scenario(scenario_number=1)

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
