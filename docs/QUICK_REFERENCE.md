# Game Creation Quick Reference

Quick checklist for creating or modifying games with the Strategy Game Engine.

## ✅ Complete Game Creation Checklist

### Phase 1: Configuration (15 min)
- [ ] Edit `game_config.json`
  - [ ] Change game name
  - [ ] Set author and version
  - [ ] Configure window size (default: 1280×720)
  - [ ] Define teams (at least 2)
  - [ ] Set team colors
  - [ ] Configure player_controlled flags
  - [ ] Set turn_order

### Phase 2: Terrain Types (30 min)
- [ ] Launch editor: `python editor.py`
- [ ] Press `T` for Terrain mode
- [ ] Click "+ Create New Terrain" for each terrain type:
  - [ ] Define terrain name
  - [ ] Set passability (Easy/Slow/Blocked)
  - [ ] Choose color (RGB values)
  - [ ] Set icon name
  - [ ] Save terrain
- [ ] Verify in `resources/terrains.json`

**Minimum:** 3-4 terrain types (grass, obstacle, slow terrain)

### Phase 3: Unit Types (1 hour)
- [ ] In editor, press `U` for Units mode
- [ ] Click "+ Create New Unit Type" for each unit:
  - [ ] Enter unit name
  - [ ] Set health (HP)
  - [ ] Set attack power
  - [ ] Set defense
  - [ ] Set attack range (1=melee, 2+=ranged)
  - [ ] Set mobility (movement per turn)
  - [ ] Set vision range
  - [ ] Save unit
- [ ] Verify in `resources/units/{name}.json`

**Minimum:** 3-4 unit types (melee, ranged, scout)

### Phase 4: Maps & Scenarios (1-2 hours)
- [ ] Design first map:
  - [ ] Press `N` for new scenario
  - [ ] Set grid size with `+/-` keys
  - [ ] Press `T` and paint terrain
  - [ ] Press `U` and place units for team 0
  - [ ] Place units for team 1
  - [ ] Press `S` to save
- [ ] Create additional scenarios (recommended: 3-5)
- [ ] Verify files in `resources/maps/`

**Minimum:** 1 scenario with balanced forces

### Phase 5: Testing & Balance (1 hour)
- [ ] Launch game: `python main.py`
- [ ] Test main menu
- [ ] Play each scenario
- [ ] Check balance:
  - [ ] Can both sides win?
  - [ ] Are units useful?
  - [ ] Is terrain interesting?
  - [ ] Is difficulty appropriate?
- [ ] Return to editor and adjust as needed
- [ ] Re-test until satisfied

### Phase 6: Polish & Documentation (optional)
- [ ] Write README for your game
- [ ] Document unique mechanics
- [ ] Add gameplay tips
- [ ] Create screenshots
- [ ] Test on clean install
- [ ] Share with others!

---

## 🎯 Minimum Viable Game

**What you need to start playing:**

1. ✅ `game_config.json` with:
   - Game name
   - 2 teams defined
   
2. ✅ `resources/terrains.json` with:
   - At least 1 terrain type (auto-created on first editor run)
   
3. ✅ `resources/units/` with:
   - At least 1 unit type (soldier.json provided by default)
   
4. ✅ `resources/maps/` with:
   - map_1.txt (terrain layout)
   - units_1.json (unit placements)

**Total time:** ~30 minutes with defaults

---

## 🔧 Common Modifications

### Change Game Name
**File:** `game_config.json`
```json
"game": {
  "name": "Your Game Name Here"
}
```

### Add New Team
**File:** `game_config.json`
```json
{
  "id": 2,
  "name": "Third Faction",
  "color": [100, 255, 100],
  "player_controlled": false,
  "turn_order": 2
}
```

### Quick Terrain
**Editor:** `T` → `+ Create New Terrain`
- Name: `lava`
- Passability: `Block`
- Color: `255, 100, 0`
- Icon: `lava`
- Save!

### Quick Unit
**Editor:** `U` → `+ Create New Unit Type`
- Name: `mage`
- Health: `70`
- Attack: `40`
- Defense: `2`
- Range: `4`
- Mobility: `2`
- Vision: `6`
- Save!

### Resize Map
**Editor:** 
- Press `+` to increase size
- Press `-` to decrease size
- Range: 5×5 to 50×50

---

## 📁 File Locations

