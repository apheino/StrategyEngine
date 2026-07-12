# Dynamic Scenario Discovery

## Overview

Combat Alley 2000 now automatically discovers and displays all available scenarios in the game menu. No code changes are needed to add new scenarios to the menu - just create the scenario files and they'll appear automatically!

## How It Works

### Skirmish Mode

The skirmish menu dynamically scans the `resources/maps/` directory for available scenarios:

1. **Discovers scenarios** by finding `map_N.txt` files
2. **Validates** that corresponding `units_N.json` files exist
3. **Reads descriptions** from the units JSON files
4. **Generates menu** with all discovered scenarios

### Campaign Mode

Campaign mode uses story files (`resources/stories/scenario_N.json`) to link scenarios together in sequence. It still works the same way - starting with scenario 1 and progressing through the story.

## What's Shown in the Menu

The skirmish menu displays:

```
Scenario 1: The First Battle - Tutorial
Scenario 2: Rectangular map (15x8) with obstacles and catapult
Scenario 3: Large battle on 200x100 map
Scenario 4: Structure test scenario
Scenario 99: Test Scenario
Back to Main Menu
```

Each entry shows:
- **Scenario number** (from filename)
- **Description** (from units JSON file)

## Adding New Scenarios

### Method 1: Using the Editor

1. Open the editor: `python editor.py`
2. Press `[` or `]` to select scenario number
3. Create your map and place units/structures
4. Press `S` to save
5. **Done!** Scenario automatically appears in menu

### Method 2: Manual Creation

1. Create `resources/maps/map_N.txt` (your map terrain)
2. Create `resources/maps/units_N.json` (your units)
3. Add a description field:
   ```json
   {
     "scenario": N,
     "description": "Your scenario description",
     "teams": [ /* ... */ ]
   }
   ```
4. **Done!** Restart the game to see it in the menu

## Scenario Numbering

- **Standard scenarios**: 1, 2, 3, 4...
- **Test scenarios**: 99 (or any high number)
- **Custom scenarios**: Use any number 1-999

The menu sorts scenarios numerically.

## Technical Details

### Discovery Function

```python
def get_available_scenarios():
    """
    Scan resources/maps directory for available scenarios
    
    Returns:
        list: [{\"number\": int, \"description\": str}, ...]
    """
```

This function:
1. Scans for `map_*.txt` files
2. Extracts scenario number from filename
3. Checks for matching `units_*.json` file
4. Reads description from JSON
5. Returns sorted list of scenarios

### Menu Generation

```python
def init_scenario_select_menu():
    """Initialize scenario selection menu (dynamically discovers available scenarios)"""
```

This function:
1. Calls `get_available_scenarios()`
2. Creates menu button for each scenario
3. Sets action to `scenario_N` format
4. Adds "Back to Main Menu" button

### Action Handler

```python
elif action.startswith(\"scenario_\"):
    # Handle dynamic scenario selection
    scenario_num = int(action.split('_')[1])
    start_scenario(scenario_num, campaign_mode=False)
```

This code:
1. Detects `scenario_N` actions
2. Extracts scenario number
3. Launches the scenario

## Benefits

### Before (Hardcoded)
- Only 3 scenarios in menu
- Had to edit code to add scenarios
- Scenario 4, 99, etc. were "hidden"
- Required programmer knowledge

### After (Dynamic)
- All scenarios automatically shown
- No code changes needed
- Editor creates scenarios instantly
- User-friendly content creation

## Examples

### Creating a New Scenario

```bash
# In editor:
python editor.py
# Press ] to go to scenario 5
# Create your map
# Press S to save
# Quit editor
# Start game → Scenario 5 appears in menu!
```

### Custom Description

Edit `resources/maps/units_5.json`:
```json
{
  "scenario": 5,
  "description": "Desert Ambush - Defend the Oasis",
  "teams": [ /* ... */ ]
}
```

Menu will show:
```
Scenario 5: Desert Ambush - Defend the Oasis
```

## Limitations

- Requires both `map_N.txt` and `units_N.json` files
- Scenario numbers must be integers
- Description limited to one line in menu display
- No scenario thumbnails (yet)

## Future Enhancements

Possible improvements:
- [ ] Scenario thumbnails/previews
- [ ] Difficulty ratings
- [ ] Filter scenarios by tags
- [ ] Sort by name, number, or date
- [ ] Show scenario stats (map size, unit count)
- [ ] "Featured" scenarios section
- [ ] Scenario categories (tutorial, challenge, etc.)

## Testing

The system has been tested with:
- ✅ Scenarios 1, 2, 3 (original)
- ✅ Scenario 4 (structures test)
- ✅ Scenario 99 (test scenario)
- ✅ Missing scenarios (gaps handled correctly)
- ✅ Invalid filenames (ignored gracefully)

All tests passing!

---

**See Also:**
- [EDITOR.md](EDITOR.md) - Editor usage guide
- [NEW_GAME_GUIDE.md](NEW_GAME_GUIDE.md) - Creating custom scenarios
- [STRUCTURES.md](STRUCTURES.md) - Using structures in scenarios
