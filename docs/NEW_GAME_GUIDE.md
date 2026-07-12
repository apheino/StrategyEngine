# Creating a New Game - Complete Guide

This guide shows you how to create a completely new game or modify the existing one using the Strategy Game Engine and its visual editor tools.

## Overview

The engine separates game content from code, allowing you to create custom games by:
1. **Game Configuration** - Define game identity and settings
2. **Terrain Types** - Create custom terrain with passability rules
3. **Unit Types** - Define unit statistics and abilities
4. **Maps & Scenarios** - Design battlefields and unit placements
5. **Testing & Iteration** - Play and refine your game

All done through visual tools and JSON files - **no code editing required**!

---

## Step 1: Configure Your Game

Edit `game_config.json` to set up your game's identity and rules.

### Game Metadata

```json
{
  "game": {
    "name": "Your Game Name",
    "version": "1.0.0",
    "author": "Your Name",
    "description": "Game description",
    "window_width": 1280,
    "window_height": 720,
    "fps": 60
  }
}
```

**Fields:**
- `name`: Displayed in title bar and menus
- `version`: Track your game versions
- `author`: Your name or team
- `description`: Brief game description
- `window_width/height`: Game window size
- `fps`: Target framerate (usually 60)

### Teams Configuration

Define the factions/sides in your game:

```json
{
  "teams": [
    {
      "id": 0,
      "name": "Heroes",
      "description": "Brave warriors fighting for justice",
      "color": [100, 150, 255],
      "player_controlled": true,
      "turn_order": 0
    },
    {
      "id": 1,
      "name": "Dark Legion",
      "description": "Evil forces seeking domination",
      "color": [200, 50, 50],
      "player_controlled": false,
      "turn_order": 1
    }
  ]
}
```

**Team Fields:**
- `id`: Unique identifier (0, 1, 2...)
- `name`: Team display name
- `description`: Team backstory/role
- `color`: RGB color [R, G, B] for units
- `player_controlled`: true = human controlled, false = AI
- `turn_order`: Sequence of turns (0 goes first, then 1, etc.)

**Tips:**
- You can have 2+ teams (support for 3+ team battles)
- Multiple teams can be player-controlled for hot-seat multiplayer
- Colors should be distinct for visual clarity
- Turn order can be customized (e.g., 0→1→0 or 0→1→2→0)

---

## Step 2: Create Custom Terrain Types

Use the visual terrain creator in the editor.

### Launch Editor

```bash
python editor.py
```

### Create Terrain

1. Press `T` for Terrain mode
2. Scroll down in left panel
3. Click **"+ Create New Terrain"** (green button)

### Define Terrain Properties

**Example: Lava Terrain**

```
Name: lava
Passability: Block (click Block button)
Color R: 255
Color G: 100
Color B: 0
Icon: lava
```

Press **Enter** or click **"Save Terrain"**

### Terrain Examples by Theme

**Fantasy Game:**
- Plains (Easy) - RGB(120, 200, 100)
- Forest (Slow) - RGB(40, 100, 40)
- Mountain (Block) - RGB(140, 120, 100)
- River (Block) - RGB(80, 140, 200)
- Lava (Block) - RGB(255, 100, 0)
- Magic Circle (Easy) - RGB(150, 100, 255)

**Sci-Fi Game:**
- Metal Floor (Easy) - RGB(180, 180, 180)
- Energy Field (Block) - RGB(100, 200, 255)
- Hazard Zone (Slow) - RGB(255, 200, 50)
- Void (Block) - RGB(20, 20, 40)
- Platform (Easy) - RGB(140, 140, 150)

**Historical Game:**
- Grassland (Easy) - RGB(100, 180, 80)
- Woods (Slow) - RGB(60, 100, 50)
- Hill (Slow) - RGB(150, 140, 100)
- River (Block) - RGB(80, 120, 180)
- Road (Easy) - RGB(160, 140, 120)

### Passability Guide

- **Easy (0)**: Normal movement cost
- **Slow (1)**: 2x movement cost (halved mobility when starting from)
- **Blocked (2)**: Cannot pass through, blocks line of sight

