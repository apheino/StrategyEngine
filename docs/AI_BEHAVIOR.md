# Enemy AI Behavior System - Technical Documentation

## Overview

The Caribbean Naval Warfare game features an intelligent AI system (NavalAI) that provides challenging and realistic enemy behavior. This document explains in detail how the AI makes decisions and controls enemy units.

---

## AI Architecture

### Core Components

The AI system is implemented in `naval_ai.py` and consists of:
1. **NavalAI Class** - Main decision-making engine
2. **Difficulty Scaling** - Adjustable intelligence level (1-10)
3. **Tactical Decision System** - Action selection logic
4. **Fleet Coordination** - Multi-unit cooperation
5. **Strategic Evaluation** - Overall battle assessment

### Initialization

```python
ai = NavalAI(difficulty=5)  # Normal difficulty
```

**Difficulty Levels:**
- `1-3`: Easy - Basic behavior, no coordination
- `4-6`: Normal - Standard tactics, some coordination
- `7-8`: Hard - Advanced tactics, strong coordination
- `9-10`: Expert/Pirate King - Perfect execution

---

## Decision-Making Process

### Phase 1: Target Prioritization

The AI evaluates ALL visible enemies and assigns priority scores to each target.

#### Scoring System

**Base Factors:**

1. **Health-Based Priority**
   - Enemy at < 30% HP: **+50 points** (high priority - finish them off!)
   - Enemy at 30-60% HP: **+25 points** (medium priority - exploit weakness)
   - Enemy at > 60% HP: **+0 points** (low priority - fresh target)
   
   *Rationale:* Eliminating wounded enemies removes threats and prevents healing/retreat

2. **Threat Assessment**
   - Enemy attack power: **+attack_value × 2 points**
   - Example: Ship with 30 attack = +60 priority points
   
   *Rationale:* Neutralize high-damage threats first to minimize damage taken

3. **Range Consideration**
   - Enemy within attack range: **+30 points** (can attack immediately!)
   - Enemy outside range: **-2 points per tile distance**
   - Example: Enemy 5 tiles away = -10 points
   
   *Rationale:* Prioritize targets that can be engaged this turn

4. **Unit Type Value**
   - Ship of the Line: **+30 points** (high-value flagship)
   - Frigate: **+25 points** (artillery threat)
   - Brigantine: **+15 points** (balanced)
   - Sloop: **+10 points** (basic)
   
   *Rationale:* Eliminate valuable enemy assets for strategic advantage

5. **Randomization**
   - Random modifier: **-10 to +10 points**
   
   *Rationale:* Adds unpredictability, prevents exploitable patterns

#### Example Priority Calculation

Enemy Ship of the Line at 25% HP, 15 attack power, 3 tiles away:
- Base: 0
- Low health (<30%): +50
- Threat (15 × 2): +30
- Distance (3 tiles): -6
- Unit type: +30
- Random (e.g., +5): +5
- **Total: 109 points** (VERY HIGH PRIORITY!)

Healthy Sloop at 100% HP, 10 attack power, 2 tiles away:
- Base: 0
- Health: +0
- Threat (10 × 2): +20
- Distance: -4
- Unit type: +10
- Random (e.g., -3): -3
- **Total: 23 points** (lower priority)

**Result:** AI will focus on the wounded Ship of the Line first.

---

### Phase 2: Action Selection

After identifying the best target, the AI decides what action to take:

#### Decision Tree

```
1. No enemies visible?
   → PATROL (random movement)

2. Unit health < 25% AND defensive tactics enabled?
   → RETREAT (move away from enemies)

3. Target within attack range?
   → Should focus fire with allies? (difficulty ≥ 5)
      → Yes: ATTACK (coordinated)
      → No: ATTACK (individual)

4. Target outside range AND aggressive tactics?
   → Should wait for allies? (difficulty ≥ 6)
      → Yes: WAIT (hold position)
      → No: MOVE_ATTACK (approach target)

5. Otherwise?
   → DEFENSIVE_POSITION (form up with allies)
```

