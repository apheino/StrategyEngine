# Movement and Turn System

## Team System

The game uses a two-team system:
- **Team 0**: Player-controlled units (Blue team)
- **Team 1**: Enemy AI-controlled units (Red team)

## Player Turn System

### Unit Selection

1. **Click on a player unit** (team 0) to select it
   - Selected unit is highlighted with a **yellow border**
   - Valid movement destinations are shown as **green cells**
   - Unit info is displayed at the bottom of the screen

2. **Click on a green cell** to move the selected unit
   - Unit will smoothly animate movement to the destination
   - Movement speed: 2 cells per second
   - Movement uses "move" animation, then switches to "idle" when complete
   - **Mobility is deducted** based on distance moved
   - **Unit remains active** if mobility points remain (can move again)
   - Unit becomes inactive when mobility reaches 0

3. **Click another unit** or empty space to deselect

4. **Hover over any unit** to see their information
   - A tooltip appears showing unit stats
   - Displays: unit type, team, health, attack, defense, mobility, range
   - Works for both player and enemy units

### Movement Rules

**Movement Range:**
- Each unit has a **mobility** value (default: 3 cells)
- Units can move up to their mobility value using pathfinding
- **Mobility is consumed** based on distance moved (1 point per cell)
- **Multiple moves allowed**: Units can move again if mobility remains
- Movement pathfinding uses BFS to find routes around obstacles
- Units cannot move through blocked terrain (mountains, water)

**Example:** Soldier with 3 mobility can:
- Move 1 space, then 2 more spaces (3 total)
- Move 2 spaces, then 1 more space (3 total)  
- Move 3 spaces in one move
- Any combination totaling ≤3 spaces

**Terrain Effects:**
- **Easy Passable** (grassland, etc.): Normal movement
- **Slow Passable**: Mobility is **halved** when starting from this terrain type
  - If unit has 3 mobility and starts on slow terrain, effective mobility = 1
- **Blocked** (not passable): Cannot enter or path through

**Movement Restrictions:**
- Cannot move to cells occupied by other units
- Cannot move to blocked terrain
- Cannot move through blocked terrain (proper pathfinding enforced)
- **Can move multiple times** per turn until mobility exhausted
- Can only select and move units on player turn (team 0)

### Turn Management

**Ending Your Turn:**
- Press **SPACE** to end the player turn
- All player units will have their mobility and active status reset next turn

**Turn Flow:**
1. Player Turn (team 0)
   - Select and move your units
   - Press SPACE when done
2. Enemy Turn (team 1)
   - Enemy AI takes actions (currently placeholder)
   - Automatically ends and returns to player turn
3. Repeat

## Enemy AI (Placeholder)

Currently, enemy units have a placeholder AI system:
- Enemy units do not take actions
- Turn automatically ends after brief pause
- Ready for future AI implementation

**Future AI Features:**
- Path finding and movement
- Target selection
- Attack decision making
- Strategic positioning

## Controls Summary

### Mouse Controls
- **Left-click unit**: Select player unit
- **Left-click green cell**: Move selected unit
- **Left-click + drag**: Pan map view (works anywhere on the grid)
  - Distinguishes between clicks (for selection) and drags (for panning)
  - Small movements count as clicks, larger movements as drags
- **Mouse wheel up**: Zoom in (toward center of current view)
- **Mouse wheel down**: Zoom out (from center of current view)

### Keyboard Controls
- **SPACE**: End turn
- **H**: Toggle damage numbers display (shows damage dealt on screen)
- **G**: Toggle grid lines
- **P**: Toggle fog of war visibility (75% vs 100% opacity)
- **ESC**: Quit game

## Unit Status

Each unit tracks:
- **is_active**: Can the unit act this turn?
  - Set to False when mobility reaches 0
  - Reset to True at start of each turn
- **mobility**: Current movement points remaining
  - Decreases with each move based on distance traveled
  - Unit can move multiple times until mobility = 0
  - Reset to max_mobility at start of each turn
- **pending_mobility_cost**: Mobility to deduct when movement animation completes
  - Stored during movement animation
  - Applied when unit reaches destination

## Screen Indicators

