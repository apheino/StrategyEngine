"""
Projectile class for ranged attacks

This module implements projectiles that travel from an attacker to a target.
Projectiles are used for ranged attacks (e.g., arrows from archers) and provide
visual feedback for attacks with range > 1.

Key features:
- Smooth interpolation from start to target position
- Automatic rotation to face direction of travel
- Speed-based animation (faster units shoot faster projectiles)
- Automatic damage application on hit
"""
import pygame
import os
import math
import random


class Projectile:
    """
    Represents a projectile in flight from attacker to target
    
    Projectiles animate ranged attacks by traveling from the attacker's position
    to the target's position over time. When the projectile reaches the target,
    damage is automatically applied.
    
    Attributes:
        start_pos (tuple): Starting position as (row, col) in grid coordinates
        target_pos (tuple): Target position as (row, col) in grid coordinates  
        progress (float): Progress from 0.0 (at start) to 1.0 (at target)
        speed (float): Projectile flight speed in grid cells per second
        sprite (Surface): Pygame image to display for this projectile
        attacker (Unit): Unit that fired the projectile
        target (Unit): Target unit that will take damage
        damage (int): Damage to apply when projectile hits
        is_complete (bool): True if projectile has reached target
        angle (float): Rotation angle in degrees for sprite rendering
    """
    
    def __init__(self, start_pos, target_pos, speed, sprite_name, attacker, target, base_damage, offset=(0.0, 0.0), hit_chance=1.0):
        """
        Initialize a new projectile
        
        The projectile will travel from start_pos to target_pos at the given speed.
        The sprite is automatically loaded and rotated to face the direction of travel.
        Each projectile has an independent hit/miss roll.
        Damage has Gaussian variance on successful hit.
        
        Args:
            start_pos (tuple): Starting (row, col) in grid coordinates
            target_pos (tuple): Target (row, col) in grid coordinates
            speed (float): Flight speed in grid cells per second
            sprite_name (str): Name of projectile sprite file (e.g., "arrow")
            attacker (Unit): Unit that fired the projectile
            target (Unit): Target unit that will receive damage
            base_damage (int): Base damage value (will vary with Gaussian distribution)
            offset (tuple): Visual offset (row_offset, col_offset) for spread effect
            hit_chance (float): Probability of hitting (0.0 to 1.0)
        """
        # Position and movement
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.progress = 0.0  # 0.0 = at start, 1.0 = at target
        self.offset = offset  # Visual offset for volley spread
        
        # Speed with fallback default
        self.speed = speed if speed > 0 else 8.0  # Default to 8 cells/second
        
        # Combat references
        self.attacker = attacker  # Who shot this projectile
        self.target = target      # Who will be hit
        self.base_damage = base_damage  # Base damage (will have variance applied on hit)
        self.is_complete = False  # True when projectile reaches target
        
        # Hit/miss determination (rolled once when projectile is created)
        self.hit_chance = hit_chance
        self.is_hit = random.random() < hit_chance  # True if this projectile will hit
        
        # Visual representation
        self.sprite = self.load_sprite(sprite_name)
        
        # Calculate rotation angle to face direction of travel
        # atan2 gives angle in radians, we convert to degrees
        # Angle is from start to target
        delta_row = target_pos[0] - start_pos[0]
        delta_col = target_pos[1] - start_pos[1]
        self.angle = math.degrees(math.atan2(delta_row, delta_col))
    
    def load_sprite(self, sprite_name):
        """
        Load projectile sprite image from file
        
        Looks for the sprite in resources/projectiles/ directory.
        Expects PNG files with the given name.
        
        Args:
            sprite_name (str): Name of sprite file without extension (e.g., "arrow")
        
        Returns:
            pygame.Surface: Loaded sprite image, or None if loading fails
        """
        filepath = f"resources/projectiles/{sprite_name}.png"
        
        if os.path.exists(filepath):
            try:
                return pygame.image.load(filepath)
            except pygame.error as e:
                print(f"Error loading projectile sprite {filepath}: {e}")
        
        return None
    
    def update(self, dt):
        """
        Update projectile position and check for target reached
        
        Moves the projectile along its path based on speed and delta time.
        When the projectile reaches the target (progress >= 1.0), damage
        is automatically applied to the target unit.
        
        Args:
            dt (float): Delta time in seconds since last update
        
        Returns:
            bool: True if projectile has reached target, False otherwise
        """
        # If already complete, no further updates needed
        if self.is_complete:
            return True
        
        # Calculate Manhattan distance between start and target (in grid cells)
        # This is the total distance the projectile must travel
        distance = abs(self.target_pos[0] - self.start_pos[0]) + \
                  abs(self.target_pos[1] - self.start_pos[1])
        
        if distance > 0:
            # Calculate how much progress to make this frame
            # progress_per_second = speed (cells/sec) / distance (cells)
            # This gives us the fraction of the journey per second
            progress_per_second = self.speed / distance
            self.progress += progress_per_second * dt
            
            # Check if projectile has reached or passed the target
            if self.progress >= 1.0:
                self.progress = 1.0
                self.is_complete = True
                
                # Apply damage to target on impact (only if hit, with Gaussian variance)
                if self.is_hit and self.target and self.target.is_alive:
                    # Calculate variable damage using attacker's method
                    actual_damage = self.attacker.calculate_variable_damage(self.base_damage)
                    self.actual_damage = actual_damage  # Store for logging
                    self.target.take_damage(actual_damage)
                
                return True
        else:
            # Start and target are the same cell - instant hit with variable damage
            self.is_complete = True
            if self.is_hit and self.target and self.target.is_alive:
                actual_damage = self.attacker.calculate_variable_damage(self.base_damage)
                self.actual_damage = actual_damage
                self.target.take_damage(actual_damage)
            return True
        
        return False
    
    def get_current_position(self):
        """
        Get current interpolated position of projectile in flight
        
        Calculates the projectile's current position by linearly interpolating
        between start_pos and target_pos based on current progress value.
        
        Returns:
            tuple: Current position as (row, col) with float values
        """
        start_row, start_col = self.start_pos
        target_row, target_col = self.target_pos
        
        # Linear interpolation: current = start + (target - start) * progress
        current_row = start_row + (target_row - start_row) * self.progress
        current_col = start_col + (target_col - start_col) * self.progress
        
        # Apply visual offset for spread effect
        current_row += self.offset[0]
        current_col += self.offset[1]
        
        return (current_row, current_col)
    
    def draw(self, screen, cell_size, zoom, offset_x, offset_y, screen_width, screen_height):
        """
        Draw the projectile sprite at its current position
        
        Renders the projectile as a scaled and rotated sprite. The sprite size
        scales with zoom level, and the sprite is rotated to face the direction
        of travel.
        
        Args:
            screen (Surface): Pygame surface to draw on
            cell_size (int): Base size of grid cells in pixels
            zoom (float): Current zoom level (1.0 = normal, >1 = zoomed in)
            offset_x (int): Camera horizontal offset in pixels
            offset_y (int): Camera vertical offset in pixels
            screen_width (int): Width of screen (unused, kept for interface consistency)
            screen_height (int): Height of screen (unused, kept for interface consistency)
        """
        # Don't draw if no sprite or projectile has completed its flight
        if not self.sprite or self.is_complete:
            return
        
        # Get current interpolated position in grid coordinates
        row, col = self.get_current_position()
        
        # Calculate scaled cell size based on zoom
        scaled_cell_size = cell_size * zoom
        
        # Convert grid position to screen position
        # Position at center of cell for projectile
        x = col * scaled_cell_size + offset_x + scaled_cell_size / 2
        y = row * scaled_cell_size + offset_y + scaled_cell_size / 2
        
        # Scale sprite based on zoom
        # Projectiles are rendered at 50% of cell size (smaller than units)
        # Minimum size of 8 pixels to remain visible when zoomed out
        scale_factor = zoom * 0.5
        sprite_size = max(8, int(16 * scale_factor))
        scaled_sprite = pygame.transform.scale(self.sprite, (sprite_size, sprite_size))
        
        # Rotate sprite to face direction of travel
        # Negative angle because pygame rotation is counter-clockwise
        rotated_sprite = pygame.transform.rotate(scaled_sprite, -self.angle)
        
        # Center the rotated sprite at the calculated position
        # Rotation changes sprite dimensions, so we recalculate the rect
        sprite_rect = rotated_sprite.get_rect(center=(x, y))
        
        # Draw the rotated, scaled sprite
        screen.blit(rotated_sprite, sprite_rect)
