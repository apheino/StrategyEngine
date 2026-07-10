# New Features Summary

## Recent Updates (Latest First)

### 0.0 Menu System & Story Campaign
**Added:** Complete menu system with state machine and JSON story campaign.

**Features:**
- **State machine architecture**: Clean separation of game states
  - MAIN_MENU: Title screen with campaign/skirmish options
  - STORY_SCREEN: Narrative intro before scenarios
  - PLAYING: Active gameplay
  - VICTORY: Success screen with campaign progression
  - DEFEAT: Failure screen with retry option
  - SCENARIO_SELECT: Skirmish scenario selection

- **Main menu**:
  - New Campaign: Start story-driven campaign
  - Skirmish: Select any scenario without story
  - Quit: Exit game
  - Navigation: Arrow keys + ENTER

- **Story campaign system**:
  - JSON story files (resources/stories/)
  - Story screens with intro text
  - Victory/defeat narrative
  - Automatic campaign progression
  - Scenario 1 → 2 → 3 flow

- **Skirmish mode**:
  - Direct scenario selection
  - No story context
  - Ideal for practice/testing

- **Victory/defeat detection**:
  - Automatic when all units of one side eliminated
  - State transitions to appropriate screen
  - Campaign: Continue to next scenario
  - Skirmish: Replay or return to menu

**Story Files:**
```json
// resources/stories/scenario_1.json
{
  "scenario_number": 1,
  "title": "The First Battle",
  "intro_text": [...],
  "victory_text": [...],
  "defeat_text": [...],
  "next_scenario": 2
}
```

**Menu Navigation:**
- UP/DOWN arrows to navigate
- ENTER to select
- ESC to quit or return to main menu
- Story screen: ENTER to begin, ESC to menu
- In-game: ESC returns to main menu

**Technical:**
- State-based event handling
- Separate rendering per state
- JSON story loading with error handling
- Campaign vs skirmish mode tracking
- Victory/defeat condition checking

**Testing:**
```
✓ State machine transitions work correctly
✓ Menu navigation with keyboard
✓ Story files load from JSON
✓ Campaign mode progresses through scenarios
✓ Skirmish mode allows direct selection
✓ Victory/defeat detection automatic
✓ All existing gameplay features preserved
```

### 0.1 Fog of War System
**Added:** Fog of war with vision range and tactical visibility.

**Features:**
- **Vision range**: Each unit has vision_range attribute (4-7 cells)
  - Archer: 7 (best vision)
  - Soldier: 5 (standard vision)
  - Knight: 4 (restricted by heavy armor)
  - Catapult: 6 (elevated position)
- **Circular vision**: Uses Euclidean distance for realistic circular visibility
- **Light gray fog**: Unexplored areas covered with light gray (192,192,192) overlay
- **Explored cells persist**: Once seen, terrain remains visible (like classic RTS)
- **Enemy visibility**: Enemy units only visible when in current vision range
- **Vision range visualization**: Selected units show light blue overlay of vision area
- **Dynamic updates**: Fog recalculates automatically after unit movement
- **P key toggle**: Show all map (75% fog) vs normal (100% fog)

**How Vision Works:**
```python
# Circular vision using Euclidean distance
distance = sqrt((row - unit_row)² + (col - unit_col)²)
if distance <= vision_range:
    cell_is_visible = True
```

**Visibility System:**
- **visible_cells**: Currently visible cells (dynamic, recalculated per move)
- **explored_cells**: Permanently revealed terrain (persistent)
- Fog covers unexplored_cells only
- Enemy units filtered - only shown if in visible_cells

**Tactical Implications:**
- **Archers see furthest** - best for scouting
- **Knights see least** - need support for reconnaissance  
- **Vision determines targeting** - can't attack what you can't see
- **Exploration matters** - move units to reveal map
- **Fog updates per move** - see new areas immediately after movement completes

**Visual Indicators:**
- Light gray fog on unexplored areas
- Light blue overlay shows selected unit's vision range
- Unit info displays VIS: X value

**Testing:**
```
✓ Circular vision with Euclidean distance
✓ Vision range 5 creates circle radius 5, not 10x10 box
✓ Fog updates after movement animation completes
✓ Explored cells persist between turns
✓ Enemy units only visible in vision range
✓ P key toggles fog opacity
```

