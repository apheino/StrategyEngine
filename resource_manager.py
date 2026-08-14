"""
Resource Manager for centralized asset loading and caching

This module provides a singleton resource manager that handles:
- Loading and caching of all game assets (sprites, sounds, data files)
- Consistent error handling for missing resources
- Memory-efficient asset reuse
- Clear separation between resource loading and game logic

Benefits:
- Avoids duplicate loading of assets
- Centralized error handling and logging
- Easy to add new resource types
- Validates resources at startup
"""

import pygame
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from functools import lru_cache


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResourceManager:
    """
    Singleton resource manager for loading and caching game assets
    
    Handles all resource loading with caching to avoid redundant file I/O.
    Provides consistent error handling and fallback for missing resources.
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern - only one instance exists"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize resource manager (only runs once due to singleton)"""
        if self._initialized:
            return
        
        self._initialized = True
        
        # Cache dictionaries for loaded resources
        self._image_cache: Dict[str, pygame.Surface] = {}
        self._json_cache: Dict[str, Any] = {}
        self._sound_cache: Dict[str, pygame.mixer.Sound] = {}
        
        # Resource directories
        self.base_path = Path("resources")
        self.units_path = self.base_path / "units"
        self.structures_path = self.base_path / "structures"
        self.projectiles_path = self.base_path / "projectiles"
        self.terrains_path = self.base_path / "terrains.json"
        self.icons_path = self.base_path / "icons"
        self.maps_path = self.base_path / "maps"
        self.stories_path = self.base_path / "stories"
        self.campaigns_path = self.base_path / "campaigns"
        
        logger.info("Resource Manager initialized")
    
    def clear_cache(self):
        """Clear all cached resources (useful for reloading)"""
        self._image_cache.clear()
        self._json_cache.clear()
        self._sound_cache.clear()
        logger.info("Resource cache cleared")
    
    # ========================================
    # IMAGE LOADING
    # ========================================
    
    def load_image(self, path: Path, size: Optional[tuple] = None, 
                   alpha: bool = True) -> Optional[pygame.Surface]:
        """
        Load an image from file with caching
        
        Args:
            path: Path to image file
            size: Optional (width, height) to scale to
            alpha: Use alpha channel (transparency)
            
        Returns:
            Pygame Surface or None if loading fails
        """
        # Create cache key including size
        cache_key = f"{path}_{size}"
        
        # Return cached version if available
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]
        
        # Load image
        if not path.exists():
            logger.warning(f"Image not found: {path}")
            return self._create_placeholder_surface(size or (64, 64))
        
        try:
            if alpha:
                surface = pygame.image.load(str(path)).convert_alpha()
            else:
                surface = pygame.image.load(str(path)).convert()
            
            # Scale if size specified
            if size:
                surface = pygame.transform.scale(surface, size)
            
            # Cache and return
            self._image_cache[cache_key] = surface
            return surface
            
        except pygame.error as e:
            logger.error(f"Failed to load image {path}: {e}")
            return self._create_placeholder_surface(size or (64, 64))
    
    def _create_placeholder_surface(self, size: tuple) -> pygame.Surface:
        """Create a placeholder surface for missing images"""
        surface = pygame.Surface(size)
        surface.fill((100, 100, 100))  # Gray
        
        # Draw an X to indicate missing
        pygame.draw.line(surface, (255, 0, 0), (0, 0), size, 2)
        pygame.draw.line(surface, (255, 0, 0), (size[0], 0), (0, size[1]), 2)
        
        return surface
    
    def load_unit_sprite(self, unit_type: str, animation: str, health: int, 
                        frame: int, size: int = 64) -> Optional[pygame.Surface]:
        """
        Load a unit animation sprite
        
        Args:
            unit_type: Type of unit (e.g., "sloop")
            animation: Animation name (e.g., "idle", "move", "attack")
            health: Health percentage (100, 50, 25) for health-based variants
            frame: Frame number
            size: Sprite size in pixels
            
        Returns:
            Pygame Surface or None
        """
        # Construct sprite filename
        filename = f"{unit_type}_{animation}_{health}_{frame}.png"
        path = self.units_path / filename
        
        return self.load_image(path, (size, size))
    
    def load_structure_sprite(self, structure_type: str, 
                             size: int = 64) -> Optional[pygame.Surface]:
        """
        Load a structure sprite
        
        Args:
            structure_type: Type of structure (e.g., "naval_fort")
            size: Sprite size in pixels
            
        Returns:
            Pygame Surface or None
        """
        path = self.structures_path / f"{structure_type}.png"
        return self.load_image(path, (size, size))
    
    def load_projectile_sprite(self, projectile_type: str, 
                               size: int = 32) -> Optional[pygame.Surface]:
        """
        Load a projectile sprite
        
        Args:
            projectile_type: Type of projectile (e.g., "cannonball")
            size: Sprite size in pixels
            
        Returns:
            Pygame Surface or None
        """
        path = self.projectiles_path / f"{projectile_type}.png"
        return self.load_image(path, (size, size))
    
    def load_terrain_icon(self, icon_name: str, 
                         size: int = 64) -> Optional[pygame.Surface]:
        """
        Load a terrain icon
        
        Args:
            icon_name: Name of terrain icon
            size: Icon size in pixels
            
        Returns:
            Pygame Surface or None
        """
        path = self.icons_path / f"{icon_name}.png"
        return self.load_image(path, (size, size))
    
    # ========================================
    # JSON DATA LOADING
    # ========================================
    
    def load_json(self, path: Path) -> Optional[Dict]:
        """
        Load JSON data from file with caching
        
        Args:
            path: Path to JSON file
            
        Returns:
            Parsed JSON dict or None if loading fails
        """
        # Return cached version if available
        cache_key = str(path)
        if cache_key in self._json_cache:
            return self._json_cache[cache_key]
        
        # Load JSON
        if not path.exists():
            logger.warning(f"JSON file not found: {path}")
            return None
        
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            
            # Cache and return
            self._json_cache[cache_key] = data
            return data
            
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load JSON {path}: {e}")
            return None
    
    def load_unit_definition(self, unit_type: str) -> Optional[Dict]:
        """Load unit definition from JSON"""
        path = self.units_path / f"{unit_type}.json"
        return self.load_json(path)
    
    def load_structure_definition(self, structure_type: str) -> Optional[Dict]:
        """Load structure definition from JSON"""
        path = self.structures_path / f"{structure_type}.json"
        return self.load_json(path)
    
    def load_terrain_definitions(self) -> Optional[Dict]:
        """Load terrain type definitions"""
        return self.load_json(self.terrains_path)
    
    def load_scenario_story(self, scenario_number: int) -> Optional[Dict]:
        """Load scenario story/narrative"""
        path = self.stories_path / f"scenario_{scenario_number}.json"
        return self.load_json(path)
    
    def load_campaign(self, campaign_id: str) -> Optional[Dict]:
        """Load campaign definition"""
        path = self.campaigns_path / f"{campaign_id}.json"
        return self.load_json(path)
    
    def load_units_file(self, filename: str) -> Optional[Dict]:
        """Load unit placement file"""
        path = self.maps_path / filename
        return self.load_json(path)
    
    # ========================================
    # TEXT FILE LOADING
    # ========================================
    
    def load_map_file(self, map_file: str) -> Optional[list]:
        """
        Load map terrain data from text file
        
        Args:
            map_file: Name of map file (e.g., "map_1.txt")
            
        Returns:
            List of map rows or None if loading fails
        """
        path = self.maps_path / map_file
        
        if not path.exists():
            logger.warning(f"Map file not found: {path}")
            return None
        
        try:
            with open(path, 'r') as f:
                return [line.strip() for line in f.readlines()]
        except IOError as e:
            logger.error(f"Failed to load map {path}: {e}")
            return None
    
    # ========================================
    # VALIDATION
    # ========================================
    
    def validate_resources(self) -> bool:
        """
        Validate that critical resources exist
        
        Returns:
            True if all critical resources are present
        """
        critical_paths = [
            self.base_path,
            self.units_path,
            self.structures_path,
            self.maps_path,
            self.terrains_path,
        ]
        
        missing = []
        for path in critical_paths:
            if not path.exists():
                missing.append(path)
        
        if missing:
            logger.error(f"Missing critical resources: {missing}")
            return False
        
        logger.info("Resource validation passed")
        return True


# Global singleton instance
resource_manager = ResourceManager()