**Key Feature:** Multiple terrain types can share the same passability but have different colors/icons for visual variety!

### Terrain File

All terrains saved to: `resources/terrains.json`

You can edit this file directly or use the visual creator. The editor will load all terrains automatically on next start.

---

## Step 3: Create Custom Unit Types

Use the visual unit creator in the editor.

### Create Unit

1. In editor, press `U` for Units mode
2. Scroll down in left panel
3. Click **"+ Create New Unit Type"** (green button)

### Define Unit Attributes

**Example: Fire Mage**

```
Name: firemage
Health: 70
Attack: 40
Defense: 3
Range: 4
Mobility: 2
Vision: 6
```

Press **Enter** or click **"Save Unit"**

### Unit Attribute Guide

**Core Stats:**
- `max_health`: Hit points (typical: 50-200)
- `attack_power`: Base damage (typical: 10-50)
- `defense`: Damage reduction (typical: 0-15)
- `attack_range`: Attack distance in cells (1=melee, 2-5=ranged)
- `max_mobility`: Movement per turn (typical: 2-5)
- `vision_range`: Sight distance (typical: 4-8)

**Advanced Stats (auto-filled):**
- `speed`: Movement animation speed (default: 10)
- `projectile_speed`: Projectile animation speed (default: 15)
- `projectile_count`: Number of projectiles fired (default: 1)
- `projectile_sprite`: Sprite name or "null" for melee (default: "null")
- `hit_chance`: Hit probability 0.0-1.0 (default: 0.95 = 95%)
- `damage_std`: Damage variance (default: 2.0)
- `fire_type`: "direct" or "indirect" (default: "direct")

### Unit Design Patterns

**Melee Infantry:**
- Range: 1
- High health, moderate attack
- Example: Warrior (HP:120, Att:25, Def:8, Range:1, Mobility:3)

**Ranged Attacker:**
- Range: 3-5
- Lower health, high attack
- Example: Archer (HP:70, Att:35, Def:2, Range:4, Mobility:2)

**Heavy Unit:**
- High health and defense
- Low mobility
- Example: Tank (HP:200, Att:30, Def:15, Range:1, Mobility:1)

**Scout:**
- High mobility and vision
- Low combat stats
- Example: Scout (HP:60, Att:15, Def:2, Range:1, Mobility:5, Vision:8)

**Artillery:**
- Very long range
- Slow, low defense
- Example: Catapult (HP:80, Att:50, Def:5, Range:6, Mobility:1)

### Unit Examples by Theme

**Fantasy:**
- Knight (melee, high defense)
- Archer (ranged, medium)
- Wizard (ranged, high attack, low health)
- Healer (support, low combat)
- Dragon (powerful, high mobility)

**Sci-Fi:**
- Marine (balanced infantry)
- Sniper (long-range, precise)
- Mech (heavy, powerful)
- Scout Drone (fast, weak)
- Artillery Bot (siege weapon)

**Historical:**
- Spearman (melee, defensive)
- Bowman (ranged, moderate)
- Cavalry (fast, powerful charge)
- Trebuchet (siege, long-range)
- General (command unit)

### Unit File

All units saved to: `resources/units/{name}.json`

Example file structure:
```json
{
  "max_health": 70,
  "attack_power": 40,
  "defense": 3,
  "attack_range": 4,
  "max_mobility": 2,
  "speed": 10,
  "projectile_speed": 15,
  "projectile_count": 1,
  "projectile_sprite": "fireball",
  "hit_chance": 0.90,
  "damage_std": 3.0,
  "fire_type": "direct",
  "vision_range": 6
}
```

---

## Step 4: Design Maps and Scenarios

Use the editor to create battlefields and place units.

### Create New Map

1. In editor, press `N` for new scenario
2. Press `+` or `-` to adjust grid size (5×5 to 50×50)
3. Recommended sizes:
   - Small: 10×10 to 15×12 (quick battles)
   - Medium: 20×15 to 25×20 (standard)
   - Large: 30×25 to 50×50 (epic battles)

### Paint Terrain

1. Press `T` for Terrain mode
2. Click terrain type in left panel (or press 1-6 for quick select)
3. Click on grid to paint
4. Right-click to erase (resets to first terrain type)