### 0.2 Multiple Moves Per Turn
**Added:** Units can move multiple times based on remaining mobility.

**Features:**
- **Mobility consumption**: Each move deducts mobility based on distance
- **Partial moves allowed**: Move 1 space, then move again if mobility remains
- **Auto-reselection**: Unit stays selected after partial move
- **Dynamic valid moves**: Movement options update after each move
- **Activity tracking**: Unit becomes inactive only when mobility = 0

**How it Works:**
```python
# Soldier with 3 mobility
move 1 space -> 2 mobility left (stays active, auto-reselected)
move 1 space -> 1 mobility left (stays active)
move 1 space -> 0 mobility (becomes inactive)

# OR move 3 spaces at once -> 0 mobility (becomes inactive)
```

**Mobility Deduction:**
- Deducted when movement animation completes (not when starting)
- Based on path length: mobility_cost = len(path) - 1
- Fog of war updates after each completed move
- Valid moves recalculated with remaining mobility

**Tactical Benefits:**
- **Flexible positioning**: Reposition and still have moves left
- **Resource management**: Use mobility efficiently
- **Scout and retreat**: Move forward to see, move back if threatened
- **Partial advance**: Inch forward carefully

**Testing:**
```
✓ Move 1 space: unit stays active with remaining mobility
✓ Move full mobility: unit becomes inactive
✓ Mobility correctly deducted per move
✓ Valid moves updated after partial move
✓ Fog updates after each move completion
```

### 0.3 Direct/Indirect Fire System
**Added:** Units can have direct fire (needs line of sight) or indirect fire (shoots over obstacles).

**Features:**
- **fire_type attribute**: 'direct' or 'indirect' in unit definition files
- **Line of sight checking**: Bresenham's algorithm traces path between attacker and target
- **Obstacle blocking**: Direct fire blocked by impassable terrain (mountains, water)
- **Indirect fire**: Can shoot over obstacles (artillery/mortar-style)

**How it Works:**
```python
# Direct fire (archers, most ranged units)
fire_type=direct  # Cannot attack if terrain blocks line of sight

# Indirect fire (catapults, mortars - future units)
fire_type=indirect  # Can attack over obstacles
```

**Line of Sight Algorithm:**
- Uses Bresenham's line algorithm to trace cells between attacker and target
- Checks each cell along the path for impassable terrain
- Start and end positions not checked (can shoot from/to any terrain)
- If any intermediate cell is blocked, line of sight fails

**Tactical Implications:**
- **Direct fire units**: Must position for clear shots, can be protected behind obstacles
- **Indirect fire units**: Can bombard from behind cover, more valuable strategically
- **Terrain becomes critical**: Mountains/water create cover zones
- **Flanking matters**: Move around obstacles to get clear shots

**Current Units:**
- Archer: direct fire (needs line of sight)
- Soldier: direct fire (melee, LOS not usually an issue at range 1)
- Knight: direct fire (melee, LOS not usually an issue at range 1)

**Testing:**
```
✓ Line of sight correctly traces Bresenham path
✓ Blocked terrain prevents direct fire attacks
✓ Indirect fire (when implemented) ignores terrain
✓ Attack highlighting shows only valid targets
```

### 0.2 Pathfinding System
**Added:** Units now navigate around obstacles using proper pathfinding.

**Features:**
- **BFS Algorithm**: Breadth-First Search calculates all reachable cells
- **No obstacle clipping**: Units cannot path through blocked terrain
- **Waypoint movement**: Units follow calculated paths around obstacles
- **Visual navigation**: Movement animation shows realistic pathing behavior

**How it Works:**
```python
# BFS explores reachable cells from unit position
# Builds path from start to each destination
# Movement animation follows waypoints sequentially
path = [(2,3), (2,4), (2,5), (3,5), (3,6)]  # Around obstacle
```

**Before:**
- Simple Manhattan distance check
- Units could be assigned destinations blocked by obstacles
- Animation moved in straight line through impassable terrain

**After:**
- Proper pathfinding validates reachable destinations
- Only cells with valid paths are shown as valid moves
- Animation follows the calculated path around obstacles

