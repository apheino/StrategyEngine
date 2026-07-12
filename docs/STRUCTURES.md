# Structures System

## Overview

Combat Alley 2000 now supports **destructible structures** (buildings) that can be placed on maps, owned by teams, and destroyed in combat. Structures block movement when alive and become passable once destroyed.

## Features

- **Placeable**: Add structures to any scenario through the editor or JSON files
- **Destructible**: Can be attacked and destroyed by units
- **Team-Owned**: Structures can belong to specific teams or be neutral
- **Strategic**: Block movement and provide tactical objectives
- **Base Structures**: Special flag for team headquarters

## Structure Types

### Headquarters
- **Health**: 500 HP
- **Defense**: 20
- **Special**: Marked as team base (`is_base: true`)
- **Description**: Heavily fortified command center
- **Visual**: Fortress with flag

### Hangar
- **Health**: 300 HP
- **Defense**: 15
- **Special**: None
- **Description**: Vehicle storage and repair facility
- **Visual**: Industrial building with large door

### Sandbag
- **Health**: 100 HP
- **Defense**: 5
- **Special**: None
- **Description**: Light cover and defensive position
- **Visual**: Stacked sandbags

## Gameplay Mechanics

### Movement Blocking
- **Alive structures**: Cell is **unpassable** (blocks movement)
- **Destroyed structures**: Cell becomes **passable** (can walk through rubble)

### Combat
- Units can attack enemy structures (not neutral or friendly)
- Structures cannot dodge attacks (100% hit rate)
- Damage is reduced by structure's defense value
- Structures have health bars showing current HP
- Once HP reaches 0, structure is destroyed

### Team Ownership
- **Team-owned** (0, 1, 2, etc.): Colored by team, can be attacked by enemies
- **Neutral** (null/None): Gray color, cannot be attacked

## Using Structures in Editor

### Enable Structures Mode
Press **R** key to enter structures mode

### Place a Structure
1. Select structure type from left panel
2. Select team ownership (or "Neutral")
3. Left-click on map to place
4. Right-click to remove structures

### Save Scenario
Structures are automatically saved when you press **S**

### Editor Controls
```
R - Structures mode
T - Terrain mode
U - Units mode
```

## File Format

Structures are stored in the same JSON file as units (`units_N.json`):

```json
{
  "scenario": 1,
  "description": "Battle scenario",
  "teams": [ /* units */ ],
  "structures": [
    {
      "type": "headquarters",
      "row": 5,
      "col": 10,
      "team": 0
    },
    {
      "type": "sandbag",
      "row": 3,
      "col": 7,
      "team": null
    }
  ]
}
```

### Fields
- `type`: Structure type name (must match a .json file in `resources/structures/`)
- `row`: Grid row position
- `col`: Grid column position  
- `team`: Team ID (0, 1, 2...) or `null` for neutral

## Creating Custom Structures

### 1. Create JSON Definition

Create `resources/structures/my_structure.json`:
```json
{
  "max_health": 200,
  "defense": 10,
  "is_base": false,
  "description": "Custom structure description"
}
```

### 2. Create Sprite Image

Create `resources/structures/my_structure.png` (64x64 pixels recommended)

### 3. Use in Editor

The structure will automatically appear in the editor's structure list!

## Structure Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_health` | int | Maximum hit points |
| `defense` | int | Damage reduction per attack |
| `is_base` | bool | Mark as team headquarters |
| `description` | string | Text description |

## Victory Conditions

The `is_base` flag can be used for future victory conditions:
- Destroy enemy headquarters to win
- Protect your base from destruction
- Control all bases on the map

*Currently not enforced by game logic, but available for custom scenarios*

## Strategic Uses

### Blocking Terrain
Place structures to create choke points and control movement

### Defensive Positions
Sandbags provide cover that must be destroyed to advance

### Objectives
Make destroying the enemy headquarters a mission goal

### Neutral Obstacles
Use neutral structures as map features both teams must navigate

## Example Scenarios

### Fortress Assault
```json
"structures": [
  {"type": "headquarters", "row": 1, "col": 14, "team": 1},
  {"type": "hangar", "row": 3, "col": 12, "team": 1},
  {"type": "sandbag", "row": 5, "col": 10, "team": 1},
  {"type": "sandbag", "row": 5, "col": 11, "team": 1}
]
```

### Neutral Ruins
```json
"structures": [
  {"type": "hangar", "row": 5, "col": 7, "team": null},
  {"type": "sandbag", "row": 4, "col": 8, "team": null}
]
```

## Tips

- **Block key paths**: Place structures on important routes
- **Protect bases**: Surround headquarters with defensive structures
- **Mix types**: Combine strong (hangar) and light (sandbag) defenses
- **Use neutral**: Create obstacles both teams must deal with
- **Test balance**: Structures can significantly affect difficulty

## Technical Details

### Rendering Order
1. Terrain
2. Fog of war
3. Unit status indicators
4. Selection highlights
5. **Structures** ← Drawn here
6. Units
7. Projectiles

### Class: Structure

Located in `structure.py`:
- Manages health, defense, team
- Handles damage calculation
- Renders sprite and health bar
- Provides passability status

### Integration Points

**scenario.py**:
- `load_structures()`: Load from JSON
- `get_structure_at(row, col)`: Find structure at position
- `get_passability_at(row, col)`: Checks structure blocking
- `calculate_valid_attacks()`: Include structures as targets
- `draw_structures()`: Render all structures

**editor.py**:
- `MODE_STRUCTURES`: Structure placement mode
- `place_structure()`: Add structure to map
- `remove_structure()`: Delete structure
- Structure panel with type/team selection

## Future Enhancements

Possible additions:
- [ ] Structure construction during gameplay
- [ ] Repair mechanics
- [ ] Special abilities (turrets, radar)
- [ ] Resource generation
- [ ] Capturable structures (change team ownership)
- [ ] Structure line of sight blocking
- [ ] Garrison units inside structures

---

**See Also:**
- [EDITOR.md](EDITOR.md) - Editor usage guide
- [GAMEPLAY.md](GAMEPLAY.md) - Game mechanics
- [NEW_GAME_GUIDE.md](NEW_GAME_GUIDE.md) - Creating custom content
