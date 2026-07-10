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
   - Unit becomes inactive after moving (can't move again this turn)

3. **Click another unit** or empty space to deselect

4. **Hover over any unit** to see their information
   - A tooltip appears showing unit stats
   - Displays: unit type, team, health, attack, defense, mobility, range
   - Works for both player and enemy units

### Movement Rules

**Movement Range:**
- Each unit has a **mobility** value (default: 3 cells)
- Units can move up to their mobility value using pathfinding
- Movement pathfinding uses BFS to find routes around obstacles
- Units cannot move through blocked terrain (mountains, water)

**Terrain Effects:**
- **Easy Passable** (grassland, etc.): Normal movement
- **Slow Passable**: Mobility is **halved** when starting from this terrain type
  - If unit has 3 mobility and starts on slow terrain, effective mobility = 1
- **Blocked** (not passable): Cannot enter or path through

**Movement Restrictions:**
- Cannot move to cells occupied by other units
- Cannot move to blocked terrain
- Cannot move through blocked terrain (proper pathfinding enforced)
- Can only move once per turn (unit becomes inactive after moving)
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
- **ESC**: Quit game

## Unit Status

Each unit tracks:
- **is_active**: Can the unit act this turn?
  - Set to False after moving
  - Reset to True at start of each turn
- **mobility**: Current movement points
  - Decreases based on actions (currently unused, reserved for future)
  - Reset to max_mobility at start of each turn

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

## Example Gameplay

1. Start game - Player turn begins
2. Click on your soldier unit
   - Yellow border appears
   - Green cells show where you can move
3. Click on a green cell
   - Unit moves with animation
   - Unit becomes inactive
   - Selection clears
4. Select and move other units as desired
5. Press SPACE to end turn
6. Enemy turn executes (currently instant)
7. Player turn begins again with all units active

## Tips

- Plan your moves carefully - units can only move once per turn
- Check terrain passability - slow terrain reduces mobility
- Remember starting position affects movement range
- Use zoom and pan to see the full battlefield
- Toggle grid (G) for cleaner view

## Future Enhancements

Planned features:
- Attack system (units can attack adjacent enemies)
- Unit health bars
- Combat animations
- Enemy AI behavior
- Multiple actions per turn (move + attack)
- Special abilities per unit type
- Victory/defeat conditions
- Campaign mode with multiple scenarios