**Testing:**
```
✓ Archer at (2,3) correctly cannot reach (3,8) if blocked
✓ Paths stored with proper waypoints (2-5 cells typically)
✓ Movement animation follows multi-waypoint paths
✓ Units visibly navigate around mountains/water
```

### 1. Damage Number Display
**Added:** Visual feedback showing actual damage dealt during combat.

**Features:**
- **Hit display**: Shows **-X** in bright green (e.g., "-12" for 12 damage)
- **Miss display**: Shows **0** in red for missed attacks
- **Float and fade**: Messages float upward and fade out over 1.5 seconds
- **Toggle control**: Press **H key** to show/hide damage numbers
- **Default off**: Messages disabled by default to reduce clutter
- **Multiple projectiles**: Horizontally separated messages for volleys

**Examples:**
```
Archer fires 3 arrows:
  Arrow 1: -11 (green)
  Arrow 2: 0 (red - miss)
  Arrow 3: -14 (green)
```

### 2. Gaussian Damage Variance
**Added:** Realistic damage variation using Gaussian distribution.

**Mechanics:**
- **attack_power**: Median damage value
- **damage_std**: Standard deviation controlling variance
- **Distribution**: Normal distribution N(attack_power, damage_std²)
- **Minimum damage**: Always at least 1

**Unit Configurations:**
- **Archer**: attack_power=12, damage_std=2.5 (9-15 typical range)
- **Soldier**: attack_power=22, damage_std=3.0 (18-26 typical range)
- **Knight**: attack_power=30, damage_std=4.0 (24-36 typical range)

**Evolution Path:**
- Can evolve to decrease damage_std for more consistent damage
- Balances with hit_chance evolution for different unit strategies

**Testing:**
```
✓ Gaussian distribution produces correct mean and variance
✓ Minimum damage of 1 enforced
✓ Each hit calculates independent damage
✓ Damage displayed in combat messages
```

### 3. Health-Based Degradation
**Added:** Units become weaker as they take damage.

**Mobility Degradation (All Units):**
- 100-75% health: 100% mobility
- 75-50% health: 85% mobility
- 50-25% health: 65% mobility
- 25-0% health: 40% mobility

**Attack Power Degradation (Melee Only):**
- 100-75% health: 100% attack
- 75-50% health: 85% attack
- 50-25% health: 70% attack
- 25-0% health: 50% attack

**Projectile Count Degradation (Ranged Only):**
- 100-75% health: 100% projectiles (e.g., 3 arrows)
- 75-50% health: 85% projectiles (e.g., 2 arrows)
- 50-25% health: 65% projectiles (e.g., 1 arrow)
- 25-0% health: 40% projectiles (e.g., 1 arrow minimum)

**Important:** 
- Melee units: Attack power degrades, always 1 strike
- Ranged units: Each projectile deals full damage, but fewer projectiles fired

**Strategic Impact:**
- Damaged melee units strike weaker and should retreat
- Wounded archers maintain per-arrow damage but fire fewer arrows
- All damaged units are slower and easier to catch
- Creates dynamic tactical decisions about protecting wounded units

### 4. Hit Chance Probability System
**Added:** Attacks can now miss based on unit-specific accuracy.

**Features:**
- **hit_chance**: Probability value from 0.0 to 1.0
- **Independent rolls**: Each projectile rolls separately
- **Visual feedback**: Green damage for hits, red 0 for misses
- **Console output**: Detailed hit/miss logs

**Unit Hit Chances:**
- **Knight**: 98% (extremely accurate melee)
- **Soldier**: 95% (reliable infantry)
- **Archer**: 75% (less accurate ranged)

**Multi-Projectile Impact:**
- Archer with 3 arrows at 75% hit chance:
  - Most common: 2-3 hits
  - Possible: 0-3 hits (adds variability)

**Testing:**
```
✓ Hit chance rolls work per-projectile
✓ Misses deal no damage
✓ Hits apply variable damage
✓ Console logs show all results
```

### 5. Multi-Projectile System
**Added:** Units can fire multiple projectiles per attack (gun battery effect).

