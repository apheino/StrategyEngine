"""
Game configuration loader and manager

This module loads game configuration from game_config.json and provides
centralized access to all game settings. This makes the engine configurable
without code changes and supports multiple games using the same engine.

Usage:
    from config import game_config
    
    window_title = game_config.get_game_name()
    team_color = game_config.get_team_color(0)
"""

import json
from pathlib import Path


class GameConfig:
    """
    Game configuration manager
    
    Loads and provides access to game configuration from game_config.json.
    Falls back to sensible defaults if config file is missing or incomplete.
    """
    
    def __init__(self, config_file='game_config.json'):
        """
        Initialize configuration manager
        
        Args:
            config_file (str): Path to game configuration JSON file
        """
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from JSON file with fallback defaults"""
        default_config = {
            'game': {
                'name': 'Strategy Game',
                'version': '1.0.0',
                'author': 'Unknown',
                'description': 'A turn-based strategy game',
                'window_width': 1280,
                'window_height': 720,
                'fps': 60
            },
            'teams': [
                {
                    'id': 0,
                    'name': 'Team 1',
                    'color': [100, 150, 255],
                    'player_controlled': True,
                    'turn_order': 0
                },
                {
                    'id': 1,
                    'name': 'Team 2',
                    'color': [255, 100, 100],
                    'player_controlled': False,
                    'turn_order': 1
                }
            ],
            'ui': {
                'colors': {
                    'background': [30, 90, 150],
                    'grid_line': [128, 128, 128],
                    'selection_highlight': [255, 255, 0]
                }
            },
            'gameplay': {
                'default_cell_size': 64,
                'turn_start_team': 0
            }
        }
        
        config_path = Path(self.config_file)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge loaded config with defaults (loaded takes precedence)
                    return self._deep_merge(default_config, loaded_config)
            except Exception as e:
                print(f"Warning: Error loading {self.config_file}: {e}")
                print("Using default configuration")
                return default_config
        else:
            print(f"Warning: {self.config_file} not found, using defaults")
            return default_config
    
    def _deep_merge(self, base, override):
        """Deep merge two dictionaries, with override taking precedence"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    # ========================================
    # GAME METADATA
    # ========================================
    
    def get_game_name(self):
        """Get the game name"""
        return self.config['game'].get('name', 'Strategy Game')
    
    def get_game_version(self):
        """Get the game version"""
        return self.config['game'].get('version', '1.0.0')
    
    def get_game_author(self):
        """Get the game author"""
        return self.config['game'].get('author', 'Unknown')
    
    def get_window_size(self):
        """Get window dimensions as (width, height) tuple"""
        return (
            self.config['game'].get('window_width', 1280),
            self.config['game'].get('window_height', 720)
        )
    
    def get_fps(self):
        """Get target frames per second"""
        return self.config['game'].get('fps', 60)
    
    # ========================================
    # TEAM CONFIGURATION
    # ========================================
    
    def get_teams(self):
        """Get list of all team configurations"""
        return self.config.get('teams', [])
    
    def get_team_config(self, team_id):
        """
        Get configuration for a specific team
        
        Args:
            team_id (int): Team ID to look up
            
        Returns:
            dict: Team configuration or None if not found
        """
        for team in self.get_teams():
            if team['id'] == team_id:
                return team
        return None
    
    def get_team_name(self, team_id):
        """Get team name by ID"""
        team = self.get_team_config(team_id)
        return team['name'] if team else f'Team {team_id}'
    
    def get_team_color(self, team_id):
        """Get team color as RGB tuple"""
        team = self.get_team_config(team_id)
        return tuple(team['color']) if team else (128, 128, 128)
    
    def is_player_controlled(self, team_id):
        """Check if team is player-controlled"""
        team = self.get_team_config(team_id)
        return team['player_controlled'] if team else (team_id == 0)
    
    def get_turn_order(self):
        """Get list of team IDs in turn order"""
        teams = sorted(self.get_teams(), key=lambda t: t.get('turn_order', t['id']))
        return [t['id'] for t in teams]
    
    # ========================================
    # UI CONFIGURATION
    # ========================================
    
    def get_ui_color(self, color_name, default=(128, 128, 128)):
        """
        Get UI color by name
        
        Args:
            color_name (str): Name of the color (e.g., 'background', 'grid_line')
            default (tuple): Default RGB tuple if color not found
            
        Returns:
            tuple: RGB color tuple
        """
        colors = self.config.get('ui', {}).get('colors', {})
        color = colors.get(color_name, default)
        return tuple(color) if isinstance(color, list) else color
    
    def get_font_size(self, size_name):
        """
        Get font size by name
        
        Args:
            size_name (str): 'large_size', 'medium_size', or 'small_size'
            
        Returns:
            int: Font size in pixels
        """
        fonts = self.config.get('ui', {}).get('fonts', {})
        sizes = {
            'large_size': 48,
            'medium_size': 36,
            'small_size': 24
        }
        return fonts.get(size_name, sizes.get(size_name, 24))
    
    def get_health_bar_config(self):
        """Get health bar configuration"""
        return self.config.get('ui', {}).get('health_bar', {
            'height': 4,
            'border_color': [255, 255, 255],
            'healthy_color': [0, 255, 0],
            'damaged_color': [255, 255, 0],
            'critical_color': [255, 0, 0],
            'healthy_threshold': 0.6,
            'critical_threshold': 0.3
        })
    
    # ========================================
    # GAMEPLAY CONFIGURATION
    # ========================================
    
    def get_default_cell_size(self):
        """Get default grid cell size"""
        return self.config.get('gameplay', {}).get('default_cell_size', 64)
    
    def get_starting_team(self):
        """Get which team goes first"""
        return self.config.get('gameplay', {}).get('turn_start_team', 0)
    
    def get_default_victory_condition(self):
        """Get default victory condition type"""
        return self.config.get('victory_conditions', {}).get('default_type', 'elimination')
    
    # ========================================
    # CONTROLS
    # ========================================
    
    def get_control_key(self, action):
        """Get key binding for an action"""
        controls = self.config.get('controls', {})
        return controls.get(action, 'UNKNOWN')


# Global configuration instance
# Import this in other modules: from config import game_config
game_config = GameConfig()
