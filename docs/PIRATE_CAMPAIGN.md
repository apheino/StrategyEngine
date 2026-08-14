# Rise of the Pirate King Campaign

## Overview
Epic 10-scenario campaign where you start with a single stolen sloop and fight your way to become the legendary Pirate King of the Caribbean!

## Campaign Progression

### Economy System
- **Starting Gold:** 500 pieces
- **Earn Gold:** Complete scenarios, defeat enemies, capture settlements
- **Buy Ships:** Build your fleet between scenarios
  - Sloop: 500 gold (fast, weak)
  - Brigantine: 1500 gold (balanced)
  - Frigate: 3000 gold (artillery, mortars)
  - Ship of the Line: 5000 gold (powerful warship)

### Ship Fleet Selection
Starting from Scenario 2, you choose your fleet composition before each battle. Spend your accumulated gold wisely!

## Scenarios

### 1. Humble Beginnings (Difficulty: 1)
**Objective:** Defeat merchant convoy, earn first gold
- Start: 1 Sloop ("Sea Rat")
- Enemies: 3 Merchant ships
- Reward: 800 gold
- Learn: Basic combat and maneuvering

### 2. First Conquest (Difficulty: 2)
**Objective:** Capture coastal fortress
- Available Ships: Sloop, Brigantine
- Enemies: Coastal defenses, naval fort
- Reward: 1500 gold + Porto Seguro settlement
- Learn: Fortress assault tactics

### 3. Island Chain Raid (Difficulty: 3)
**Objective:** Capture 3 islands before Royal Navy arrives
- Time Limit: 15 turns
- Available Ships: Sloop, Brigantine
- Reward: 2000 gold
- Learn: Speed and tactical decision-making

### 4. Rival Pirates (Difficulty: 4)
**Objective:** Defeat competing pirate crew
- Available Ships: Sloop, Brigantine, Frigate
- Enemies: Rival pirate fleet + stronghold
- Reward: 3000 gold
- Learn: Using mortars and artillery

### 5. The Armada Approaches (Difficulty: 5)
**Objective:** Survive Spanish Armada assault
- Available Ships: All types
- Enemies: Large Spanish fleet
- Reward: 5000 gold
- Learn: Using terrain (narrow channels) tactically

### 6. Fortress Siege (Difficulty: 6)
**Objective:** Capture heavily fortified island
- Available Ships: All types
- Enemies: Governor's fortress, elite defenses
- Reward: 7000 gold
- Learn: Long siege warfare

### 7. Naval Blockade (Difficulty: 7)
**Objective:** Break Royal Navy blockade
- Available Ships: All types
- Enemies: Blockading fleet at strategic channels
- Reward: 8000 gold
- Learn: Naval superiority and control points

### 8. The Pirate Alliance (Difficulty: 8)
**Objective:** Unite pirate crews and defeat colonial forces
- Available Ships: All types
- Allies: 3 pirate crews join you
- Reward: 10000 gold
- Learn: Alliance warfare and coordination

### 9. Clash of Titans (Difficulty: 9)
**Objective:** Defeat legendary Admiral Blackwood
- Available Ships: All types
- Enemies: Admiral's flagship + elite fleet
- Reward: 12000 gold
- Learn: Fighting legendary opponents

### 10. Rise of the Pirate King (FINAL - Difficulty: 10)
**Objective:** Defeat the Pirate King and claim the throne
- Available Ships: All types
- Enemies: Pirate King Redbeard's legendary fleet + fortress
- Reward: 20000 gold + BECOME PIRATE KING
- Final Battle: Supremacy of the Caribbean!

## Features

### Island Fortresses
- Can be fought, captured, or lost
- Provide territorial control and gold per turn
- Heavy cannon defenses (8 range, 40 damage)
- Garrison defenders spawn to protect
- Capture by occupying adjacent tiles

### Archipelago Maps
- Realistic island chain layouts
- Strategic chokepoints and channels
- Natural harbors and beaches
- Varied terrain (jungle islands, rocky outcrops, reefs)
- Tactical positioning opportunities

### Enhanced Enemy AI

**The enemy AI uses sophisticated tactics to challenge you!**

- **Target Prioritization:** Focuses damaged ships (< 30% HP gets +50 priority), high-value targets (Ship of Line +30), and immediate threats
- **Fleet Coordination:** Allies work together with focus fire (2+ units attack same target), wait for reinforcements when outnumbered
- **Tactical Positioning:** Maintains optimal firing range, uses terrain for cover, retreats when badly damaged (< 25% HP)
- **Adaptive Strategy:** Evaluates fleet strength ratios and adjusts (aggressive when winning, defensive when losing)
- **Difficulty Scaling:** AI improves from Easy (3) to Pirate King (10) with enhanced coordination and perfect execution

📖 **For detailed AI behavior explanation, see [AI_BEHAVIOR.md](AI_BEHAVIOR.md)**

### Amazing Start Menu
- Caribbean water background with gradient effect
- Animated sailing ship silhouettes (bobbing motion)
- Pirate-themed decorations (treasure chest with coins, rotating compass)
- Gold and cream 8-bit color palette
- Smooth 60 FPS animations
- Keyboard and mouse support
- Smooth animations and transitions
- Full keyboard and mouse support

## Victory Conditions
Each scenario has unique objectives:
- **Eliminate Enemy:** Destroy all enemy ships
- **Capture Fortress:** Take control of fortifications
- **Control Territory:** Hold strategic points
- **Time-Limited:** Complete before deadline
- **Survival:** Withstand assault waves

## Tips for Success

1. **Early Game (Scenarios 1-3):**
   - Focus on sloops for speed
   - Learn enemy patterns
   - Conserve your ships

2. **Mid Game (Scenarios 4-7):**
   - Mix ship types for versatility
   - Use frigates for long-range bombardment
   - Capture fortresses for income

3. **Late Game (Scenarios 8-10):**
   - Build balanced fleet with Ships of the Line
   - Coordinate attacks on priority targets
   - Use island terrain for defensive advantage

## File Locations
- Campaign: `resources/campaigns/pirate_king_campaign.json`
- Stories: `resources/stories/pirate_*.json`
- Maps: `resources/maps/pirate_map_*.txt`
- Units: `resources/maps/pirate_units_*.json`
- AI: `naval_ai.py`
- Menu: `start_menu.py`

---

**Yo ho ho! May the winds fill your sails and the gold fill your coffers!**

*Become the Legend. Claim the Throne. Rule the Caribbean!*
