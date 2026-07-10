# Unit System Documentation

## Unit Class Attributes

### Attribute Loading System

Unit attributes are now loaded from JSON files located in `resources/units/{unit_type}.json`.

**File Format:**
```json
{
  "name": "Soldier",
  "description": "Balanced infantry unit with moderate stats",
  "max_health": 100,
  "attack_power": 20,
  "defense": 5,
  "attack_range": 1,
  "max_mobility": 3,
  "speed": 2.0,
  "projectile_speed": 0.0,
  "projectile_count": 1,
  "hit_chance": 0.95,
  "damage_std": 3.0,
  "fire_type": "direct",
  "vision_range": 5
}
```

If a unit's attribute file is not found, default values are used.

### Combat Attributes
- **health** (int): Current hit points (0 to max_health)
- **max_health** (int): Maximum hit points (loaded from file)
- **attack_power** (int): Base damage dealt in combat (median of damage distribution) - **reduced when damaged (melee only)**
- **defense** (int): Damage reduction/armor value (loaded from file)
- **attack_range** (int): Number of grid cells unit can attack from (loaded from file)
- **projectile_speed** (float): Speed of projectiles in cells per second (0 = melee, >0 = ranged)
- **projectile_count** (int): Number of projectiles fired per attack (1 = single shot, 2+ = volley/battery)
- **hit_chance** (float): Probability of hitting target (0.0 to 1.0) - **melee units have higher accuracy**
- **damage_std** (float): Standard deviation for damage variance (Gaussian distribution) - **evolve for consistency**
- **fire_type** (string): Attack type - **'direct'** requires line of sight, **'indirect'** can fire over obstacles

### Movement Attributes
- **mobility** (int): Current movement points available this turn - **reduced when damaged**
- **max_mobility** (int): Maximum movement points per turn (loaded from file)
- **speed** (float): Movement animation speed in cells per second (loaded from file)

### Vision Attributes
- **vision_range** (int): How far the unit can see in cells (loaded from file)
  - Creates circular visible area using Euclidean distance
  - Affects fog of war visibility and targeting
  - Different per unit type: Archer (7), Soldier (5), Knight (4)
  - Higher vision = better scouting capability

## Damage Degradation System

Units become weaker and slower as they take damage. All units suffer mobility degradation. Additionally:
- **Melee units**: Attack power degrades with health
- **Ranged units**: Projectile count degrades with health (attack power per projectile remains full)

**Important:** 
- **Melee attacks** suffer damage degradation (wounded knight swings weaker)
- **Ranged attacks** maintain full power per projectile, but fire fewer projectiles (wounded archer fires fewer arrows at full strength)

### Mobility Degradation (All Units)
| Health % | Mobility | Example (Max 5) |
|----------|----------|-----------------|  
| 100-75%  | 100%     | 5 moves         |
| 75-50%   | 85%      | 4 moves         |
| 50-25%   | 65%      | 3 moves         |
| 25-0%    | 40%      | 2 moves         |

### Projectile Count Degradation (Ranged Only)
| Health % | Projectiles | Example (Max 3) |
|----------|-------------|-----------------|  
| 100-75%  | 100%        | 3 arrows        |
| 75-50%   | 85%         | 2 arrows        |
| 50-25%   | 65%         | 1 arrow         |
| 25-0%    | 40%         | 1 arrow (min)   |

**Applies to:** Ranged units only (Archers)  
**Does NOT apply to:** Melee units (always 1 strike)
| Health % | Attack   | Example (Base 30) |
|----------|----------|-------------------|
| 100-75%  | 100%     | 30 damage         |
| 75-50%   | 85%      | 25 damage         |
| 50-25%   | 70%      | 21 damage         |
| 25-0%    | 50%      | 15 damage         |

**Applies to:** Melee units only (Knights, Soldiers)  
**Does NOT apply to:** Ranged units (Archers) - they always deal full attack_power

**Strategic Implications:**
- Damaged melee units should retreat or be protected (much weaker strikes)
- Damaged ranged units maintain firepower but with reduced rate of fire
- All damaged units are slower and easier to catch
- Focus fire on melee threats reduces their damage output
- Focus fire on ranged threats reduces their volley size
- Wounded archers still deadly but less overwhelming (1-2 arrows vs 3)
- Healing (if implemented) valuable for all unit types
- Protecting wounded units becomes a tactical consideration

## Hit Chance System

Attacks have a probability of missing. Each attack rolls against the unit's hit_chance to determine if it hits.