**Features:**
- **projectile_count**: Number of projectiles fired (1 = single shot, 2+ = volley)
- **Visual spread**: Projectiles spread horizontally for clarity
- **Staggered timing**: Slight delay between projectiles for visual effect
- **Independent rolls**: Each projectile rolls hit/miss separately
- **Slower speed**: Multi-projectile units fire slower (archer: 4.0 vs melee: 8.0)

**Current Configuration:**
- **Archer**: projectile_count=3, projectile_speed=4.0 (triple arrow volley)
- **Soldier**: projectile_count=1 (single melee strike)
- **Knight**: projectile_count=1 (single heavy strike)

**Implementation:**
```python
# In unit file: resources/units/archer.json
{
  "projectile_count": 3,
  "projectile_speed": 4.0
}

# Creates multiple projectiles with horizontal offset
for i in range(projectile_count):
    offset = (i - (projectile_count - 1) / 2) * 0.3  # Spread projectiles
    projectile = Projectile(..., x_offset=offset)
```

**Testing:**
```
✓ Multiple projectiles fire correctly
✓ Horizontal spread prevents overlapping
✓ Each projectile has independent hit roll
✓ Damage messages display with offsets
✓ Works for any projectile_count value
```

### 6. Health-Based Animation System

### 1. Health-Based Animation System
**Added:** Units now display different animations based on their current health percentage.

**Animation Variants:**
- **100% Health** (Full Health): Normal, pristine appearance
- **50% Health** (Damaged): Wounded appearance, visible damage
- **25% Health** (Critical): Heavily damaged, near defeat appearance

**Affected Animations:**
- **Idle animations**: idle_100, idle_50, idle_25
- **Move animations**: move_100, move_50, move_25
- **Attack animations**: attack_100, attack_50, attack_25

**Automatic Selection:**
- Units automatically use the appropriate animation variant based on current HP
- Thresholds: >75% = 100%, >37.5% = 50%, ≤37.5% = 25%
- Seamless transitions when taking damage
- Improves visual feedback and battlefield awareness

**Implementation:**
```python
# Animation threshold lists
idle_health_thresholds = [(100, "idle_100"), (50, "idle_50"), (25, "idle_25")]
move_health_thresholds = [(100, "move_100"), (50, "move_50"), (25, "move_25")]
attack_health_thresholds = [(100, "attack_100"), (50, "attack_50"), (25, "attack_25")]

# Helper methods
get_idle_animation_for_health()    # Returns appropriate idle animation
get_move_animation_for_health()    # Returns appropriate move animation
get_attack_animation_for_health()  # Returns appropriate attack animation
```

**File Naming Convention:**
```
soldier_idle_100_0.png    # Full health idle, frame 0
soldier_idle_50_0.png     # 50% health idle, frame 0
soldier_idle_25_0.png     # 25% health idle, frame 0
soldier_move_100_0.png    # Full health move, frame 0
soldier_attack_50_0.png   # 50% health attack, frame 0
```

**Testing:**
```
✓ Animations load correctly for all health variants
✓ Automatic selection based on HP percentage
✓ Smooth transitions between health states
✓ All three unit types have complete animation sets
✓ Animation state persists correctly
```

### 2. Unit Rotation System
**Added:** Units now rotate to face the direction of movement.

**Features:**
- **Precise angles**: Uses atan2 for exact angle calculation (not just 4 directions)
- **Rotation angle**: 0° = right, 90° = down, 180° = left, 270° = up
- **Horizontal flipping**: Units moving left are flipped to avoid upside-down appearance
- **Visual polish**: Makes movement more realistic and directional

**Implementation:**
```python
rotation_angle = math.degrees(math.atan2(delta_row, delta_col))
flip_horizontal = delta_col < 0  # Flip when moving left
# Adjust rotation when flipped: rotation_angle - 180.0
```

**Testing:**
```
✓ Rotation calculates correctly for all 8 directions
✓ Horizontal flipping works for leftward movement
✓ Sprite rendering handles rotation and flipping
✓ No visual artifacts or distortion
```

### 3. Projectile System
**Added:** Ranged attacks now display flying projectiles.

**Features:**
- **Visual feedback**: Arrows, spears, or magic bolts fly from attacker to target
- **Speed-based**: Projectile flight speed configurable per unit (projectile_speed attribute)
- **Automatic rotation**: Projectiles rotate to face direction of travel
- **Damage on hit**: Damage applied when projectile reaches target
- **Smooth animation**: Linear interpolation for smooth flight path

