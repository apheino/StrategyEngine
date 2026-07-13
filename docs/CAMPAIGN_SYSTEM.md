# Campaign System Documentation

## Overview

The campaign system allows for flexible definition of campaigns that chain scenarios together in a specific order. Campaigns are defined separately from scenarios, allowing:
- Multiple campaigns to reuse the same scenarios in different orders
- Easy creation of new campaigns without modifying scenario files
- Clear separation between gameplay (scenarios) and narrative flow (campaigns)

## File Structure

```
resources/
├── campaigns/           # Campaign definition files
│   ├── main_campaign.json
│   ├── tutorial_campaign.json
│   └── ...
├── stories/            # Scenario narrative files
│   ├── scenario_1.json
│   ├── scenario_2.json
│   └── ...
└── maps/               # Scenario gameplay files
    ├── map_1.txt
    ├── units_1.json
    └── ...
```

## Campaign Definition Format

Campaign files are JSON files in `resources/campaigns/` with the following structure:

```json
{
  "id": "campaign_id",
  "name": "Campaign Display Name",
  "description": "Brief description shown in campaign selection",
  "scenarios": [
    {
      "scenario_number": 1,
      "required": true,
      "unlock_condition": null,
      "briefing_override": ["Optional", "Custom briefing lines"]
    },
    {
      "scenario_number": 2,
      "required": true,
      "unlock_condition": "complete_1"
    }
  ],
  "victory_text": [
    "Campaign Complete!",
    "",
    "Congratulations message..."
  ]
}
```

### Fields

#### Root Level
- **id** (string, required): Unique identifier for the campaign. Used as filename (without .json)
- **name** (string, required): Display name shown in menus
- **description** (string, optional): Description shown in campaign selection menu
- **scenarios** (array, required): List of scenarios in order
- **victory_text** (array, optional): Text shown when campaign is completed

#### Scenario Entry
- **scenario_number** (int, required): Which scenario to load (references map_X.txt and units_X.json)
- **required** (bool, optional): Whether this scenario must be completed to progress
- **unlock_condition** (string, optional): Condition to unlock this scenario (e.g., "complete_1")
- **briefing_override** (array, optional): Custom intro text for this scenario (overrides scenario_X.json)

## Scenario Definition Format

Scenario story files in `resources/stories/scenario_X.json` define narrative text:

```json
{
  "scenario_number": 1,
  "title": "Scenario Title",
  "intro_text": [
    "Mission briefing line 1",
    "Mission briefing line 2",
    "",
    "Objective: ..."
  ],
  "victory_text": [
    "Success message"
  ],
  "defeat_text": [
    "Failure message"
  ]
}
```

**Note**: The old `next_scenario` field has been removed. Campaign flow is now defined in campaign files.

## Campaign Flow

### Starting a Campaign

1. Player selects "Select Campaign" from main menu
2. Game shows list of available campaigns from `resources/campaigns/`
3. Player selects a campaign
4. Game loads campaign and starts first scenario

### During Campaign

1. Player completes a scenario
2. Victory screen shows campaign progress (e.g., "Scenario 2 of 3")
3. "Continue Campaign" button advances to next scenario
4. Repeat until all scenarios complete

### Completing a Campaign

1. Player completes final scenario
2. Game displays campaign victory text
3. Player returns to main menu

### Exiting Campaign

- Selecting "Main Menu" from any screen ends the current campaign
- Campaign progress is not saved (starts over next time)

## Code Integration

### Campaign Module (`campaign.py`)

The `campaign` module provides:

```python
# Load a specific campaign
campaign_obj = campaign.load_campaign('main_campaign')

# Get all available campaigns
campaigns = campaign.get_available_campaigns()
# Returns: [(id, name, description), ...]

# Start a campaign (sets as current)
campaign.start_campaign('main_campaign')

# Get current active campaign
current = campaign.get_current_campaign()

# Check scenario flow
current_scenario = current.get_current_scenario()
next_scenario = current.get_next_scenario()
is_done = current.is_complete()

# Mark scenario complete and advance
current.mark_scenario_complete(scenario_number)

# End campaign
campaign.end_campaign()
```

### Main Game Integration

Main menu flow:
1. `init_main_menu()` shows "Select Campaign" button
2. `init_campaign_select_menu()` shows available campaigns
3. `execute_menu_action("start_campaign_X")` starts selected campaign
4. `start_campaign(campaign_id)` loads campaign and starts first scenario

Victory screen flow:
1. `init_victory_menu()` checks if campaign has next scenario
2. Shows "Continue Campaign" button if more scenarios exist
3. `execute_menu_action("next_scenario")` advances campaign
4. If campaign complete, shows campaign victory text

## Creating New Campaigns

### Example 1: Linear Campaign

```json
{
  "id": "story_mode",
  "name": "The Liberation War",
  "description": "Follow the Blue Alliance through 3 major battles",
  "scenarios": [
    {"scenario_number": 1, "required": true, "unlock_condition": null},
    {"scenario_number": 2, "required": true, "unlock_condition": "complete_1"},
    {"scenario_number": 3, "required": true, "unlock_condition": "complete_2"}
  ],
  "victory_text": [
    "The war is won!",
    "Freedom is secured."
  ]
}
```

### Example 2: Tutorial Campaign (Reusing Scenarios)

```json
{
  "id": "tutorial",
  "name": "Training Missions",
  "description": "Learn the game mechanics",
  "scenarios": [
    {
      "scenario_number": 1,
      "required": true,
      "unlock_condition": null,
      "briefing_override": [
        "TUTORIAL 1: Basic Combat",
        "Learn to move and attack."
      ]
    },
    {
      "scenario_number": 4,
      "required": true,
      "unlock_condition": "complete_1",
      "briefing_override": [
        "TUTORIAL 2: Siege Warfare",
        "Learn to attack structures."
      ]
    }
  ],
  "victory_text": ["Training complete!"]
}
```

### Example 3: Challenge Campaign

```json
{
  "id": "gauntlet",
  "name": "The Gauntlet",
  "description": "Face all scenarios in sequence without defeat",
  "scenarios": [
    {"scenario_number": 1, "required": true},
    {"scenario_number": 2, "required": true},
    {"scenario_number": 3, "required": true},
    {"scenario_number": 4, "required": true},
    {"scenario_number": 99, "required": true}
  ],
  "victory_text": [
    "ULTIMATE VICTORY!",
    "You have conquered the gauntlet!"
  ]
}
```

## Benefits of New System

### Flexibility
- Create multiple campaigns without modifying scenarios
- Reuse scenarios in different orders
- Different campaigns can provide different context for same battles

### Modularity
- Scenarios are standalone and reusable
- Campaign files are simple and easy to edit
- Clear separation of concerns

### Extensibility
- Easy to add new campaigns
- Support for future features (branching paths, optional scenarios)
- Campaign progress tracking can be expanded

### Designer-Friendly
- Non-programmers can create campaigns by editing JSON
- Campaign structure is clear and self-documenting
- No code changes needed to add campaigns

## Future Enhancements

Possible future additions:
- Campaign save/load system
- Branching paths based on victory conditions
- Optional side scenarios
- Persistent unit progression between scenarios
- Campaign-specific modifiers (difficulty, special rules)
- Achievement tracking per campaign
