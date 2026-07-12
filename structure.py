"""
Structure module for Combat Alley 2000.
Handles structures (buildings) that can be placed on the map, owned by teams,
and destroyed in combat.
"""

import pygame
import json
import os
from pathlib import Path


class Structure:
    """
    Represents a structure (building) on the battlefield.
    
    Structures are stationary objects that:
    - Block movement (unpassable when alive)
    - Can be attacked and destroyed
    - May be owned by a team
    - Make cells passable once destroyed
    """
    
    def __init__(self, structure_type, row, col, team=None, cell_size=64):
        """
        Initialize a structure.
        
        Args:
            structure_type: Name of the structure type (e.g., "headquarters")
            row: Grid row position
            col: Grid column position
            team: Team ID that owns this structure (None for neutral)
            cell_size: Size of grid cells for rendering
        """
        self.type = structure_type
        self.row = row
        self.col = col
        self.team = team
        self.cell_size = cell_size
        
        # Load structure stats from definition file
        self._load_definition()
        
        # Initialize state
        self.health = self.max_health
        self.is_alive = True
        
        # Load sprite
        self._load_sprite()
        
    def _load_definition(self):
        """Load structure stats from JSON definition file."""
        definition_path = Path(f"resources/structures/{self.type}.json")
        
        if not definition_path.exists():
            # Default values if definition not found
            print(f"Warning: Structure definition not found: {definition_path}")
            self.max_health = 100
            self.defense = 5
            self.is_base = False
            self.description = "Unknown structure"
            return
        
        with open(definition_path, 'r') as f:
            data = json.load(f)
            self.max_health = data.get('max_health', 100)
            self.defense = data.get('defense', 5)
            self.is_base = data.get('is_base', False)
            self.description = data.get('description', '')
    
    def _load_sprite(self):
        """Load structure sprite image."""
        sprite_path = Path(f"resources/structures/{self.type}.png")
        
        if not sprite_path.exists():
            # Create a placeholder surface if sprite not found
            self.sprite = pygame.Surface((self.cell_size, self.cell_size))
            self.sprite.fill((100, 100, 100))  # Gray placeholder
            print(f"Warning: Structure sprite not found: {sprite_path}")
        else:
            try:
                self.sprite = pygame.image.load(str(sprite_path)).convert_alpha()
                self.sprite = pygame.transform.scale(self.sprite, (self.cell_size, self.cell_size))
            except pygame.error as e:
                print(f"Error loading structure sprite {sprite_path}: {e}")
                self.sprite = pygame.Surface((self.cell_size, self.cell_size))
                self.sprite.fill((100, 100, 100))
    
    def take_damage(self, damage):
        """
        Apply damage to the structure.
        
        Args:
            damage: Raw damage amount (will be reduced by defense)
            
        Returns:
            Actual damage taken after defense
        """
        if not self.is_alive:
            return 0
        
        # Calculate actual damage (minimum 1)
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        
        # Check if destroyed
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"{self.type} at ({self.row}, {self.col}) destroyed!")
        
        return actual_damage
    
    def get_health_percentage(self):
        """Get health as a percentage (0-100)."""
        return int((self.health / self.max_health) * 100)
    
    def is_passable(self):
        """
        Check if the cell with this structure is passable.
        
        Returns:
            True if destroyed (passable), False if alive (blocks movement)
        """
        return not self.is_alive
    
    def draw(self, screen, camera_x=0, camera_y=0, zoom=1.0):
        """
        Draw the structure on screen.
        
        Args:
            screen: Pygame surface to draw on
            camera_x: Camera X offset for panning
            camera_y: Camera Y offset for panning
            zoom: Zoom level (1.0 = 100%)
        """
        if not self.is_alive:
            return  # Don't draw destroyed structures
        
        # Calculate screen position with camera and zoom
        scaled_size = int(self.cell_size * zoom)
        screen_x = int((self.col * self.cell_size - camera_x) * zoom)
        screen_y = int((self.row * self.cell_size - camera_y) * zoom)
        
        # Scale sprite for zoom
        if zoom != 1.0:
            scaled_sprite = pygame.transform.scale(self.sprite, (scaled_size, scaled_size))
        else:
            scaled_sprite = self.sprite
        
        # Draw structure sprite
        screen.blit(scaled_sprite, (screen_x, screen_y))
        
        # Draw health bar if damaged
        if self.health < self.max_health:
            self._draw_health_bar(screen, screen_x, screen_y, scaled_size)
        
        # Draw team indicator if owned
        if self.team is not None:
            self._draw_team_indicator(screen, screen_x, screen_y, scaled_size)
    
    def _draw_health_bar(self, screen, x, y, size):
        """Draw health bar above structure."""
        bar_width = size
        bar_height = max(4, int(size * 0.08))
        bar_y = y - bar_height - 2
        
        # Background (red)
        pygame.draw.rect(screen, (255, 0, 0), (x, bar_y, bar_width, bar_height))
        
        # Health (green)
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, (0, 255, 0), (x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, (0, 0, 0), (x, bar_y, bar_width, bar_height), 1)
    
    def _draw_team_indicator(self, screen, x, y, size):
        """Draw team color indicator in corner."""
        indicator_size = max(8, int(size * 0.2))
        
        # Team colors (should match game_config.json)
        team_colors = {
            0: (0, 100, 255),    # Blue
            1: (255, 50, 50),    # Red
            2: (50, 255, 50),    # Green
            3: (255, 255, 50),   # Yellow
        }
        
        color = team_colors.get(self.team, (128, 128, 128))
        
        # Draw colored square in top-left corner
        pygame.draw.rect(screen, color, (x, y, indicator_size, indicator_size))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, indicator_size, indicator_size), 1)
    
    def __repr__(self):
        """String representation for debugging."""
        team_str = f"Team {self.team}" if self.team is not None else "Neutral"
        status = "Alive" if self.is_alive else "Destroyed"
        return f"<Structure {self.type} at ({self.row},{self.col}) {team_str} {status} HP:{self.health}/{self.max_health}>"


def load_structure_types():
    """
    Load all available structure types from resources/structures/.
    
    Returns:
        List of structure type names (without .json extension)
    """
    structures_dir = Path("resources/structures")
    
    if not structures_dir.exists():
        return []
    
    structure_types = []
    for json_file in structures_dir.glob("*.json"):
        structure_types.append(json_file.stem)
    
    return sorted(structure_types)