#### Action Types Explained

**1. ATTACK**
- Unit fires at selected target
- Uses optimal weapon (cannons/mortars based on range)
- Considers focus fire if allies can also hit target

**2. MOVE_ATTACK**
- Move toward target while maintaining optimal range
- Stops at `(attack_range - 1)` tiles away
- Uses A* pathfinding to avoid obstacles
- Maximum movement per turn based on ship speed

**3. RETREAT**
- Calculate average enemy position
- Move in opposite direction
- Try to reach allied units for protection
- Prioritize survival over damage

**4. DEFENSIVE_POSITION**
- Move toward allied unit center of mass
- Form defensive formation
- Maintain spacing (2-3 tiles between units)
- Prepare for enemy approach

**5. WAIT**
- Hold current position
- Preserve movement for next turn
- Used when waiting for ally reinforcements

**6. PATROL**
- Random movement within allowed area
- Search for enemies
- Maintain territorial presence

---

### Phase 3: Fleet Coordination (Difficulty ≥ 5)

High-difficulty AI uses sophisticated multi-unit tactics.

#### Focus Fire

**Trigger Conditions:**
- Difficulty ≥ 5
- 2+ allied units can hit the same target
- Target is high-priority

**Effect:**
- Multiple units attack same enemy simultaneously
- Concentrates damage to eliminate threats quickly
- Mimics human player "focus fire" strategy

**Example:**
```
Turn 1:
- Enemy frigate at 80% HP
- 3 AI brigantines can reach it
- AI enables focus fire
- All 3 attack frigate
- Frigate reduced to 20% HP

Turn 2:
- Same 3 brigantines finish off frigate
- Enemy loses artillery support
```

#### Allied Waiting

**Trigger Conditions:**
- Difficulty ≥ 6
- AI unit outnumbered 2:1 or worse within 8-tile radius
- Unit health > 25%

**Effect:**
- Unit holds position instead of charging
- Waits for allied reinforcements
- Prevents isolated units from being destroyed

**Example:**
```
Situation:
- 1 AI ship faces 3 enemy ships
- Allies are 6 tiles away

Without waiting logic:
- AI ship charges → gets surrounded → dies

With waiting logic:
- AI ship waits → allies arrive → 4v3 advantage → wins
```

#### Formation Maintenance

**Trigger Conditions:**
- Defensive tactics active
- Multiple allied units present

**Effect:**
- Units move toward ally center of mass
- Maintain 2-3 tile spacing
- Create mutual support network
- Concentrated firepower

---

## Strategic Evaluation

The AI assesses overall battle situation each turn.

### Strength Calculation

**Formula:**
```
unit_strength = current_hp × attack_power
fleet_strength = sum(all_unit_strengths)
strength_ratio = friendly_strength / enemy_strength
```

### Strategy Selection

**Based on strength ratio:**

| Ratio | Strategy | Behavior |
|-------|----------|----------|
| > 1.5 | AGGRESSIVE | Press attack, eliminate enemies |
| 0.5 - 1.5 | BALANCED | Tactical combat, opportunistic |
| < 0.5 | DEFENSIVE | Regroup, protect weakened units |

**Example:**

```
Scenario 1: AI Winning
- AI fleet: 3 ships, total strength = 450
- Enemy fleet: 2 ships, total strength = 250
- Ratio: 450/250 = 1.8
- Strategy: AGGRESSIVE
- AI behavior: All units attack, push forward

Scenario 2: AI Losing
- AI fleet: 2 ships, total strength = 200
- Enemy fleet: 4 ships, total strength = 500
- Ratio: 200/500 = 0.4
- Strategy: DEFENSIVE
- AI behavior: Retreat, form defensive line, protect damaged ships
```

---

## Difficulty Scaling Details

### Easy (Difficulty 1-3)

**Characteristics:**
- No fleet coordination
- Simple target selection (nearest enemy)
- No retreat logic
- 50% aggressive / 50% defensive split
- Random patrol when idle