**Map Design Tips:**

**Natural Barriers:**
- Use blocked terrain (water, mountains) to create choke points
- Leave pathways between barriers for tactical movement
- Consider unit vision ranges when placing forests

**Strategic Positions:**
- High ground (could be slow terrain on hills)
- Defensive positions (surrounded by difficult terrain)
- Open areas for ranged units
- Cover areas for melee approach

**Visual Interest:**
- Mix terrain types for variety
- Create themed zones (forest area, desert area, etc.)
- Use roads/paths to guide player movement
- Add water features for visual appeal

### Place Units

1. Press `U` for Units mode
2. Select unit type from left panel
3. Select team (color)
4. Click on grid to place unit
5. Right-click to remove unit

**Unit Placement Tips:**

**Balance:**
- Give each team roughly equal strength
- Mix unit types for tactical variety
- Consider range matchups (melee vs ranged)

**Starting Positions:**
- Place teams on opposite sides/corners
- Leave space between teams for maneuvering
- Consider terrain advantages/disadvantages
- Place scouts/mobile units on flanks

**Scenario Design:**
- Tutorial: Small map, few units, simple terrain
- Standard: Medium map, mixed forces, varied terrain
- Challenge: Large map, asymmetric forces, complex terrain

### Save Scenario

1. Press `S` to save
2. Creates two files:
   - `resources/maps/map_N.txt` (terrain data)
   - `resources/maps/units_N.json` (unit placements)

**Scenario Numbering:**
- Scenario 1: Usually tutorial/first mission
- Scenario 2, 3, etc.: Progressive difficulty
- Default scenario_number = 1 (edit in code for other scenarios)

### Create Multiple Scenarios

To create scenario 2, 3, etc.:
1. In `editor.py`, find `self.scenario_number = 1`
2. Change to desired number (or add UI control)
3. Design and save new scenario

---

## Step 5: Test Your Game

### Launch Game

```bash
python main.py
```

### Test Checklist

**Menu System:**
- ✓ Game name displays correctly
- ✓ Can start campaign or skirmish
- ✓ Scenarios appear in selection

**Gameplay:**
- ✓ Terrain displays with correct colors
- ✓ Units appear with team colors
- ✓ Movement works on passable terrain
- ✓ Blocked terrain prevents movement
- ✓ Slow terrain reduces mobility
- ✓ Combat works correctly
- ✓ Unit stats feel balanced
- ✓ Vision ranges work

**Visual Polish:**
- ✓ Map looks visually appealing
- ✓ Terrain types are distinguishable
- ✓ Team colors are clear
- ✓ UI elements work

### Balance Testing

**Unit Balance:**
- Can any unit type dominate easily?
- Are mobility values appropriate?
- Is attack/defense ratio fair?
- Do ranges create interesting tactics?

**Map Balance:**
- Does either team have unfair advantage?
- Are there multiple viable strategies?
- Is the map size appropriate for unit count?
- Do terrain features create interesting choices?

### Iteration

1. Play test scenarios
2. Note issues (too easy, too hard, boring, etc.)
3. Return to editor
4. Adjust units, terrain, or placements
5. Save and test again
6. Repeat until fun!

---

## Complete Game Creation Workflow

### Quick Start (30 minutes)

1. **Setup** (5 min)
   - Edit `game_config.json` - change game name
   - Edit team names and colors

2. **Content** (10 min)
   - Keep default terrains or create 1-2 custom ones
   - Keep default units or create 1-2 custom ones

3. **Map** (10 min)
   - Open editor
   - Create small map (12×10)
   - Paint simple terrain
   - Place 4-6 units per team

4. **Test** (5 min)
   - Launch game
   - Play through scenario
   - Note any issues

### Full Game Creation (3-5 hours)

1. **Planning** (30 min)
   - Game theme and setting
   - Team concepts and strategies
   - Terrain types needed
   - Unit roster design

2. **Configuration** (15 min)
   - Edit `game_config.json` completely
   - Set up teams, colors, turn order
   - Configure UI preferences

3. **Terrain Creation** (30 min)
   - Create 6-10 terrain types
   - Test different passability combinations
   - Ensure visual distinctiveness