| Content | File Location | Edit Method |
|---------|--------------|-------------|
| Game name/settings | `game_config.json` | Text editor |
| Teams | `game_config.json` | Text editor |
| Terrain types | `resources/terrains.json` | Editor or text |
| Unit types | `resources/units/{name}.json` | Editor or text |
| Map layouts | `resources/maps/map_N.txt` | Editor |
| Unit placements | `resources/maps/units_N.json` | Editor |

---

## 🎮 Editor Quick Keys

| Key | Action |
|-----|--------|
| **T** | Terrain mode |
| **U** | Units mode |
| **S** | Save scenario |
| **L** | Load scenario |
| **N** | New scenario (clear all) |
| **+** | Increase grid size |
| **-** | Decrease grid size |
| **1-6** | Quick select terrain 1-6 |
| **Left Click** | Place terrain/unit |
| **Right Click** | Erase terrain/unit |
| **Q** or **ESC** | Quit editor |

---

## 🚀 Launch Commands

```bash
# Launch game
python main.py

# Launch editor
python editor.py

# With virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
python main.py            # or editor.py
```

---

## 💡 Quick Tips

### Balance
- **Melee units:** High HP, low mobility, range 1
- **Ranged units:** Low HP, high attack, range 3-5
- **Scouts:** Low combat, high mobility and vision
- **Heavy units:** Very high HP/defense, mobility 1-2

### Map Design
- **Small maps:** 10×10 to 15×12 for quick battles
- **Medium maps:** 20×15 to 25×20 for standard play
- **Large maps:** 30×25+ for epic battles
- Use terrain for choke points and cover

### Testing
- Play as both sides to check balance
- Try different strategies
- Adjust if one side dominates
- Iterate quickly with editor

### Content Growth
1. Start with 3 units, 4 terrains, 1 map
2. Test and balance
3. Add 1-2 more of each
4. Create 2-3 more scenarios
5. Repeat until satisfied

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Game won't start | Check `game_config.json` syntax |
| Terrains not loading | Verify `resources/terrains.json` exists |
| Units not loading | Check `resources/units/{name}.json` files |
| Map won't load | Verify map and units files for scenario N |
| Editor crashes | Check terminal for error messages |
| Units too strong/weak | Use editor to adjust stats quickly |

---

## 📚 Full Documentation

For comprehensive guides, see:
- **NEW_GAME_GUIDE.md** - Complete game creation walkthrough
- **EDITOR.md** - Editor features and detailed instructions
- **CONFIGURATION.md** - Game configuration system
- **GAMEPLAY.md** - Game mechanics and rules
- **UNIT_SYSTEM.md** - Unit design and balance

---

## 🎯 Success Metrics

**You've created a playable game when:**
- ✅ Game launches without errors
- ✅ Custom game name displays
- ✅ Terrain paints correctly in scenarios
- ✅ Units appear with correct team colors
- ✅ Combat and movement work
- ✅ Game is fun to play!

**You've created a polished game when:**
- ✅ Multiple unique scenarios
- ✅ Diverse unit roster (5+ types)
- ✅ Varied terrain (6+ types)
- ✅ Balanced gameplay
- ✅ Clear visual distinction
- ✅ Documentation for players

---

## 🎨 Theme Templates

### Fantasy
- **Terrains:** Plains, Forest, Mountains, River, Castle
- **Units:** Knight, Archer, Wizard, Dragon, Scout
- **Colors:** Blues, greens, browns, gold

### Sci-Fi
- **Terrains:** Metal, Energy Field, Void, Platform, Hazard
- **Units:** Marine, Sniper, Mech, Drone, Artillery
- **Colors:** Grays, blues, neon accents

### Historical
- **Terrains:** Grassland, Woods, Hills, River, Road
- **Units:** Spearman, Bowman, Cavalry, Trebuchet, General
- **Colors:** Earth tones, reds, blues

### Post-Apocalyptic
- **Terrains:** Rubble, Wasteland, Radiation, Ruins, Debris
- **Units:** Survivor, Raider, Mutant, Scavenger, Veteran
- **Colors:** Browns, grays, toxic greens

---

## 🔄 Iteration Cycle

1. **Create** - Make content in editor
2. **Test** - Play in game
3. **Evaluate** - What works? What doesn't?
4. **Adjust** - Modify in editor
5. **Repeat** - Until it's fun!

**Average cycle:** 5-10 minutes per iteration

---

## ✨ You're Ready!

With this reference and the tools provided, you can create complete custom strategy games. Start simple, test often, and expand as you go. Have fun creating! 🎮
