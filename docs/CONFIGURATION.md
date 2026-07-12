# Game Configuration System

## Overview

The game configuration system allows you to customize the game without modifying code. All game settings, team configurations, UI colors, and gameplay parameters are stored in `game_config.json`.

This makes the engine reusable for different games and allows easy modding.

## Configuration File: `game_config.json`

### Structure

```json
{
  "game": { ... },       // Game metadata and window settings
  "teams": [ ... ],      // Team definitions
  "ui": { ... },         // UI colors and fonts
  "gameplay": { ... },   // Gameplay defaults
  "victory_conditions": { ... },  // Victory settings
  "controls": { ... }    // Key bindings
}
```

### Game Metadata

```json
"game": {
  "name": "Combat Alley 2000",      // Window title
  "version": "1.0.0",                // Version string
  "author": "Strategy Engine Team",  // Author name
  "description": "A tactical...",    // Description
  "window_width": 1280,              // Window width in pixels
  "window_height": 720,              // Window height in pixels
  "fps": 60                          // Target frames per second
}
```

### Team Configuration

Teams are defined in an array. Each team has:

```json
"teams": [
  {
    "id": 0,                          // Unique team ID
    "name": "Blue Alliance",          // Display name
    "description": "Player forces",   // Description
    "color": [100, 150, 255],        // RGB color
    "player_controlled": true,        // Is this team player-controlled?
    "turn_order": 0                   // Position in turn sequence
  },
  {
    "id": 1,
    "name": "Red Empire",
    "color": [255, 100, 100],
    "player_controlled": false,       // AI-controlled
    "turn_order": 1
  }
]
```

**Key Features:**
- Support for 2+ teams
- Multiple player-controlled teams possible
- Custom turn order
- Team-specific colors for UI

### UI Configuration

```json
"ui": {
  "colors": {
    "background": [30, 90, 150],
    "grid_line": [128, 128, 128],
    "selection_highlight": [255, 255, 0],
    "valid_move": [0, 255, 0],
    "attack_range": [255, 0, 0],
    // ... more colors
  },
  "fonts": {
    "large_size": 48,
    "medium_size": 36,
    "small_size": 24
  },
  "health_bar": {
    "height": 4,
    "border_color": [255, 255, 255],
    "healthy_color": [0, 255, 0],
    "damaged_color": [255, 255, 0],
    "critical_color": [255, 0, 0]
  }
}
```

### Gameplay Settings

```json
"gameplay": {
  "default_cell_size": 64,         // Grid cell size in pixels
  "default_fog_enabled": true,     // Start with fog of war on
  "turn_start_team": 0             // Which team goes first
}
```

### Victory Conditions

```json
"victory_conditions": {
  "default_type": "elimination",   // Currently only "elimination" supported
  "check_each_turn": true          // Check for victory after each turn
}
```

## Using the Configuration

### In Python Code

```python
from config import game_config

# Get game name
title = game_config.get_game_name()

# Get team information
team_name = game_config.get_team_name(0)
team_color = game_config.get_team_color(0)
is_player = game_config.is_player_controlled(0)

# Get UI colors
bg_color = game_config.get_ui_color('background')
selection_color = game_config.get_ui_color('selection_highlight')

# Get turn order
turn_order = game_config.get_turn_order()  # Returns [0, 1] or custom order
```

### API Reference

**Game Metadata:**
- `get_game_name()` → str
- `get_game_version()` → str
- `get_window_size()` → (width, height)
- `get_fps()` → int

**Team Management:**
- `get_teams()` → list of team dicts
- `get_team_config(team_id)` → team dict or None
- `get_team_name(team_id)` → str
- `get_team_color(team_id)` → (r, g, b)
- `is_player_controlled(team_id)` → bool
- `get_turn_order()` → list of team IDs

**UI Configuration:**
- `get_ui_color(color_name, default)` → (r, g, b)
- `get_font_size(size_name)` → int
- `get_health_bar_config()` → dict

**Gameplay:**
- `get_default_cell_size()` → int
- `get_starting_team()` → int

## Creating Different Games

You can create completely different games by creating different `game_config.json` files:

### Example: Medieval Fantasy Game

```json
{
  "game": {
    "name": "Kingdoms at War",
    "version": "1.0.0"
  },
  "teams": [
    {
      "id": 0,
      "name": "Kingdom of Light",
      "color": [255, 215, 0],
      "player_controlled": true
    },
    {
      "id": 1,
      "name": "Shadow Empire",
      "color": [75, 0, 130],
      "player_controlled": false
    },
    {
      "id": 2,
      "name": "Neutral Traders",
      "color": [200, 200, 200],
      "player_controlled": false
    }
  ]
}
```

### Example: Sci-Fi 4-Team FFA

```json
{
  "game": {
    "name": "Stellar Conflict",
    "version": "1.0.0"
  },
  "teams": [
    {
      "id": 0,
      "name": "Earth Federation",
      "color": [0, 100, 255],
      "player_controlled": true,
      "turn_order": 0
    },
    {
      "id": 1,
      "name": "Mars Colony",
      "color": [255, 50, 50],
      "player_controlled": true,
      "turn_order": 1
    },
    {
      "id": 2,
      "name": "Jupiter Alliance",
      "color": [255, 200, 100],
      "player_controlled": false,
      "turn_order": 2
    },
    {
      "id": 3,
      "name": "Alien Invaders",
      "color": [0, 255, 0],
      "player_controlled": false,
      "turn_order": 3
    }
  ]
}
```

## Benefits

**For Game Developers:**
- Change game name/branding instantly
- Adjust colors and UI without code changes
- Experiment with different team setups
- Easy balancing and tweaking

**For Modders:**
- Create total conversions by changing config
- Add more teams without code knowledge
- Customize UI to match theme
- Support for community mods

**For the Engine:**
- Reusable across multiple games
- Clean separation of data and code
- Easy to test different configurations
- Foundation for future features (campaigns, mods)

## Future Extensions

The configuration system is designed to support:
- Custom victory conditions (capture points, survival, escort)
- Campaign definitions
- Mod system
- Difficulty settings
- Game mode variations
- Localization support

## Fallback Behavior

If `game_config.json` is missing or has errors:
- The engine uses built-in defaults
- A warning is printed to console
- The game still runs normally

This ensures the game is robust even if the config file is corrupted.