4. **Unit Creation** (1 hour)
   - Create 5-10 unit types
   - Design roles (melee, ranged, scout, etc.)
   - Balance stats and costs
   - Consider unit synergies

5. **Map Design** (1-2 hours)
   - Create 3-5 scenarios
   - Vary map sizes and layouts
   - Design terrain features
   - Balance unit placements
   - Create difficulty progression

6. **Testing** (1 hour)
   - Play all scenarios
   - Balance testing
   - Bug checking
   - Polish and refinement

7. **Iteration** (ongoing)
   - Gather feedback
   - Adjust balance
   - Add more content
   - Refine gameplay

---

## File Structure Reference

### Your Game Files

```
strategy/
├── game_config.json           # Game settings and teams
├── resources/
│   ├── terrains.json          # Custom terrain types
│   ├── units/                 # Unit definitions
│   │   ├── warrior.json
│   │   ├── mage.json
│   │   └── ...
│   └── maps/                  # Scenarios
│       ├── map_1.txt          # Scenario 1 terrain
│       ├── units_1.json       # Scenario 1 units
│       ├── map_2.txt          # Scenario 2 terrain
│       ├── units_2.json       # Scenario 2 units
│       └── ...
```

### What Each File Does

**`game_config.json`**
- Game identity (name, version, author)
- Window settings (size, FPS)
- Teams configuration
- UI colors and fonts
- Victory conditions
- Gameplay settings

**`resources/terrains.json`**
- All terrain type definitions
- Name, color, passability, icon
- Loaded dynamically by game and editor
- Edit visually in editor or manually in JSON

**`resources/units/{name}.json`**
- Individual unit type definition
- Stats, abilities, projectile settings
- One file per unit type
- Edit visually in editor or manually in JSON

**`resources/maps/map_N.txt`**
- Terrain layout for scenario N
- Grid dimensions on first line
- Passability values (0/1/2) for each cell
- Maps terrain types to passability for gameplay

**`resources/maps/units_N.json`**
- Unit placements for scenario N
- Organized by team
- Unit type, position (row, col)
- Scenario metadata

---

## Tips for Different Game Types

### Strategy-Heavy Games
- Larger maps (25×25+)
- More unit types (8-12)
- Complex terrain with choke points
- Varied unit abilities and roles
- Resource management considerations

### Action-Focused Games
- Smaller maps (10×15)
- Fewer unit types (4-6)
- Open terrain for movement
- Fast-paced combat
- Quick scenarios

### Puzzle/Tactical Games
- Small to medium maps
- Specific unit placements for puzzles
- Unique terrain layouts
- One solution or limited solutions
- Progressive difficulty

### Campaign Games
- Story-driven scenario progression
- Increasing difficulty
- Introduce mechanics gradually
- Boss battles or special scenarios
- Victory conditions variety

---

## Troubleshooting

### Game Won't Start
- Check `game_config.json` for syntax errors
- Ensure all teams have unique IDs
- Verify window size values are reasonable

### Terrains Don't Appear
- Check `resources/terrains.json` exists
- Verify JSON syntax is correct
- Colors should be [R, G, B] format
- Passability must be 0, 1, or 2

### Units Don't Load
- Check unit JSON files exist in `resources/units/`
- Verify all required fields are present
- Numeric values should be integers (except hit_chance, damage_std)
- Unit names must match filenames (lowercase)

### Scenarios Don't Load
- Check map and units files exist
- Map dimensions must match actual grid
- Unit positions must be within grid bounds
- Team IDs must match those in game_config.json

### Balance Issues
- Use editor to quickly adjust unit stats
- Test different terrain layouts
- Vary starting positions
- Adjust mobility and range values

---

## Advanced: Creating a Complete Game Package

### Structure Your Game

```
my_strategy_game/
├── README.md                  # Your game's readme
├── game_config.json           # Game configuration
├── main.py                    # Game launcher
├── editor.py                  # Content editor
├── resources/
│   ├── terrains.json
│   ├── units/
│   ├── maps/
│   ├── icons/                 # Optional: custom sprites
│   └── projectiles/           # Optional: custom projectiles
├── docs/
│   ├── GAMEPLAY.md            # How to play your game
│   └── CREDITS.md             # Attribution
└── venv/                      # Python environment
```