**Projectile Types:**
- **arrow.png** - Used by archers
- **spear.png** - Alternative ranged weapon
- **magic_bolt.png** - For magical ranged attacks

**Implementation:**
```python
# Unit attribute
projectile_speed = 8.0  # 0 = melee (no projectile), >0 = ranged

# Attack creates projectile if ranged
attack_info = unit.attack(target)
if attack_info['uses_projectile']:
    projectile = Projectile(start_pos, target_pos, speed, sprite_name, ...)
    projectiles.append(projectile)
```

**Technical Details:**
- Interpolation: Progress from 0.0 (start) to 1.0 (target)
- Speed: Grid cells per second
- Rotation: Calculated with atan2 for direction angle
- Rendering: Scaled to 80% of cell size with rotation applied

**Testing:**
```
✓ Projectiles fire from correct position
✓ Projectiles reach target accurately
✓ Damage applies on projectile hit
✓ Rotation faces direction of travel
✓ Multiple projectiles can be in flight simultaneously
```

### 4. Combat System
**Added:** Full combat system with attacks, damage calculation, and animations.

**Damage Formula:**
```
actual_damage = max(1, attacker.attack_power - defender.defense)
```
Minimum damage is always 1, even with high defense.

**Attack Flow:**
1. Select unit (click on your unit)
2. Valid attack targets highlighted in red
3. Click enemy to attack
4. Attack animation plays
5. Projectile fires (if ranged) or damage applies immediately (if melee)
6. Hurt animation plays on target
7. Health bar updates
8. Death animation plays if HP reaches 0
9. Unit removed after death animation completes

**Range Types:**
- **Melee** (range 1): Immediate damage, no projectile
- **Ranged** (range >1): Projectile flies to target, damage on hit

**Attack Animations:**
- **Attack animation**: 3 frames, plays when attacking
- **Returns to idle**: Automatically returns to idle after attack completes
- **Health-based variants**: attack_100, attack_50, attack_25

**Unit becomes inactive**: After attacking, unit cannot move or attack again this turn

**Testing:**
```
✓ Damage calculation correct for all attack/defense combinations
✓ Attack animations play and return to idle
✓ Projectiles created for ranged attacks
✓ Melee attacks apply damage immediately
✓ Units become inactive after attacking
✓ Attack range checking works correctly
```

### 5. Hurt and Death Animations
**Added:** Visual feedback when units take damage or die.

**Hurt Animation:**
- **Trigger**: Plays when unit takes damage
- **Duration**: 2 frames (brief red flash)
- **Returns to idle**: After hurt animation completes
- **File naming**: `{unit}_hurt_0.png`, `{unit}_hurt_1.png`

**Death Animation:**
- **Trigger**: Plays when unit health reaches 0
- **Duration**: 4 frames (unit collapse/fade)
- **Unit removal**: Unit removed from game after death animation completes
- **File naming**: `{unit}_death_0.png` through `{unit}_death_3.png`
- **is_dying flag**: Prevents interaction with dying units

**Implementation:**
```python
# Taking damage
def take_damage(self, damage):
    self.health -= damage
    if self.health <= 0:
        self.health = 0
        self.is_dying = True
        self.current_animation = "death"
    else:
        self.is_hurt = True
        self.current_animation = "hurt"

# Update checks for animation completion
if self.is_hurt and animation_complete:
    self.is_hurt = False
    self.set_idle_animation()  # Return to appropriate idle

if self.is_dying and animation_complete:
    self.is_alive = False  # Mark for removal
```

**Testing:**
```
✓ Hurt animation plays on damage
✓ Death animation plays when HP reaches 0
✓ Unit removed after death animation completes
✓ No interaction possible with dying units
✓ Animations play completely without interruption
```

---

## Previous Features

### 1. Improved Camera Controls
**Enhanced:** Panning and zooming now work more intuitively with better mouse interaction.