### Hit Chance by Unit Type
| Unit    | Hit Chance | Notes                                    |
|---------|------------|------------------------------------------|
| Knight  | 98%        | Extremely accurate melee strikes         |
| Soldier | 95%        | Reliable infantry combat                 |
| Archer  | 75%        | Ranged attacks are less accurate         |

### Multi-Projectile Attacks
For units that fire multiple projectiles (e.g., archers with 3 arrows):
- **Each projectile rolls separately** for hit/miss
- An attack with 3 projectiles at 75% hit chance typically results in:
  - 2-3 hits (most common)
  - 0-1 hits (rare but possible)
- This adds variability and excitement to ranged combat

### Visual Feedback
- **-X** (damage number) appears in **bright green** text above the target when an attack hits
  - Example: "-12" means 12 damage was dealt
  - Damage varies due to Gaussian distribution
- **0** appears in **red** text above the target when an attack misses
- Messages fade out and float upward over 1.5 seconds
- Multiple projectiles create **horizontally separated messages** for clarity
- Messages appear very close to the target unit (just above it)
- Press **H key** to toggle damage display on/off

### Console Output
All attacks print hit/miss results to the console:
```
archer fired 3 projectiles at soldier
archer's projectile hit soldier for 12 damage (HP: 88/100)
archer's projectile missed soldier!
archer's projectile hit soldier for 12 damage (HP: 76/100)
```

## Damage Variance System

Every successful hit deals **variable damage** using a Gaussian (normal) distribution. This creates realistic combat variance where damage fluctuates around the unit's base attack power.

### How It Works

**Attack Power as Median:**
- `attack_power` is the median (center) of the damage distribution
- Actual damage is sampled from: `N(attack_power, damage_std²)`
- Minimum damage is always 1

**Standard Deviation (damage_std):**
- Controls the spread/consistency of damage
- Lower std = more consistent damage (tight distribution)
- Higher std = more variable damage (wide distribution)

### Damage Distribution by Unit

| Unit    | Attack Power | Damage Std | Typical Range | Notes                           |
|---------|--------------|------------|---------------|---------------------------------|
| Archer  | 12           | 2.5        | 9-15          | Moderate variance per arrow     |
| Soldier | 22           | 3.0        | 18-26         | Reliable consistent damage      |
| Knight  | 30           | 4.0        | 24-36         | High damage with some variance  |

### Evolution Strategy

Units can evolve along two axes:

**1. Hit Chance Evolution:**
- Increase `hit_chance` to hit more reliably
- Trade-off: May decrease damage or increase cost

**2. Damage Consistency Evolution:**
- Decrease `damage_std` for tighter damage distribution
- Example: Archer with std=1.0 deals 10-14 damage (more predictable)
- Example: Archer with std=4.0 deals 6-18 damage (more variable)

**Example Evolution Path:**
```
# Archer Evolution Stages
Stage 1: attack_power=12, hit_chance=0.75, damage_std=2.5  (current)
Stage 2: attack_power=12, hit_chance=0.80, damage_std=2.0  (more accurate, more consistent)
Stage 3: attack_power=14, hit_chance=0.80, damage_std=1.5  (elite: high damage, accurate, consistent)
```

### Configuration

Edit unit definition files:
```json
// resources/units/archer.json
{
  "attack_power": 12,     // Median damage (center of distribution)
  "damage_std": 2.5,      // Standard deviation (controls variance)
  "hit_chance": 0.75      // 75% chance to hit per projectile
}
```

Lower `damage_std` = more reliable/consistent unit (good for strategy)
Higher `damage_std` = more chaotic/unpredictable unit (high risk/reward)

### Movement Animation State
- **is_moving** (bool): Whether unit is currently animating movement
- **movement_start_pos** (tuple): Starting position for animation
- **movement_target_pos** (tuple): Target position for animation
- **movement_progress** (float): Animation progress from 0.0 to 1.0

### Position & Identity
- **unit_type** (str): Type identifier (e.g., "soldier", "archer", "knight")
- **team** (int): Player/team number (0, 1, 2, etc.)
- **position** (tuple): Grid location as (row, col)

### Status Flags
- **is_alive** (bool): Whether unit is still alive
- **is_active** (bool): Whether unit can act this turn
- **facing_direction** (str): Direction facing ("right", "left", "up", "down")

### Animation System
- **current_animation** (str): Current animation name ("idle", "move", "attack", "death")
- **animation_frame** (int): Current frame index in animation
- **animation_speed** (float): Seconds per frame (default: 0.1)
- **animation_timer** (float): Internal timer for frame updates

## Animation Types

Each unit type supports four animation states:

1. **Idle** - Resting/waiting state (2 frames)
2. **Move** - Walking/moving animation (4 frames)
3. **Attack** - Combat action (3 frames)
4. **Death** - Defeat/destruction sequence (4 frames)

## File Structure

Animation files follow this naming convention:
```
resources/units/{unit_type}_{animation}_{frame}.png
```

Examples:
- `resources/units/soldier_idle_0.png`
- `resources/units/archer_move_2.png`
- `resources/units/knight_attack_1.png`

## Unit Types

### Currently Available:

#### Soldier (Blue) - Balanced Infantry
- **Max Health:** 100
- **Attack Power:** 22 (median)
- **Damage Std:** 3.0 (typical range: 18-26)
- **Defense:** 6
- **Attack Range:** 1
- **Max Mobility:** 3
- **Speed:** 2.0
- **Hit Chance:** 95%
- **Role:** Versatile frontline melee fighter with balanced stats and reliable damage

#### Archer (Green) - Ranged Attacker
- **Max Health:** 80
- **Attack Power:** 12 per projectile (median)
- **Damage Std:** 2.5 (typical range per arrow: 9-15)
- **Defense:** 3
- **Attack Range:** 5
- **Max Mobility:** 3
- **Speed:** 2.5
- **Projectile Speed:** 4.0
- **Projectile Count:** 3 (fires 3 arrows per attack)
- **Hit Chance:** 75% (per projectile)
- **Total Damage:** Typically 24-36 if 2-3 arrows hit
- **Role:** Glass cannon with high mobility and range but low health/defense. Variable damage output.

#### Knight (Purple) - Heavy Cavalry
- **Max Health:** 150
- **Attack Power:** 30 (median)
- **Damage Std:** 4.0 (typical range: 24-36)
- **Defense:** 12
- **Attack Range:** 1
- **Max Mobility:** 2
- **Speed:** 1.8
- **Hit Chance:** 98%
- **Role:** Heavy tank with highest HP and armor, powerful strike with some variance, very slow movement

Each unit type has 13 animation frames total (39 files for all 3 types).

### Adding New Unit Types

To add a new unit type:
1. Create attribute file: `resources/units/{unit_type}.json`
2. Create animation frames: `resources/units/{unit_type}_{animation}_{frame}.png`
3. Add unit to scenario units file with the new unit_type name

## Key Methods

### Combat
- `take_damage(damage)` - Apply damage with defense calculation
- `heal(amount)` - Restore health points
- `attack(target)` - Attack another unit

### Movement
- `move_to(position)` - Start animated movement to new grid location
- `reset_turn()` - Reset for new turn (restore mobility)
- `get_current_position()` - Get interpolated position during animation

### Animation
- `set_animation(name)` - Change current animation
- `update(dt)` - Update animation frame and movement
- `get_current_frame()` - Get current pygame surface
- `draw(screen, x, y, cell_size)` - Render unit to screen
- `draw_health_bar(screen, x, y, cell_size)` - Render health bar above unit

### Team Identification
- `is_player_unit()` - Check if team 0 (player)
- `is_enemy_unit()` - Check if team 1 (enemy)
- `is_ally_of(unit)` - Check if same team

## Health Bar System

Health bars are automatically displayed above each unit:

**Visual Properties:**
- **Width**: 80% of cell size
- **Height**: 8% of cell size (minimum 4px)
- **Position**: 2px above unit sprite
- **Colors**: 
  - Green: >60% health (healthy)
  - Yellow: 30-60% health (wounded)
  - Red: <30% health (critical)
- **Fill**: Proportional to current health percentage
- **Border**: White outline for visibility

**Features:**
- Scales dynamically with grid zoom
- Updates in real-time as health changes
- Works with all unit types and max health values
- Hidden if would render off-screen (above viewport)

## Usage Example

```python
from unit import Unit

# Create a soldier
soldier = Unit(unit_type="soldier", team=0, position=(2, 3))

# Move the unit
soldier.move_to((3, 4))

# Update animation (call each frame)
soldier.update(delta_time)

# Draw the unit
soldier.draw(screen, x_pos, y_pos, 64)

# Combat
archer = Unit(unit_type="archer", team=1, position=(5, 5))
damage = soldier.attack(archer)
```

## Future Expansion Ideas

### Additional Attributes to Consider:
- **experience** - Level up system
- **special_abilities** - Unique powers per unit
- **cost** - Resource cost to create unit
- **evasion** - Dodge chance
- **movement_type** - Flying, ground, water
- **morale** - Affects combat effectiveness

### Additional Animations:
- Hurt/damage reaction
- Special ability casting
- Victory pose
- Retreat/flee
- Different directional sprites