### Distribute Your Game

1. **Document everything:**
   - Write clear README with installation
   - Explain your game's unique mechanics
   - Provide strategy tips

2. **Include all files:**
   - game_config.json with your settings
   - All terrain and unit definitions
   - All scenario files
   - Any custom sprites (if added)

3. **Test on clean install:**
   - Clone to new directory
   - Install dependencies
   - Verify everything loads

4. **Share:**
   - Upload to GitHub
   - Share on itch.io or similar
   - Provide screenshots/videos
   - Get feedback and iterate!

---

## Next Steps

### Enhance Your Game

**Add More Content:**
- More unit types with unique abilities
- More terrain varieties
- More scenarios with diverse layouts
- Campaign with story progression

**Visual Polish:**
- Custom sprites for units/terrain
- Animated effects
- Sound effects and music
- UI improvements

**Gameplay Features:**
- Custom victory conditions
- Special unit abilities
- Resource systems
- Upgrades/progression
- Multiplayer modes

### Learn the Engine

See documentation for:
- **CONFIGURATION.md** - Config system details
- **EDITOR.md** - Editor features and controls
- **GAMEPLAY.md** - Game mechanics
- **UNIT_SYSTEM.md** - Unit design details

---

## Example: Complete Fantasy Game

Let's create a simple fantasy game from scratch!

### 1. Game Config

Edit `game_config.json`:
```json
{
  "game": {
    "name": "Kingdom Clash",
    "version": "1.0.0",
    "author": "You",
    "description": "Fantasy tactical battles"
  },
  "teams": [
    {
      "id": 0,
      "name": "Kingdom Forces",
      "color": [100, 150, 255],
      "player_controlled": true
    },
    {
      "id": 1,
      "name": "Orc Horde",
      "color": [150, 50, 50],
      "player_controlled": false
    }
  ]
}
```

### 2. Create Terrains

In editor (T mode → + Create New Terrain):
- Plains: RGB(120, 200, 100), Easy
- Forest: RGB(40, 100, 40), Slow
- Mountains: RGB(120, 100, 80), Blocked
- River: RGB(80, 120, 200), Blocked

### 3. Create Units

In editor (U mode → + Create New Unit):
- knight: HP:120, Att:30, Def:10, Range:1, Mobility:2
- archer: HP:70, Att:35, Def:3, Range:4, Mobility:2
- wizard: HP:60, Att:45, Def:2, Range:5, Mobility:2
- scout: HP:50, Att:20, Def:2, Range:1, Mobility:4

### 4. Create First Battle

- Grid: 15×12
- Terrain: Mostly plains with forest strip in middle, mountains on edges
- Units:
  - Kingdom (left): 2 knights, 3 archers, 1 wizard
  - Orcs (right): 3 warriors, 2 archers, 1 shaman
- Save as scenario 1

### 5. Test and Refine

- Launch game
- Play scenario
- Adjust if too easy/hard
- Create more scenarios!

You now have a complete custom game! 🎮

---

## Support and Resources

**Documentation:**
- `docs/EDITOR.md` - Editor guide
- `docs/CONFIGURATION.md` - Config details
- `docs/GAMEPLAY.md` - Game mechanics

**Get Help:**
- Check existing unit/terrain JSON files for examples
- Experiment in the editor - it's safe!
- Test frequently while creating
- Start small and expand

**Community:**
- Share your games!
- Get feedback from players
- Learn from other creators
- Contribute improvements

---

## Conclusion

You now have all the tools to create complete custom strategy games:

✅ **Visual editor** for terrain and units
✅ **JSON configuration** for game settings
✅ **Map designer** for scenarios
✅ **No coding required** for content creation
✅ **Easy iteration and testing**

Start creating, test often, and most importantly - **have fun**! 🎮

The Strategy Game Engine makes it easy to bring your tactical game ideas to life. Whether you're creating a fantasy epic, sci-fi warfare, historical battles, or something completely unique, the tools are here to help you build it.

Good luck with your game creation! 🚀