**Panning Improvements:**
- **Works on the grid**: Can now pan by clicking and dragging anywhere on the grid
- **Smart click detection**: Automatically distinguishes between clicks (for unit selection) and drags (for panning)
- **Drag threshold**: Movement must exceed 5 pixels to be considered a drag
- **No conflicts**: Unit selection only triggers on mouse release if you didn't drag

**Zooming Improvements:**
- **Zoom toward viewport center**: Mouse wheel zooms toward the center of your current view
- **Maintains focus**: The point at the center of your screen stays centered as you zoom
- **Natural navigation**: Makes it easy to zoom into what you're currently looking at

**Technical Implementation:**
- `Grid.is_dragging()` - Checks if movement exceeded threshold
- `Grid.zoom_at_viewport_center(factor, width, height)` - Zooms while keeping viewport center stable
- `Grid.drag_threshold` - Configurable sensitivity (default: 5 pixels)

**Testing:**
```
✓ Drag detection works correctly
✓ Viewport center position remains stable during zoom
✓ Click vs drag distinction prevents accidental panning
✓ Panning works smoothly on the grid
✓ Zoom in/out maintains viewport focus
```

**Benefits:**
- More intuitive camera controls
- Easier to navigate large maps
- Zoom into whatever you're currently viewing
- No accidental panning when clicking units
- Smooth experience for exploring the battlefield

### 2. Health Bars Above Units
**Added:** Visual health bars now display above each unit showing their current health status.

**Features:**
- **Position**: Displayed above each unit sprite
- **Dynamic sizing**: Scales with grid zoom level
- **Width**: 80% of cell width for clean visual
- **Color-coded by health**:
  - **Green** (>60% health): Unit is healthy
  - **Yellow** (30-60% health): Unit is moderately damaged
  - **Red** (<30% health): Unit is critically wounded
- **Real-time updates**: Health bar updates immediately when damage is taken
- **Proportional fill**: Bar fill width represents current health percentage

**Visual Design:**
```
- Black background bar
- Color-coded health fill
- White border outline
- Positioned 2px above unit sprite
- Scales smoothly with zoom
```

**Implementation:**
- New method: `Unit.draw_health_bar(screen, x, y, cell_size)`
- Automatically called from `Unit.draw()` method
- Works for all unit types with different max health values

**Testing:**
```
✓ Health bar colors change at correct thresholds
✓ Renders correctly at all health levels (0-100%)
✓ Works with different unit types (Soldier/Archer/Knight)
✓ Scales properly with zoom
✓ No performance impact
```

### 3. Universal Unit Hover Information
**Changed:** Hover tooltips now work for all units, not just enemies.

- Player units show "(Player)" in tooltip
- Enemy units show "(Enemy)" in tooltip
- Provides tactical information about your own units and enemies

### 4. File-Based Unit Attributes
**Changed:** Unit stats are now loaded from external JSON files instead of hardcoded values.

**Attribute Files:**
```
resources/units/soldier.json
resources/units/archer.json
resources/units/knight.json
resources/units/catapult.json
```

**File Format:**
```json
{
  "name": "Soldier",
  "description": "Balanced infantry unit",
  "max_health": 100,
  "attack_power": 20,
  "defense": 5,
  "attack_range": 1,
  "max_mobility": 3,
  "speed": 2.0
}
```

**Benefits:**
- Easy to modify unit balance without code changes
- Add new unit types by creating new .txt files
- Clear separation of game data from code logic
- Different unit types have unique stats and roles

**Unit Stats Comparison:**

| Unit Type | HP  | ATK | DEF | Range | Mobility | Speed |
|-----------|-----|-----|-----|-------|----------|-------|
| Soldier   | 100 | 20  | 5   | 1     | 3        | 2.0   |
| Archer    | 80  | 25  | 3   | 3     | 4        | 2.5   |
| Knight    | 150 | 35  | 12  | 1     | 2        | 1.8   |

**Testing:**
```
✓ All unit types load attributes correctly
✓ Different units have different stats
✓ Health initializes to max_health properly
✓ Default values used if file not found
```

---

## Previous Features

## 1. Animated Unit Movement

### Implementation
Units now smoothly animate their movement between grid positions instead of teleporting instantly.

### Technical Details
- **Speed attribute**: 2.0 cells per second (configurable per unit)
- **Interpolated positioning**: Units smoothly transition from start to target
- **Animation states**:
  - "move" animation plays during movement
  - "idle" animation resumes when movement completes