**Tactics Configuration:**
```python
tactics = {
    "aggressive": 0.5,
    "defensive": 0.5,
    "coordinated": False
}
```

**Behavior:**
- Attacks closest visible enemy
- No focus fire
- Doesn't wait for allies
- Predictable patterns

**Best for:** New players learning mechanics

---

### Normal (Difficulty 4-6)

**Characteristics:**
- Basic coordination enabled
- Proper target prioritization (uses scoring system)
- Simple retreat logic (< 25% HP)
- 60% aggressive / 40% defensive
- Focus fire on high-value targets

**Tactics Configuration:**
```python
tactics = {
    "aggressive": 0.6,
    "defensive": 0.4,
    "coordinated": True
}
```

**Behavior:**
- Prioritizes wounded enemies
- Uses focus fire when 2+ units available
- Retreats when critically damaged
- Some unpredictability from random modifiers

**Best for:** Intermediate players, main campaign

---

### Hard (Difficulty 7-8)

**Characteristics:**
- Advanced coordination
- Full strategic evaluation
- Allied waiting logic active
- 70% aggressive / 30% defensive
- Optimal positioning

**Tactics Configuration:**
```python
tactics = {
    "aggressive": 0.7,
    "defensive": 0.3,
    "coordinated": True
}
```

**Behavior:**
- Waits for allies before engaging when outnumbered
- Maintains optimal attack range
- Uses terrain advantages
- Adaptive strategy (aggressive/defensive/balanced)
- Coordinated multi-unit attacks

**Best for:** Experienced players seeking challenge

---

### Expert/Pirate King (Difficulty 9-10)

**Characteristics:**
- Perfect execution
- Maximum coordination
- Advanced tactical decisions
- 70% aggressive / 30% defensive
- Exploits all weaknesses

**Tactics Configuration:**
```python
tactics = {
    "aggressive": 0.7,
    "defensive": 0.3,
    "coordinated": True
}
```

**Behavior:**
- Never makes suboptimal moves
- Perfect focus fire timing
- Optimal retreat decisions
- Superior positioning
- Exploits player mistakes immediately
- Minimal randomization (more predictable but optimal)

**Best for:** Expert players, final campaign scenarios

---

## Tactical Patterns

### Pattern 1: Wounded Target Elimination

**Situation:** Enemy at < 30% HP

**AI Behavior:**
1. All nearby units prioritize wounded target (+50 priority)
2. Focus fire if 2+ units can reach
3. Use fast ships (sloops) to finish off fleeing enemies
4. Prevent healing/retreat

**Counter:** Protect damaged ships, retreat to safety, use screening units

---

### Pattern 2: Artillery Focus

**Situation:** Enemy frigate (long-range artillery) detected

**AI Behavior:**
1. Frigate gets +25 priority (high threat)
2. Fast ships (sloops/brigantines) rush to engage
3. Close distance to negate range advantage
4. Focus fire once in range

**Counter:** Protect frigates with screening ships, use terrain for cover

---

### Pattern 3: Defensive Retreat

**Situation:** AI unit at < 25% HP

**AI Behavior:**
1. Unit retreats toward allies
2. Move away from enemy center of mass
3. Seek cover behind terrain/islands
4. Allies provide covering fire

**Counter:** Pursue with fast ships, cut off retreat path, finish quickly

---

### Pattern 4: Ambush from Islands

**Situation:** AI ships positioned near jungle islands

**AI Behavior:**
1. Use jungle terrain for concealment
2. Wait for player to approach
3. Emerge when player is in optimal range
4. Coordinated attack from multiple angles

**Counter:** Scout ahead, use long-range artillery, approach cautiously

---

### Pattern 5: Fortress Support

**Situation:** AI defending captured fortress

**AI Behavior:**
1. Position ships within fortress cannon range (8 tiles)
2. Use fortress as artillery support
3. Ships engage player units within fortress range
4. Retreat behind fortress walls when damaged
5. Create defensive perimeter