### Visual Feedback
- **Health bars**: Displayed above each unit
  - Green bar (>60% health): Healthy unit
  - Yellow bar (30-60% health): Moderately damaged
  - Red bar (<30% health): Critically wounded
  - Scales with zoom level
  - Shows exact health percentage
- **Yellow border**: Selected unit
- **Green cells with border**: Valid movement destinations
- **Unit hover tooltip**: Shows unit stats when hovering
  - Black background with red border
  - Displays all unit attributes
  - Works for both player and enemy units
  - Shows "(Player)" or "(Enemy)" team identifier
  - Follows mouse cursor
- **Turn indicator** (top-left): Shows current turn (Player/Enemy)
- **Unit info** (bottom): Shows selected unit details
- **Instructions** (left side): Quick reference for controls

### UI Information
- Current turn (Player/Enemy) with color coding
  - Green = Player turn
  - Red = Enemy turn
- Selected unit stats: type, health, mobility
- FPS counter (top-right)

## Fog of War System

### Vision and Visibility

**Vision Range:**
- Each unit has a **vision_range** attribute (4-7 cells)
- Creates a **circular visible area** using Euclidean distance
- Units can only see and attack enemies within their vision range

**Unit Vision Ranges:**
- **Archer**: 7 cells (best vision - trained scouts)
- **Catapult**: 6 cells (elevated position)
- **Soldier**: 5 cells (standard infantry vision)
- **Knight**: 4 cells (restricted by heavy armor/helmet)

**Visibility Mechanics:**
- **Unexplored areas**: Covered with light gray fog (100% opacity)
- **Explored terrain**: Remains visible permanently once seen
- **Enemy units**: Only visible when in current vision range
- **Vision updates**: Automatically recalculates after unit movement

**Vision Visualization:**
- Select a unit to see **light blue overlay** showing vision range
- Circular pattern shows exactly which cells the unit can see
- Vision display updates as you select different units

**Toggle Fog Visibility:**
- Press **P** to toggle between:
  - Normal: 100% opacity fog (unexplored areas completely hidden)
  - Show all: 75% opacity fog (can see through for planning)

### Tactical Implications

- **Archers are scouts**: Use high vision range to explore map
- **Knights need support**: Low vision makes them vulnerable to ambush
- **Exploration matters**: Move units to reveal enemy positions
- **Vision controls targeting**: Cannot attack what you can't see
- **Positioning is key**: Stay in range to maintain vision on enemies

## Example Gameplay

## Example Gameplay

1. Start game - Player turn begins with fog of war active
2. Click on your soldier unit
   - Yellow border appears
   - Green cells show where you can move (within remaining mobility)
   - Light blue overlay shows vision range
3. Click on a green cell 1 space away
   - Unit moves with animation
   - Mobility reduced by 1 (e.g., 3 → 2)
   - Unit remains selected (can move again)
   - Fog of war updates, revealing new terrain
4. Move the same unit again if mobility remains
   - Valid moves recalculated based on remaining mobility
   - Continue until mobility exhausted
5. Select and move other units as desired
   - Watch fog clear as units explore
   - Enemy units appear when in vision range
6. Press SPACE to end turn
7. Enemy turn executes (currently instant)
8. Player turn begins again with all units' mobility reset

## Tips

- **Use mobility efficiently** - partial moves let you reposition tactically
- **Vision range matters** - units reveal fog of war in circular area
- **Archers for scouting** - 7 vision range reveals most territory
- Check terrain passability - slow terrain reduces mobility
- Remember starting position affects movement range
- Use zoom and pan to see the full battlefield
- Toggle grid (G) for cleaner view
- Press P to see the full map temporarily

## Future Enhancements

Planned features:
- **Enemy AI behavior** - Intelligent movement and combat decisions
- **Multiple actions per turn** - Move then attack in same turn
- **Special abilities** - Unit-specific powers and skills
- **Victory/defeat conditions** - Win/lose scenarios
- **Campaign mode** - Story-driven multi-scenario campaigns
- **Unit experience/upgrades** - Level up system
- **More unit types** - Cavalry, siege weapons, magic users
- **Terrain effects on combat** - High ground bonuses, cover system