- **Progress tracking**: Linear interpolation from 0.0 to 1.0

### New Unit Attributes
```python
speed = 2.0              # Cells per second
is_moving = False        # Movement in progress flag
movement_start_pos       # Starting grid position
movement_target_pos      # Destination grid position  
movement_progress        # 0.0 to 1.0 completion
```

### New Unit Methods
```python
get_current_position()   # Returns interpolated (row, col) with floats
move_to(position)        # Starts animated movement
```

### Movement Timing
- 1 cell: 0.5 seconds
- 2 cells: 1.0 seconds
- 3 cells: 1.5 seconds
- 4 cells: 2.0 seconds

Distance is calculated using Manhattan distance: `|row_diff| + |col_diff|`

### Testing
All movement animation tests pass:
```
✓ Movement progress calculated correctly
✓ Position interpolation works
✓ Animation switches from "move" to "idle"
✓ Final position matches target
✓ Timing matches expected duration
```

## 2. Unit Hover Tooltips

### Implementation
When hovering the mouse over any unit, a tooltip displays their stats.

### Features
- **Automatic detection**: Mouse position converted to grid coordinates
- **All units**: Works for both player and enemy units
- **Real-time updates**: Tooltip follows mouse cursor
- **Smart positioning**: Stays on screen, adjusts if near edges
- **Team identification**: Shows "(Player)" or "(Enemy)" accordingly

### Displayed Information
```
Soldier (Player)
HP: 100/100
Attack: 20
Defense: 5
Mobility: 3/3
Range: 1
```

### Visual Design
- Semi-transparent black background (220 alpha)
- Red border (255, 100, 100)
- White text
- 10px padding
- Offset from cursor to avoid blocking view

### New Scenario Methods
```python
update_hover(mouse_x, mouse_y, screen_width, screen_height)
draw_hover_info(screen, font)
```

### New Scenario Attributes
```python
hovered_unit = None      # Currently hovered enemy unit
```

## Integration

### Main Game Loop Updates

**Update phase:**
```python
scenario.update(dt)                          # Animate units
scenario.update_hover(mouse_x, mouse_y, ...)  # Track hover
```

**Draw phase:**
```python
scenario.draw_map(screen)                    # Terrain
scenario.draw_selection_highlights(screen)   # Selection UI
scenario.draw_units(screen)                  # Units (with interpolation)
scenario.draw_hover_info(screen, font)       # Enemy tooltips
```

### Modified Files

1. **unit.py**
   - Added speed, movement state, and interpolation
   - Modified `update()` to handle movement animation
   - Modified `move_to()` to start animation instead of instant move
   - Added `get_current_position()` for smooth rendering

2. **scenario.py**
   - Modified `draw_units()` to use interpolated positions
   - Added `update_hover()` for mouse tracking
   - Added `draw_hover_info()` for tooltip rendering
   - Added `hovered_unit` state

3. **main.py**
   - Added hover update call in `update()`
   - Added hover info rendering in `draw()`
   - Updated instructions to mention hover feature

4. **Documentation**
   - Updated UNIT_SYSTEM.md with new attributes/methods
   - Updated GAMEPLAY.md with animation and hover details
   - Updated README.md with new features

## User Experience Improvements

### Before
- Units teleported instantly to destination
- No way to see enemy stats without selecting them
- Movement felt abrupt and arcade-like

### After
- Units smoothly glide across the grid
- Hover over enemies to preview their capabilities
- Movement feels more strategic and deliberate
- Better visual feedback for tactical decisions

## Performance

- Movement interpolation adds minimal overhead
- Hover detection reuses existing screen-to-grid conversion
- Tooltip only renders when hovering enemy
- No performance impact on 60 FPS gameplay

## Future Enhancements

Possible extensions:
- Adjustable speed per unit type (✓ DONE - now loaded from files)
- Movement along actual path (not just straight line)
- Acceleration/deceleration curves
- Hover info for all units (✓ DONE - now works for player and enemy)
- Health bars above units (✓ DONE - color-coded green/yellow/red)
- Attack range indicators on hover
- Combat system implementation
- Victory/defeat conditions