**Counter:** Lure ships away from fortress, focus fortress first, use superior range

---

## AI Limitations & Exploits

### Known Limitations

1. **Pathfinding Issues**
   - AI can get stuck on complex terrain
   - May take suboptimal paths around islands
   
2. **Predictable Retreat**
   - Always retreats away from enemy center
   - Retreat path can be anticipated
   
3. **No Bait Recognition**
   - Won't recognize sacrificial decoy ships
   - Can be lured into traps
   
4. **Fog of War**
   - AI only reacts to visible units
   - No strategic scouting behavior

### Player Exploits (Known)

1. **Isolation Tactic**
   - Lure single AI ship away from fleet
   - Surround and destroy before allies arrive
   
2. **Kiting**
   - Use faster ships to stay at max range
   - Attack and retreat repeatedly
   
3. **Fortress Cheese**
   - Attack from beyond fortress range
   - AI won't leave fortress protection

**Note:** These exploits are intentional for player satisfaction. Higher difficulties minimize but don't eliminate them.

---

## Configuration Files

### Campaign AI Settings

Each scenario in `resources/campaigns/pirate_king_campaign.json` has difficulty setting:

```json
{
  "id": "pirate_10",
  "difficulty": 10,
  "ai_behavior": "pirate_king"
}
```

### Unit AI Behavior

Individual units in `resources/maps/pirate_units_X.json` can have custom AI:

```json
{
  "type": "frigate",
  "team": "enemy",
  "ai_behavior": "defensive",  // or "aggressive", "flee", "guard"
  "ai_priority": "high"
}
```

**Behavior Types:**
- `aggressive`: Actively hunts player ships
- `defensive`: Guards area, only attacks nearby
- `flee`: Runs away from combat (merchants)
- `guard`: Protects specific location/unit

---

## Debugging AI Behavior

### Enable AI Debug Mode

Add to your test files:

```python
from naval_ai import NavalAI

# Create AI with debugging
ai = NavalAI(difficulty=5)

# Get decision explanation
action = ai.decide_action(unit, enemies, allies, game_state)
print(f"AI Decision: {action}")
print(f"Target priority: {ai.evaluate_target_priority(unit, enemies, game_state)}")
```

### Common Debug Checks

1. **Why did AI attack X instead of Y?**
   - Check priority scores for both targets
   - Verify range calculations
   - Check difficulty settings

2. **Why didn't AI retreat?**
   - Check unit HP percentage
   - Verify defensive tactics enabled
   - Check difficulty (retreat only at 5+)

3. **Why no focus fire?**
   - Check difficulty ≥ 5
   - Verify 2+ units can reach target
   - Check coordination flag

---

## Future Enhancements

Planned improvements for AI system:

1. **Learning Behavior** - Track player patterns
2. **Scouting Logic** - Active exploration
3. **Trap Detection** - Recognize bait/ambushes
4. **Dynamic Difficulty** - Adjust based on player performance
5. **Personality Traits** - Different AI commanders with unique styles

---

## Summary

The NavalAI system provides challenging opposition through:

✅ **Intelligent target selection** - Prioritizes threats and wounded enemies  
✅ **Fleet coordination** - Focus fire and mutual support  
✅ **Tactical positioning** - Optimal range and terrain use  
✅ **Adaptive strategy** - Adjusts to battle situation  
✅ **Difficulty scaling** - From easy training to expert challenge  

The AI creates realistic naval combat where enemy ships:
- Work together as a coordinated fleet
- Make smart tactical decisions
- Exploit player weaknesses
- Adapt to changing battle conditions
- Provide escalating challenge through campaign

**For Players:** Understanding AI behavior helps you predict enemy actions and develop counter-strategies.

**For Developers:** The modular design allows easy tuning of AI difficulty and behavior patterns.

---

*Last Updated: 2026-08-15*  
*AI Version: 1.0*  
*Module: naval_ai.py*
