"""
Unit class for game units with animations, combat, and state management

This module implements the Unit class which represents individual game units.
Each unit has:
- Stats (health, attack, defense, mobility, range)
- Animations (idle, move, attack, hurt, death with health-based variants)
- State (position, team, alive/dying, active/inactive)
- Movement system (smooth interpolated movement)
- Combat system (attack, take damage, death)
- Health-based visual states (different animations at 100%, 50%, 25% health)

Animation System:
- Health-based variants: Idle, move, and attack have different animations at full/damaged/critical health
- Naming convention: {unit}_{animation}_{health%}_{frame}.png
  - Example: soldier_idle_100_0.png (full health), soldier_idle_50_0.png (50% health)
- Non-health animations: hurt and death don't have health variants
- Automatic selection: Unit automatically uses appropriate animation based on current health percentage

Combat System:
- Damage formula: max(1, attacker.attack_power - defender.defense)
- Ranged vs melee: projectile_speed > 0 = ranged attack with projectile
- Attack animations trigger on attack, return to idle when complete
- Hurt animation plays briefly when taking damage
- Death animation plays fully before unit is removed
"""
import pygame
import os
import math
import random
import json


class Unit:
    """
    Game unit with stats, animations, and combat capabilities
    
    Represents a single unit on the battlefield (soldier, archer, knight, etc.).
    Handles all unit behavior including movement, combat, animations, and state management.
    
    Key Features:
    - File-based attributes loaded from resources/units/{unit_type}.txt
    - Sprite-based animations with automatic health-based variant selection
    - Smooth interpolated movement between grid cells
    - Turn-based action system (can act once per turn)
    - Directional facing and rotation
    - Health bars with color coding
    - Projectile support for ranged attacks
    
    Attributes:
        unit_type (str): Type identifier (e.g., "soldier", "archer", "knight")
        team (int): Team/player number (0=player, 1=enemy, 2+=other)
        position (tuple): Current grid position as (row, col)
        health (int): Current hit points
        max_health (int): Maximum hit points
        attack_power (int): Base damage dealt
        defense (int): Damage reduction (armor)
        attack_range (int): Attack range in grid cells (Manhattan distance)
        mobility (int): Current movement points this turn
        max_mobility (int): Maximum movement points per turn
        speed (float): Movement animation speed (cells per second)
        projectile_speed (float): Projectile flight speed (0=melee, >0=ranged)
    """
    
    def __init__(self, unit_type="soldier", team=0, position=(0, 0)):
        """
        Initialize a new unit with default or file-loaded attributes
        
        Loads unit attributes from file, initializes animation system,
        and sets up initial state (alive, active, at starting position).
        
        Args:
            unit_type (str): Type of unit (used for loading attributes and animations)
            team (int): Team/player number (0=player, 1=enemy, 2+=other factions)
            position (tuple): Starting grid position as (row, col)
        """
        # ========================================
        # BASIC IDENTITY
        # ========================================
        
        self.unit_type = unit_type  # "soldier", "archer", "knight", etc.
        self.team = team            # 0 = player, 1 = enemy, 2+ = other
        self.position = position    # (row, col) on grid
        
        # ========================================
        # LOAD ATTRIBUTES FROM FILE
        # ========================================
        
        # Must load attributes before setting health
        # Loads: max_health, attack_power, defense, attack_range, max_mobility, speed, projectile_speed
        self.load_attributes()
        
        # ========================================
        # CURRENT STATE
        # ========================================
        
        # Combat state
        self.health = self.max_health      # Start at full health
        self.mobility = self.max_mobility  # Start with full mobility
        
        # ========================================
        # MOVEMENT STATE
        # ========================================
        
        # Movement animation (smooth interpolation)
        self.is_moving = False                      # True during movement animation
        self.movement_start_pos = position          # Where movement started (row, col)
        self.movement_target_pos = position         # Where movement is going (row, col)
        self.movement_progress = 0.0                # 0.0 to 1.0 (interpolation)
        self.movement_path = [position]             # List of waypoints for pathfinding
        self.movement_waypoint_index = 0            # Current waypoint being moved toward
        
        # ========================================
        # COMBAT ANIMATION STATE
        # ========================================
        
        self.is_attacking = False  # True during attack animation
        self.is_dying = False      # True during death animation
        self.is_hurt = False       # True during damage reaction animation
        
        # ========================================
        # TURN-BASED STATE
        # ========================================
        
        self.is_alive = True   # False when death animation completes
        self.is_active = True  # False after acting (moving or attacking) this turn
        
        # ========================================
        # ANIMATION SYSTEM
        # ========================================
        
        # Animation storage
        self.animations = {}  # Dict: animation_name -> list of pygame.Surface frames
        
        # Health-based animation thresholds
        # List of (health_percent, animation_name) tuples sorted by health descending
        # E.g., [(100, "idle_100"), (50, "idle_50"), (25, "idle_25")]
        self.idle_health_thresholds = []
        self.move_health_thresholds = []
        self.attack_health_thresholds = []
        
        # Current animation state
        self.current_animation = "idle"  # Name of current animation
        self.animation_frame = 0         # Current frame index
        self.animation_speed = 0.1       # Seconds per frame
        self.animation_timer = 0.0       # Time accumulator for frame advance
        
        # ========================================
        # VISUAL PROPERTIES
        # ========================================
        
        # Directional facing
        self.facing_direction = "right"  # "right", "left", "up", "down"
        
        # Rotation (calculated from movement direction)
        # 0° = right, 90° = down, 180° = left, 270° = up
        self.rotation_angle = 0
        
        # Horizontal flipping (used for leftward movement to avoid upside-down appearance)
        self.flip_horizontal = False
        
        # ========================================
        # LOAD ANIMATIONS
        # ========================================
        
        # Load all sprite frames for this unit type
        self.load_animations()
    
    def load_attributes(self):
        """
        Load unit attributes from a JSON file
        
        Expected file: resources/units/{unit_type}.json
        
        Format:
            {
                "name": "Soldier",
                "description": "Balanced infantry unit",
                "max_health": 100,
                "attack_power": 20,
                "defense": 5,
                "attack_range": 1,
                "max_mobility": 3,
                "speed": 2.0,
                ...
            }
        """
        filepath = f"resources/units/{self.unit_type}.json"
        
        # Default attributes (used if file not found)
        default_attributes = {
            'max_health': 100,
            'attack_power': 20,
            'defense': 5,
            'attack_range': 1,
            'max_mobility': 3,
            'speed': 2.0,
            'projectile_speed': 0.0,  # 0 = melee (no projectile), >0 = ranged with projectile
            'projectile_count': 1,  # Number of projectiles fired per attack (1 = single shot, 2+ = volley/battery)
            'hit_chance': 0.90,  # Probability of hitting (0.0 to 1.0, default 90%)
            'damage_std': 2.0,  # Standard deviation for damage variance (Gaussian distribution)
            'fire_type': 'direct'  # 'direct' = needs line of sight, 'indirect' = can fire over obstacles
        }
        
        attributes = default_attributes.copy()
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    # Update attributes with values from JSON
                    for key in attributes.keys():
                        if key in data:
                            attributes[key] = data[key]
                
                print(f"Loaded attributes for {self.unit_type} from {filepath}")
            except Exception as e:
                print(f"Error loading attributes from {filepath}: {e}")
                print(f"Using default attributes for {self.unit_type}")
        else:
            print(f"Attribute file not found: {filepath}. Using default attributes.")
        
        # Set attributes
        self.max_health = attributes['max_health']
        self.attack_power = attributes['attack_power']
        self.defense = attributes['defense']
        self.attack_range = attributes['attack_range']
        self.max_mobility = attributes['max_mobility']
        self.speed = attributes['speed']
        self.projectile_speed = attributes['projectile_speed']
        self.projectile_count = max(1, attributes['projectile_count'])  # Ensure at least 1
        self.hit_chance = max(0.0, min(1.0, attributes['hit_chance']))  # Clamp between 0.0 and 1.0
        self.damage_std = max(0.0, attributes['damage_std'])  # Standard deviation for damage variance
        self.fire_type = attributes['fire_type']  # 'direct' or 'indirect'
    
    def load_animations(self):
        """
        Load animation frames from files
        
        Expected file structure:
        resources/units/{unit_type}_{animation}_{frame}.png
        resources/units/{unit_type}_{animation}_{health%}_{frame}.png
        
        Example:
        resources/units/soldier_idle_0.png (normal idle, 100%)
        resources/units/soldier_idle_50_0.png (damaged idle at 50%)
        resources/units/soldier_move_50_0.png (damaged move at 50%)
        resources/units/soldier_attack_25_0.png (critical attack at 25%)
        resources/units/soldier_hurt_0.png (damage reaction)
        resources/units/soldier_death_0.png (death)
        """
        # Load non-health-dependent animations
        simple_animations = ["death", "hurt"]
        
        for anim_type in simple_animations:
            frames = []
            frame_index = 0
            
            while True:
                filepath = f"resources/units/{self.unit_type}_{anim_type}_{frame_index}.png"
                
                if os.path.exists(filepath):
                    try:
                        frame = pygame.image.load(filepath)
                        frames.append(frame)
                        frame_index += 1
                    except pygame.error as e:
                        print(f"Error loading {filepath}: {e}")
                        break
                else:
                    break
            
            if frames:
                self.animations[anim_type] = frames
                print(f"Loaded {len(frames)} frames for {self.unit_type} {anim_type} animation")
            else:
                if anim_type != "hurt":  # hurt is optional
                    print(f"Warning: No frames found for {self.unit_type} {anim_type}")
        
        # Load health-based animations (idle, move, attack)
        health_based_anims = [
            ("idle", self.idle_health_thresholds),
            ("move", self.move_health_thresholds),
            ("attack", self.attack_health_thresholds)
        ]
        
        health_percents = [100, 75, 50, 25, 10]  # Common thresholds to check
        
        for anim_type, threshold_list in health_based_anims:
            for health_percent in health_percents:
                frames = []
                frame_index = 0
                
                if health_percent == 100:
                    # Normal animation (no percentage in filename)
                    while True:
                        filepath = f"resources/units/{self.unit_type}_{anim_type}_{frame_index}.png"
                        if os.path.exists(filepath):
                            try:
                                frame = pygame.image.load(filepath)
                                frames.append(frame)
                                frame_index += 1
                            except pygame.error as e:
                                print(f"Error loading {filepath}: {e}")
                                break
                        else:
                            break
                else:
                    # Damaged animation (with percentage)
                    while True:
                        filepath = f"resources/units/{self.unit_type}_{anim_type}_{health_percent}_{frame_index}.png"
                        if os.path.exists(filepath):
                            try:
                                frame = pygame.image.load(filepath)
                                frames.append(frame)
                                frame_index += 1
                            except pygame.error as e:
                                print(f"Error loading {filepath}: {e}")
                                break
                        else:
                            break
                
                if frames:
                    anim_name = f"{anim_type}_{health_percent}"
                    self.animations[anim_name] = frames
                    threshold_list.append((health_percent, anim_name))
                    if health_percent == 100:
                        print(f"Loaded {len(frames)} frames for {self.unit_type} {anim_type} animation")
                    else:
                        print(f"Loaded {len(frames)} frames for {self.unit_type} {anim_type}_{health_percent} animation")
            
            # Sort thresholds descending (highest health first)
            threshold_list.sort(reverse=True, key=lambda x: x[0])
            
            # Ensure we have at least one animation of this type
            if not threshold_list:
                print(f"Warning: No {anim_type} animations found for {self.unit_type}")
        
        # Set default animations
        self.animations["idle"] = self.animations.get("idle_100", [])
        self.animations["move"] = self.animations.get("move_100", [])
        self.animations["attack"] = self.animations.get("attack_100", [])
    
    def set_animation(self, animation_name):
        """Change the current animation"""
        if animation_name in self.animations:
            if self.current_animation != animation_name:
                self.current_animation = animation_name
                self.animation_frame = 0
                self.animation_timer = 0.0
    
    def get_idle_animation_for_health(self):
        """
        Get the appropriate idle animation name based on current health percentage
        
        Returns:
            String animation name (e.g., 'idle_100', 'idle_50', 'idle_25')
        """
        if not self.idle_health_thresholds:
            return "idle"
        
        health_percent = (self.health / self.max_health) * 100
        
        # Find the appropriate animation based on health percentage
        for threshold, anim_name in self.idle_health_thresholds:
            if health_percent >= threshold:
                return anim_name
        
        # If health is below all thresholds, use the lowest one
        return self.idle_health_thresholds[-1][1]
    
    def get_move_animation_for_health(self):
        """
        Get the appropriate move animation name based on current health percentage
        
        Returns:
            String animation name (e.g., 'move_100', 'move_50', 'move_25')
        """
        if not self.move_health_thresholds:
            return "move"
        
        health_percent = (self.health / self.max_health) * 100
        
        for threshold, anim_name in self.move_health_thresholds:
            if health_percent >= threshold:
                return anim_name
        
        return self.move_health_thresholds[-1][1]
    
    def get_attack_animation_for_health(self):
        """
        Get the appropriate attack animation name based on current health percentage
        
        Returns:
            String animation name (e.g., 'attack_100', 'attack_50', 'attack_25')
        """
        if not self.attack_health_thresholds:
            return "attack"
        
        health_percent = (self.health / self.max_health) * 100
        
        for threshold, anim_name in self.attack_health_thresholds:
            if health_percent >= threshold:
                return anim_name
        
        return self.attack_health_thresholds[-1][1]
    
    def set_idle_animation(self):
        """Set the appropriate idle animation based on current health"""
        idle_anim = self.get_idle_animation_for_health()
        self.set_animation(idle_anim)
    
    def set_move_animation(self):
        """Set the appropriate move animation based on current health"""
        move_anim = self.get_move_animation_for_health()
        self.set_animation(move_anim)
    
    def set_attack_animation(self):
        """Set the appropriate attack animation based on current health"""
        attack_anim = self.get_attack_animation_for_health()
        self.set_animation(attack_anim)
    
    def update(self, dt):
        """
        Update unit state
        
        Args:
            dt: Delta time in seconds
        """
        # Update movement animation (with waypoint support)
        if self.is_moving:
            # Calculate distance for current segment
            distance = abs(self.movement_target_pos[0] - self.movement_start_pos[0]) + \
                      abs(self.movement_target_pos[1] - self.movement_start_pos[1])
            
            if distance > 0:
                # Progress per second: speed / distance
                progress_per_second = self.speed / distance
                self.movement_progress += progress_per_second * dt
                
                # Check if reached current waypoint
                if self.movement_progress >= 1.0:
                    # Reached current waypoint
                    self.position = self.movement_target_pos
                    
                    # Check if there are more waypoints
                    if self.movement_waypoint_index < len(self.movement_path) - 1:
                        # Move to next waypoint
                        self.movement_waypoint_index += 1
                        self.movement_start_pos = self.movement_path[self.movement_waypoint_index - 1]
                        self.movement_target_pos = self.movement_path[self.movement_waypoint_index]
                        self.movement_progress = 0.0
                        
                        # Update rotation for new segment
                        start_row, start_col = self.movement_start_pos
                        target_row, target_col = self.movement_target_pos
                        delta_row = target_row - start_row
                        delta_col = target_col - start_col
                        
                        if delta_row != 0 or delta_col != 0:
                            angle_radians = math.atan2(delta_row, delta_col)
                            self.rotation_angle = math.degrees(angle_radians)
                            self.flip_horizontal = (self.rotation_angle > 90 or self.rotation_angle < -90)
                    else:
                        # Reached final destination
                        self.movement_progress = 1.0
                        self.is_moving = False
                        self.set_idle_animation()
            else:
                # No distance, already at target
                self.is_moving = False
                self.set_idle_animation()
        
        # Update hurt animation
        if self.is_hurt:
            if self.current_animation.startswith("hurt") and self.current_animation in self.animations:
                frames = self.animations[self.current_animation]
                # Check if hurt animation has completed
                if self.animation_frame >= len(frames) - 1:
                    # Hurt animation finished, return to appropriate idle
                    self.is_hurt = False
                    self.set_idle_animation()
        
        # Update attack animation
        if self.is_attacking:
            if self.current_animation.startswith("attack") and self.current_animation in self.animations:
                frames = self.animations[self.current_animation]
                # Check if attack animation has completed
                if self.animation_frame >= len(frames) - 1:
                    # Attack animation finished, return to idle
                    self.is_attacking = False
                    self.set_idle_animation()
        
        # Update death animation
        if self.is_dying:
            if self.current_animation.startswith("death") and self.current_animation in self.animations:
                frames = self.animations[self.current_animation]
                # Check if death animation has completed
                if self.animation_frame >= len(frames) - 1:
                    # Death animation finished, mark unit as dead
                    self.is_alive = False
        
        # Update animation frames
        if self.current_animation in self.animations:
            self.animation_timer += dt
            
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0.0
                frames = self.animations[self.current_animation]
                
                # For attack, hurt, and death animations, don't loop - stop at last frame
                if (self.is_attacking and self.current_animation.startswith("attack")) or \
                   (self.is_dying and self.current_animation.startswith("death")) or \
                   (self.is_hurt and self.current_animation.startswith("hurt")):
                    if self.animation_frame < len(frames) - 1:
                        self.animation_frame += 1
                else:
                    # Normal looping for other animations
                    self.animation_frame = (self.animation_frame + 1) % len(frames)
    
    def get_current_position(self):
        """
        Get the current visual position (interpolated during movement)
        
        Returns:
            (row, col) tuple with float values for smooth animation
        """
        if self.is_moving:
            # Interpolate between start and target
            start_row, start_col = self.movement_start_pos
            target_row, target_col = self.movement_target_pos
            
            current_row = start_row + (target_row - start_row) * self.movement_progress
            current_col = start_col + (target_col - start_col) * self.movement_progress
            
            return (current_row, current_col)
        else:
            return self.position
    
    def get_current_frame(self):
        """Get the current animation frame surface"""
        if self.current_animation in self.animations:
            frames = self.animations[self.current_animation]
            if frames:
                return frames[self.animation_frame]
        return None
    
    def draw(self, screen, x, y, cell_size):
        """
        Draw the unit at a screen position
        
        Args:
            screen: Pygame surface to draw on
            x, y: Screen coordinates (not grid coordinates)
            cell_size: Size of grid cell in pixels
        """
        frame = self.get_current_frame()
        
        if frame:
            # Scale frame to cell size
            scaled_frame = pygame.transform.scale(frame, (int(cell_size), int(cell_size)))
            
            # Flip horizontally if moving backward on x-axis (leftward)
            # When flipped, adjust rotation angle so x-max points forward
            if self.flip_horizontal:
                scaled_frame = pygame.transform.flip(scaled_frame, True, False)
                # After flip, sprite faces left (180°), so subtract 180° to get relative rotation
                actual_rotation = self.rotation_angle - 180.0
            else:
                actual_rotation = self.rotation_angle
            
            # Rotate the sprite to face movement direction
            if actual_rotation != 0:
                rotated_frame = pygame.transform.rotate(scaled_frame, -actual_rotation)
                # Calculate offset to keep sprite centered after rotation
                offset_x = (rotated_frame.get_width() - scaled_frame.get_width()) / 2
                offset_y = (rotated_frame.get_height() - scaled_frame.get_height()) / 2
                screen.blit(rotated_frame, (x - offset_x, y - offset_y))
            else:
                screen.blit(scaled_frame, (x, y))
        else:
            # Draw placeholder rectangle if no frame available
            color = (255, 0, 0) if self.team == 0 else (0, 0, 255)
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
            pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_size, cell_size), 2)
        
        # Draw health bar above unit
        self.draw_health_bar(screen, x, y, cell_size)
    
    def draw_health_bar(self, screen, x, y, cell_size):
        """
        Draw a health bar above the unit
        
        Args:
            screen: Pygame surface to draw on
            x, y: Screen coordinates of the unit
            cell_size: Size of grid cell in pixels
        """
        # Health bar dimensions
        bar_width = int(cell_size * 0.8)  # 80% of cell width
        bar_height = max(4, int(cell_size * 0.08))  # Scale with cell size, minimum 4px
        bar_x = x + (cell_size - bar_width) / 2  # Center the bar
        bar_y = y - bar_height - 2  # Position above unit with small gap
        
        # Only draw if health bar would be visible
        if bar_y < 0:
            return
        
        # Calculate health percentage
        health_percent = self.health / self.max_health
        
        # Determine bar color based on health percentage
        if health_percent > 0.6:
            bar_color = (0, 255, 0)  # Green
        elif health_percent > 0.3:
            bar_color = (255, 255, 0)  # Yellow
        else:
            bar_color = (255, 0, 0)  # Red
        
        # Draw background (black bar)
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # Draw health fill
        fill_width = int(bar_width * health_percent)
        if fill_width > 0:
            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Draw border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)
    
    def take_damage(self, damage):
        """
        Apply damage to the unit
        
        Damaged units suffer mobility and attack penalties.
        
        Args:
            damage: Raw damage amount before defense
        """
        actual_damage = max(1, damage - self.defense)  # Minimum 1 damage
        self.health -= actual_damage
        
        if self.health <= 0:
            self.health = 0
            self.is_dying = True
            self.set_animation("death")
        else:
            # Play hurt animation if available and unit survives
            if "hurt" in self.animations:
                self.is_hurt = True
                self.set_animation("hurt")
            else:
                # No hurt animation, just update idle to show damaged state
                self.set_idle_animation()
        
        return actual_damage
    
    def get_health_percentage(self):
        """Get current health as a percentage (0.0 to 1.0)"""
        if self.max_health <= 0:
            return 0.0
        return self.health / self.max_health
    
    def get_effective_mobility(self):
        """
        Calculate mobility reduced by damage
        
        Health % -> Mobility Multiplier:
        100-75%: 100% mobility
        75-50%: 85% mobility
        50-25%: 65% mobility
        25-0%: 40% mobility
        
        Returns:
            int: Effective mobility points based on health
        """
        health_pct = self.get_health_percentage()
        
        if health_pct >= 0.75:
            multiplier = 1.0
        elif health_pct >= 0.50:
            multiplier = 0.85
        elif health_pct >= 0.25:
            multiplier = 0.65
        else:
            multiplier = 0.40
        
        return max(1, int(self.max_mobility * multiplier))  # Always at least 1 mobility
    
    def get_effective_projectile_count(self):
        """
        Calculate projectile count reduced by damage for ranged units
        
        Wounded archers fire fewer projectiles (struggle to maintain rapid fire).
        Uses same health tiers as mobility degradation.
        
        Health % -> Projectile Multiplier:
        100-75%: 100% projectiles
        75-50%: 85% projectiles  
        50-25%: 65% projectiles
        25-0%: 40% projectiles
        
        Only applies to ranged units (projectile_speed > 0).
        Melee units always have projectile_count = 1.
        
        Returns:
            int: Effective projectile count based on health (minimum 1)
        """
        # Melee units always fire 1 "projectile" (their melee strike)
        if self.projectile_speed <= 0:
            return 1
        
        health_pct = self.get_health_percentage()
        
        if health_pct >= 0.75:
            multiplier = 1.0
        elif health_pct >= 0.50:
            multiplier = 0.85
        elif health_pct >= 0.25:
            multiplier = 0.65
        else:
            multiplier = 0.40
        
        return max(1, int(self.projectile_count * multiplier))  # Always at least 1 projectile
    
    def get_effective_attack_power(self):
        """
        Calculate attack power reduced by damage
        
        Health % -> Attack Multiplier:
        100-75%: 100% attack
        75-50%: 85% attack
        50-25%: 70% attack
        25-0%: 50% attack
        
        Returns:
            int: Effective attack power based on health
        """
        health_pct = self.get_health_percentage()
        
        if health_pct >= 0.75:
            multiplier = 1.0
        elif health_pct >= 0.50:
            multiplier = 0.85
        elif health_pct >= 0.25:
            multiplier = 0.70
        else:
            multiplier = 0.50
        
        return max(1, int(self.attack_power * multiplier))  # Always at least 1 damage
    
    def calculate_variable_damage(self, base_damage):
        """
        Calculate actual damage using Gaussian distribution
        
        Samples from a normal distribution centered on base_damage with
        standard deviation from damage_std attribute. This creates variance
        in damage output even for successful hits.
        
        Args:
            base_damage (int): Base damage value (median of distribution)
        
        Returns:
            int: Actual damage to apply (at least 1)
        """
        # Sample from Gaussian distribution
        # mu = base_damage (median), sigma = damage_std
        actual_damage = random.gauss(base_damage, self.damage_std)
        
        # Ensure minimum damage of 1
        return max(1, int(actual_damage))
    
    def heal(self, amount):
        """Heal the unit"""
        self.health = min(self.max_health, self.health + amount)
    
    def move_to(self, new_position, path=None):
        """
        Move unit to a new grid position with animation
        
        Args:
            new_position: (row, col) tuple for final destination
            path: Optional list of waypoints [(r1,c1), (r2,c2), ...] to follow
                  If None, moves directly to new_position
        """
        if path and len(path) > 1:
            # Use provided path
            self.movement_path = path
            self.movement_waypoint_index = 1  # Start at waypoint 1 (0 is current position)
            self.movement_start_pos = path[0]
            self.movement_target_pos = path[1]  # First waypoint to move toward
        else:
            # Direct movement (no path provided or single step)
            self.movement_path = [self.position, new_position]
            self.movement_waypoint_index = 1
            self.movement_start_pos = self.position
            self.movement_target_pos = new_position
        
        self.movement_progress = 0.0
        self.is_moving = True
        self.set_move_animation()
        
        # Calculate rotation angle based on first movement segment
        start_row, start_col = self.movement_start_pos
        target_row, target_col = self.movement_target_pos
        delta_row = target_row - start_row
        delta_col = target_col - start_col
        
        # Use atan2 to get actual angle in radians, then convert to degrees
        # atan2(y, x) where x=delta_col (right), y=delta_row (down)
        # Result: 0° = right, 90° = down, 180° = left, -90°/270° = up
        if delta_row != 0 or delta_col != 0:
            angle_radians = math.atan2(delta_row, delta_col)
            self.rotation_angle = math.degrees(angle_radians)
            
            # Flip sprite horizontally when moving backward on x-axis (leftward)
            # This means when the angle indicates leftward movement (> 90° or < -90°)
            self.flip_horizontal = (self.rotation_angle > 90 or self.rotation_angle < -90)
            
            # Update facing direction (approximate for cardinal directions)
            if -45 <= self.rotation_angle < 45:
                self.facing_direction = "right"
            elif 45 <= self.rotation_angle < 135:
                self.facing_direction = "down"
            elif self.rotation_angle >= 135 or self.rotation_angle < -135:
                self.facing_direction = "left"
            else:
                self.facing_direction = "up"
    
    def attack(self, target):
        """
        Attack another unit
        
        Attack power behavior:
        - Melee attacks: Reduced based on current health (wounded units strike weaker)
        - Ranged attacks: Full power (bow/projectile does the work, not affected by wounds)
        
        Projectile count behavior:
        - Ranged attacks: Reduced based on current health (wounded archers fire fewer arrows)
        - Melee attacks: Always 1 (not affected by health)
        
        Hit chance is determined by unit's hit_chance attribute.
        Damage has Gaussian variance based on damage_std.
        
        Args:
            target: Another Unit instance
        
        Returns:
            Dictionary with attack info:
            - 'uses_projectile': bool - whether this is a ranged attack
            - 'base_damage': int - base damage value (for projectile calculation)
            - 'damage': int - actual damage dealt (for melee, with variance)
            - 'projectile_speed': float - speed of projectile (if ranged)
            - 'sprite_name': str - projectile sprite name (if ranged)
            - 'projectile_count': int - number of projectiles (health-adjusted for ranged)
            - 'hit_chance': float - probability of hitting (0.0 to 1.0)
            - 'damage_std': float - standard deviation for damage variance
        """
        self.is_attacking = True
        self.set_attack_animation()
        
        # Determine base damage:
        # - Ranged attacks: Full attack power (bow/projectile does the work)
        # - Melee attacks: Health-adjusted power (wounded units strike weaker)
        is_ranged = self.projectile_speed > 0
        base_damage = self.attack_power if is_ranged else self.get_effective_attack_power()
        
        # Determine projectile count:
        # - Ranged attacks: Health-adjusted (wounded archers fire fewer arrows)
        # - Melee attacks: Always 1
        effective_projectile_count = self.get_effective_projectile_count()
        
        attack_info = {
            'uses_projectile': is_ranged,
            'base_damage': base_damage,  # Base damage for projectiles to use
            'damage': 0,  # Will be set for melee attacks
            'projectile_speed': self.projectile_speed,
            'sprite_name': self.get_projectile_sprite(),
            'projectile_count': effective_projectile_count,  # Health-adjusted for ranged
            'hit_chance': self.hit_chance,  # Probability of hitting
            'damage_std': self.damage_std  # Standard deviation for damage variance
        }
        
        # For melee attacks, check hit/miss and apply damage immediately with variance
        if not attack_info['uses_projectile']:
            hit = random.random() < self.hit_chance
            attack_info['hit'] = hit
            if hit:
                # Calculate variable damage using Gaussian distribution
                actual_damage = self.calculate_variable_damage(base_damage)
                attack_info['damage'] = actual_damage
                target.take_damage(actual_damage)
        
        return attack_info
    
    def get_projectile_sprite(self):
        """
        Get the projectile sprite name for this unit
        
        Returns:
            String sprite name or None
        """
        if self.projectile_speed <= 0:
            return None
        
        # Map unit types to projectile sprites
        projectile_map = {
            'archer': 'arrow',
            'spearman': 'spear',
            'mage': 'magic_bolt',
            'catapult': 'boulder',
        }
        
        return projectile_map.get(self.unit_type, 'arrow')  # Default to arrow
    
    def reset_turn(self):
        """Reset unit for a new turn with health-based mobility"""
        self.mobility = self.get_effective_mobility()  # Reduced mobility when damaged
        self.is_active = True
        self.is_attacking = False
        self.is_hurt = False
        self.set_idle_animation()
    
    def is_player_unit(self):
        """Check if this is a player-controlled unit (team 0)"""
        return self.team == 0
    
    def is_enemy_unit(self):
        """Check if this is an enemy unit (team 1)"""
        return self.team == 1
    
    def is_ally_of(self, other_unit):
        """Check if this unit is allied with another unit"""
        return self.team == other_unit.team
    
    def __repr__(self):
        team_name = "Player" if self.is_player_unit() else ("Enemy" if self.is_enemy_unit() else f"Team {self.team}")
        return f"Unit({self.unit_type}, {team_name}, HP: {self.health}/{self.max_health}, Pos: {self.position})"
