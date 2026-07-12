"""
Scenario management - combines maps, units, and game logic

This module orchestrates the game scenario by:
- Loading and managing the map (terrain)
- Loading and managing units (player and enemy)
- Handling player interaction (selection, movement, attacks)
- Tracking game state (turn, selected unit, valid actions)
- Managing projectiles and combat
- Rendering units, projectiles, and UI overlays

Key responsibilities:
- Scenario initialization from files
- Unit movement validation and execution
- Attack validation and execution
- Turn management (player and enemy)
- Coordinate conversions (screen to grid)
- Hover detection and tooltips
"""
import os
import json
import pygame
from config import game_config
from grid import Grid, PASSABLE_EASY, PASSABLE_SLOW, PASSABLE_BLOCKED
from unit import Unit
from projectile import Projectile
from structure import Structure


class Scenario:
    """
    Game scenario manager
    
    Combines map terrain with unit placement to create a complete game scenario.
    Handles all game logic including movement, combat, turn management, and rendering.
    
    A scenario consists of:
    - Map terrain data (loaded from resources/maps/map_n.txt)
    - Unit placement data (loaded from resources/maps/units_n.txt)
    - Game state (current turn, selected unit, valid actions)
    - Active projectiles in flight
    """
    
    def __init__(self, scenario_number=1, cell_size=64, units_file=None):
        """
        Initialize and load a complete game scenario
        
        Loads map terrain and unit placement from files, initializes game state.
        Scenario files are expected in resources/maps/ directory.
        
        Args:
            scenario_number (int): Scenario ID to load (1, 2, 3, etc.)
            cell_size (int): Base size of grid cells in pixels (default 64)
            units_file (str, optional): Custom units file name (e.g., "units_1_tutorial.json")
                                      If None, uses "units_{scenario_number}.json"
        """
        self.scenario_number = scenario_number
        self.cell_size = cell_size
        
        # ========================================
        # LOAD MAP
        # ========================================
        
        # Load map terrain from file
        map_file = f"map_{scenario_number}.txt"
        self.grid = Grid(cell_size=cell_size, map_file=map_file)
        
        # ========================================
        # LOAD UNITS
        # ========================================
        
        # Load unit placement from file
        if units_file is None:
            units_file = f"units_{scenario_number}.json"
        self.units = self.load_units(units_file)
        
        # ========================================
        # LOAD STRUCTURES
        # ========================================
        
        # Load structure placement from file (if exists)
        self.structures = self.load_structures(units_file)
        
        # ========================================
        # PLAYER INTERACTION STATE
        # ========================================
        
        # Currently selected player unit (for movement and attacks)
        self.selected_unit = None
        
        # Valid move destinations for selected unit (list of (row, col) tuples)
        self.valid_moves = []
        
        # Valid attack targets for selected unit (list of enemy Unit objects)
        self.valid_attacks = []
        
        # Movement paths (maps destination -> list of waypoints for pathfinding)
        self.movement_paths = {}
        
        # Unit currently under mouse cursor (for tooltip display)
        self.hovered_unit = None
        
        # Hovered move destination (for move preview tooltip)
        self.hovered_move = None
        
        # Attack range visualization
        self.attack_range_cells = []  # Cells attackable from current position
        self.move_attack_range_cells = []  # Cells attackable after moving
        
        # ========================================
        # COMBAT STATE
        # ========================================
        
        # Projectiles currently in flight (list of Projectile objects)
        self.projectiles = []
        
        # Hit/miss feedback system
        self.combat_messages = []  # List of (message, position, timestamp, color) tuples
        self.show_combat_messages = False  # Toggle for showing hit/miss text (press H to enable)
        
        # ========================================
        # FOG OF WAR SYSTEM
        # ========================================
        
        # Fog of war toggle (P key to toggle)
        self.show_all_map = False  # By default, hide unseen areas completely (True = show with 75% fog)
        self.visible_cells = set()  # Set of (row, col) tuples currently visible to player
        self.explored_cells = set()  # Set of (row, col) tuples that have been seen (permanent)
        
        # ========================================
        # TURN MANAGEMENT
        # ========================================
        
        # Current turn (team ID from config)
        self.current_turn = game_config.get_starting_team()
        
        # Calculate initial visible cells for player-controlled teams
        self.calculate_visible_cells()
        
        print(f"Scenario {scenario_number} loaded: {len(self.units)} units on {self.grid.grid_height}x{self.grid.grid_width} map")
    
    def load_units(self, units_file):
        """
        Load unit positions and types from JSON file
        
        Units file format (JSON):
        {
            "scenario": 1,
            "description": "Standard battle",
            "teams": [
                {
                    "id": 0,
                    "name": "Blue",
                    "units": [
                        {"type": "soldier", "row": 7, "col": 3},
                        ...
                    ]
                },
                ...
            ]
        }
        
        Args:
            units_file (str): Filename (will look in resources/maps/)
        
        Returns:
            list: List of Unit objects
        """
        units = []
        
        # If units_file is just a filename, prepend resources/maps/
        if not os.path.dirname(units_file):
            units_file = f"resources/maps/{units_file}"
        
        if not os.path.exists(units_file):
            print(f"Warning: Units file {units_file} not found. No units loaded.")
            return units
        
        try:
            with open(units_file, 'r') as f:
                data = json.load(f)
            
            # Parse teams and units
            teams = data.get('teams', [])
            for team_data in teams:
                team_id = team_data.get('id', 0)
                team_units = team_data.get('units', [])
                
                for unit_data in team_units:
                    unit_type = unit_data.get('type')
                    row = unit_data.get('row')
                    col = unit_data.get('col')
                    
                    # Validate required fields
                    if unit_type is None or row is None or col is None:
                        print(f"Warning: Invalid unit data: {unit_data}")
                        continue
                    
                    # Validate position is within map bounds
                    if row < 0 or row >= self.grid.grid_height or col < 0 or col >= self.grid.grid_width:
                        print(f"Warning: Unit position ({row},{col}) out of bounds")
                        continue
                    
                    # Create unit
                    unit = Unit(unit_type=unit_type, team=team_id, position=(row, col))
                    units.append(unit)
            
            print(f"Loaded {len(units)} units from {units_file}")
        
        except Exception as e:
            print(f"Error loading units file {units_file}: {e}")
        
        return units
    
    def load_structures(self, units_file):
        """
        Load structure positions and types from JSON file
        
        Structures are defined in the same file as units, under a "structures" key.
        File format (JSON):
        {
            "scenario": 1,
            "structures": [
                {"type": "headquarters", "row": 2, "col": 5, "team": 0},
                {"type": "sandbag", "row": 4, "col": 8, "team": null},
                ...
            ]
        }
        
        Args:
            units_file (str): Filename (will look in resources/maps/)
        
        Returns:
            list: List of Structure objects
        """
        structures = []
        
        # If units_file is just a filename, prepend resources/maps/
        if not os.path.dirname(units_file):
            units_file = f"resources/maps/{units_file}"
        
        if not os.path.exists(units_file):
            return structures
        
        try:
            with open(units_file, 'r') as f:
                data = json.load(f)
            
            # Parse structures (optional field)
            structure_data = data.get('structures', [])
            
            for struct in structure_data:
                structure_type = struct.get('type')
                row = struct.get('row')
                col = struct.get('col')
                team = struct.get('team')  # Can be None for neutral
                
                # Validate required fields
                if structure_type is None or row is None or col is None:
                    print(f"Warning: Invalid structure data: {struct}")
                    continue
                
                # Validate position is within map bounds
                if row < 0 or row >= self.grid.grid_height or col < 0 or col >= self.grid.grid_width:
                    print(f"Warning: Structure position ({row},{col}) out of bounds")
                    continue
                
                # Create structure
                structure = Structure(structure_type=structure_type, row=row, col=col, 
                                    team=team, cell_size=self.cell_size)
                structures.append(structure)
            
            if structures:
                print(f"Loaded {len(structures)} structures from {units_file}")
        
        except Exception as e:
            print(f"Error loading structures from {units_file}: {e}")
        
        return structures
    
    def get_unit_at(self, row, col):
        """
        Get unit at a specific grid position
        
        Only returns alive units that are not in the dying animation state.
        This prevents selecting or targeting units that are already defeated.
        
        Args:
            row (int): Grid row coordinate
            col (int): Grid column coordinate
        
        Returns:
            Unit: Unit object at this position, or None if empty/dying unit
        """
        for unit in self.units:
            if unit.position == (row, col) and unit.is_alive and not unit.is_dying:
                return unit
        return None
    
    def get_units_by_team(self, team):
        """
        Get all alive units belonging to a specific team
        
        Useful for checking victory conditions or executing team-wide actions.
        Only includes units with is_alive=True.
        
        Args:
            team (int): Team number (0 = player, 1 = enemy, 2+ = other factions)
        
        Returns:
            list: List of Unit objects belonging to this team
        """
        return [unit for unit in self.units if unit.team == team and unit.is_alive]
    
    def get_structure_at(self, row, col):
        """
        Get structure at a specific grid position
        
        Only returns alive structures.
        
        Args:
            row (int): Grid row coordinate
            col (int): Grid column coordinate
        
        Returns:
            Structure: Structure object at this position, or None if empty/destroyed
        """
        for structure in self.structures:
            if structure.row == row and structure.col == col and structure.is_alive:
                return structure
        return None
    
    def get_structures_by_team(self, team):
        """
        Get all alive structures belonging to a specific team
        
        Args:
            team (int): Team number (None = neutral)
        
        Returns:
            list: List of Structure objects belonging to this team
        """
        return [s for s in self.structures if s.team == team and s.is_alive]
    
    def calculate_visible_cells(self):
        """
        Calculate which cells are visible to player-controlled teams
        
        Each player-controlled unit can see cells within their vision_range.
        Uses Euclidean distance for circular vision range.
        Updates self.visible_cells set with (row, col) tuples.
        Also adds newly visible cells to explored_cells (permanent).
        """
        self.visible_cells = set()
        
        # Get all player-controlled team IDs from config
        player_team_ids = [t['id'] for t in game_config.get_teams() if t.get('player_controlled', False)]
        
        # Get all units from player-controlled teams
        player_units = [u for u in self.units if u.team in player_team_ids and u.is_alive]
        
        # For each player unit, add all cells within vision range
        for unit in player_units:
            row, col = unit.position
            vision = unit.vision_range
            
            # Check all cells within vision range using Euclidean distance (circular)
            for r in range(max(0, row - vision), min(self.grid.grid_height, row + vision + 1)):
                for c in range(max(0, col - vision), min(self.grid.grid_width, col + vision + 1)):
                    # Calculate Euclidean distance
                    distance = ((r - row) ** 2 + (c - col) ** 2) ** 0.5
                    
                    # Only add if within circular range
                    if distance <= vision:
                        # Add cell to visible set
                        self.visible_cells.add((r, c))
                        # Also add to explored cells (permanent)
                        self.explored_cells.add((r, c))
    
    def remove_dead_units(self):
        """
        Remove dead units from the active units list
        
        Called after death animations complete to clean up defeated units.
        Units with is_alive=False are removed from the units list.
        """
        self.units = [unit for unit in self.units if unit.is_alive]
    
    def update(self, dt):
        """
        Update all game logic for one frame
        
        Updates:
        - All unit animations and movement interpolation
        - All projectile positions and collision detection
        - Removes completed projectiles
        - Removes units that finished death animation
        
        Args:
            dt (float): Delta time in seconds since last frame
        """
        # Track which player units are moving before update
        player_units_moving = set()
        for unit in self.units:
            if unit.team == 0 and unit.is_moving:
                player_units_moving.add(unit)
        
        # Update all units
        for unit in self.units:
            unit.update(dt)
        
        # Check if any player units finished moving
        player_finished_moving = False
        unit_finished_moving = None
        for unit in player_units_moving:
            if not unit.is_moving:
                player_finished_moving = True
                unit_finished_moving = unit
                break
        
        if player_finished_moving:
            # Recalculate fog of war
            self.calculate_visible_cells()
            
            # Handle mobility deduction for the unit that finished moving
            if unit_finished_moving and hasattr(unit_finished_moving, 'pending_mobility_cost'):
                mobility_cost = unit_finished_moving.pending_mobility_cost
                unit_finished_moving.mobility -= mobility_cost
                unit_finished_moving.pending_mobility_cost = 0
                
                # Check if unit still has mobility remaining
                if unit_finished_moving.mobility <= 0:
                    unit_finished_moving.is_active = False
                    print(f"{unit_finished_moving.unit_type} has no mobility remaining")
                else:
                    # Unit still has mobility - keep it selected and recalculate moves
                    print(f"{unit_finished_moving.unit_type} has {unit_finished_moving.mobility} mobility remaining")
                    self.selected_unit = unit_finished_moving
                    self.valid_moves = self.calculate_valid_moves(unit_finished_moving)
                    self.valid_attacks = self.calculate_valid_attacks(unit_finished_moving)
                    
                    # Recalculate attack range visualization
                    self.attack_range_cells = self.calculate_attack_range_cells(unit_finished_moving)
                    self.move_attack_range_cells = self.calculate_move_attack_range_cells(unit_finished_moving)
        
        # Update projectiles
        for projectile in self.projectiles[:]:  # Copy list to avoid modification during iteration
            if projectile.update(dt):
                # Projectile reached target
                if projectile.target:
                    # Add hit/miss message with damage
                    if self.show_combat_messages:
                        if projectile.is_hit:
                            # Show actual damage dealt
                            actual_dmg = getattr(projectile, 'actual_damage', projectile.base_damage)
                            message = f"-{actual_dmg}"
                            color = (0, 255, 0)  # Green for damage
                        else:
                            # Show 0 for miss
                            message = "0"
                            color = (255, 0, 0)  # Red for miss
                        
                        # Calculate horizontal offset based on existing messages at this position
                        existing_at_pos = sum(1 for msg in self.combat_messages if msg[1] == projectile.target.position)
                        x_offset = (existing_at_pos - 1) * 0.5  # Spread by 0.5 cells horizontally
                        
                        # Handle both Unit and Structure targets
                        from structure import Structure
                        target_pos = (projectile.target.row, projectile.target.col) if isinstance(projectile.target, Structure) else projectile.target.position
                        self.add_combat_message(message, target_pos, color, x_offset)
                    
                    if projectile.is_hit:
                        # Get actual damage dealt (with variance)
                        actual_dmg = getattr(projectile, 'actual_damage', projectile.base_damage)
                        
                        # Handle both Unit and Structure targets
                        from structure import Structure
                        target_name = projectile.target.type if isinstance(projectile.target, Structure) else projectile.target.unit_type
                        is_structure = isinstance(projectile.target, Structure)
                        
                        print(f"{projectile.attacker.unit_type}'s projectile hit {target_name} for {actual_dmg} damage (HP: {projectile.target.health}/{projectile.target.max_health})")
                        
                        # Check if target is defeated/destroyed
                        if is_structure:
                            if not projectile.target.is_alive:
                                print(f"{target_name} destroyed!")
                        else:
                            if projectile.target.is_dying:
                                print(f"{target_name} is defeated!")
                    else:
                        # Handle both Unit and Structure targets for miss messages
                        from structure import Structure
                        target_name = projectile.target.type if isinstance(projectile.target, Structure) else projectile.target.unit_type
                        print(f"{projectile.attacker.unit_type}'s projectile missed {target_name}!")
                # Remove completed projectiles
                self.projectiles.remove(projectile)
        
        # Update combat messages (fade out old ones)
        import pygame
        current_time = pygame.time.get_ticks() / 1000.0
        self.combat_messages = [msg for msg in self.combat_messages 
                               if current_time - msg[2] < 1.5]  # Keep messages for 1.5 seconds
        
        # Remove units that have finished their death animation
        self.remove_dead_units()
    
    def draw_map(self, screen):
        """
        Draw the map terrain
        
        Delegates to Grid.draw() which handles terrain tiles and grid lines.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        self.grid.draw(screen)
    
    def draw_fog_of_war(self, screen):
        """
        Draw fog of war overlay on unexplored cells
        
        Explored cells (in explored_cells) remain visible even if not currently in view.
        Enemy units are only shown if currently visible (in visible_cells).
        
        If show_all_map is False (default), draws 100% opacity black overlay on unexplored cells
        If show_all_map is True, draws 75% opacity black overlay on unexplored cells
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        # Get screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculate grid dimensions (same logic as draw_units)
        grid_world_width, grid_world_height = self.grid.get_grid_world_size()
        scaled_cell_size = self.grid.cell_size * self.grid.zoom
        scaled_grid_width = grid_world_width * self.grid.zoom
        scaled_grid_height = grid_world_height * self.grid.zoom
        
        # Calculate centered position
        center_x = (screen_width - scaled_grid_width) / 2 + self.grid.offset_x
        center_y = (screen_height - scaled_grid_height) / 2 + self.grid.offset_y
        
        # Determine fog opacity based on show_all_map setting
        if self.show_all_map:
            fog_color = (192, 192, 192, int(255 * 0.75))  # Light gray with 75% opacity
        else:
            fog_color = (192, 192, 192, 255)  # Light gray with 100% opacity
        
        # Iterate through all grid cells
        for row in range(self.grid.grid_height):
            for col in range(self.grid.grid_width):
                # Skip explored cells (cells that have been seen remain visible)
                if (row, col) in self.explored_cells:
                    continue
                
                # Calculate screen position for this cell (same as draw_units)
                x = center_x + col * scaled_cell_size
                y = center_y + row * scaled_cell_size
                
                # Create fog surface for this cell
                fog_surface = pygame.Surface((scaled_cell_size, scaled_cell_size), pygame.SRCALPHA)
                fog_surface.fill(fog_color)
                
                # Draw fog overlay
                screen.blit(fog_surface, (x, y))
    
    def draw_units(self, screen):
        """
        Draw all alive units with their animations and health bars
        
        Units are drawn at their interpolated positions for smooth movement animation.
        Converts grid coordinates to screen coordinates accounting for camera offset and zoom.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculate grid dimensions (same logic as grid.draw)
        grid_world_width, grid_world_height = self.grid.get_grid_world_size()
        scaled_cell_size = self.grid.cell_size * self.grid.zoom
        scaled_grid_width = grid_world_width * self.grid.zoom
        scaled_grid_height = grid_world_height * self.grid.zoom
        
        # Calculate centered position
        center_x = (screen_width - scaled_grid_width) / 2 + self.grid.offset_x
        center_y = (screen_height - scaled_grid_height) / 2 + self.grid.offset_y
        
        # Draw each unit
        for unit in self.units:
            if unit.is_alive:
                # Use interpolated position for smooth animation
                row, col = unit.get_current_position()
                
                # Only draw enemy units if they are visible or show_all_map is enabled
                if unit.team != 0:  # Enemy unit
                    if not self.show_all_map and (row, col) not in self.visible_cells:
                        continue  # Skip drawing this enemy unit
                
                # Calculate screen position
                x = center_x + col * scaled_cell_size
                y = center_y + row * scaled_cell_size
                
                # Draw unit
                unit.draw(screen, x, y, scaled_cell_size)
    
    def draw_structures(self, screen):
        """
        Draw all alive structures with their health bars
        
        Structures are static and drawn at their grid positions.
        Converts grid coordinates to screen coordinates accounting for camera offset and zoom.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculate grid dimensions (same logic as grid.draw)
        grid_world_width, grid_world_height = self.grid.get_grid_world_size()
        scaled_cell_size = self.grid.cell_size * self.grid.zoom
        scaled_grid_width = grid_world_width * self.grid.zoom
        scaled_grid_height = grid_world_height * self.grid.zoom
        
        # Calculate centered position
        center_x = (screen_width - scaled_grid_width) / 2 + self.grid.offset_x
        center_y = (screen_height - scaled_grid_height) / 2 + self.grid.offset_y
        
        # Draw each structure
        for structure in self.structures:
            if structure.is_alive:
                row, col = structure.row, structure.col
                
                # Only draw enemy structures if visible or show_all_map enabled
                if structure.team not in [None, 0]:  # Enemy or neutral structure
                    if not self.show_all_map and (row, col) not in self.visible_cells:
                        continue  # Skip drawing
                
                # Calculate screen position
                x = center_x + col * scaled_cell_size
                y = center_y + row * scaled_cell_size
                
                # Draw structure using its draw method
                # (structures have their own draw method that handles sprite and health bar)
                # We need to convert to cell-based coordinates
                camera_x = -center_x
                camera_y = -center_y
                structure.draw(screen, camera_x, camera_y, self.grid.zoom)
    
    def draw_projectiles(self, screen):
        """
        Draw all active projectiles with rotation
        
        Projectiles are rendered scaled and rotated to face their direction of travel.
        Accounts for camera offset and zoom level.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculate grid dimensions (same logic as grid.draw)
        grid_world_width, grid_world_height = self.grid.get_grid_world_size()
        scaled_cell_size = self.grid.cell_size * self.grid.zoom
        scaled_grid_width = grid_world_width * self.grid.zoom
        scaled_grid_height = grid_world_height * self.grid.zoom
        
        # Calculate centered position
        center_x = (screen_width - scaled_grid_width) / 2 + self.grid.offset_x
        center_y = (screen_height - scaled_grid_height) / 2 + self.grid.offset_y
        
        # Draw each projectile
        for projectile in self.projectiles:
            # Get current position of projectile
            row, col = projectile.get_current_position()
            
            # Calculate screen position
            x = center_x + col * scaled_cell_size + scaled_cell_size / 2
            y = center_y + row * scaled_cell_size + scaled_cell_size / 2
            
            # Draw projectile
            if projectile.sprite:
                # Scale projectile sprite (smaller than units)
                scale_factor = self.grid.zoom * 0.8
                sprite_size = max(8, int(16 * scale_factor))
                scaled_sprite = pygame.transform.scale(projectile.sprite, (sprite_size, sprite_size))
                
                # Rotate sprite to face direction of travel
                rotated_sprite = pygame.transform.rotate(scaled_sprite, -projectile.angle)
                
                # Center the rotated sprite
                sprite_rect = rotated_sprite.get_rect(center=(x, y))
                
                screen.blit(rotated_sprite, sprite_rect)
    
    def draw_unit_status_indicators(self, screen):
        """
        Draw status indicators (glows) for all player units
        
        Shows unit status at a glance:
        - Green glow: Full mobility (hasn't moved)
        - Yellow glow: Partial mobility (moved but can move again)
        - Gray glow: No mobility (inactive)
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculate grid dimensions
        grid_world_width, grid_world_height = self.grid.get_grid_world_size()
        scaled_cell_size = self.grid.cell_size * self.grid.zoom
        scaled_grid_width = grid_world_width * self.grid.zoom
        scaled_grid_height = grid_world_height * self.grid.zoom
        
        # Calculate centered position
        center_x = (screen_width - scaled_grid_width) / 2 + self.grid.offset_x
        center_y = (screen_height - scaled_grid_height) / 2 + self.grid.offset_y
        
        # Get player-controlled team IDs
        player_team_ids = [t['id'] for t in game_config.get_teams() if t.get('player_controlled', False)]
        
        # Draw status glow for each player unit
        for unit in self.units:
            if unit.team in player_team_ids and unit.is_alive and not unit.is_dying:
                row, col = unit.position
                x = center_x + col * scaled_cell_size
                y = center_y + row * scaled_cell_size
                
                # Determine glow color based on unit status (use config colors)
                if unit.mobility == unit.max_mobility:
                    # Full mobility - green glow
                    glow_color = game_config.get_ui_color('unit_status_full', (0, 255, 0)) + (60,)
                elif unit.mobility > 0 and unit.is_active:
                    # Partial mobility - yellow glow
                    glow_color = game_config.get_ui_color('unit_status_partial', (255, 255, 0)) + (60,)
                else:
                    # No mobility - gray glow
                    glow_color = game_config.get_ui_color('unit_status_inactive', (128, 128, 128)) + (60,)
                
                # Draw glow overlay
                glow_surface = pygame.Surface((int(scaled_cell_size), int(scaled_cell_size)), pygame.SRCALPHA)
                glow_surface.fill(glow_color)
                screen.blit(glow_surface, (x, y))
    
    def draw_selection_highlights(self, screen):
        """
        Draw UI overlays for valid moves and attacks
        
        Renders:
        - Green highlighted cells for valid move destinations
        - Red highlighted cells for attack range from current position
        - Orange highlighted cells for move+attack range
        - Yellow border around selected unit
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculate grid dimensions
        grid_world_width, grid_world_height = self.grid.get_grid_world_size()
        scaled_cell_size = self.grid.cell_size * self.grid.zoom
        scaled_grid_width = grid_world_width * self.grid.zoom
        scaled_grid_height = grid_world_height * self.grid.zoom
        
        # Calculate centered position
        center_x = (screen_width - scaled_grid_width) / 2 + self.grid.offset_x
        center_y = (screen_height - scaled_grid_height) / 2 + self.grid.offset_y
        
        # Draw move+attack range (orange) - draw first so it appears behind other overlays
        for row, col in self.move_attack_range_cells:
            x = center_x + col * scaled_cell_size
            y = center_y + row * scaled_cell_size
            
            # Draw semi-transparent orange overlay
            overlay = pygame.Surface((int(scaled_cell_size), int(scaled_cell_size)), pygame.SRCALPHA)
            overlay.fill((255, 165, 0, 50))  # Orange with low alpha
            screen.blit(overlay, (x, y))
        
        # Draw attack range from current position (red) - darker than move+attack
        for row, col in self.attack_range_cells:
            x = center_x + col * scaled_cell_size
            y = center_y + row * scaled_cell_size
            
            # Draw semi-transparent red overlay
            overlay = pygame.Surface((int(scaled_cell_size), int(scaled_cell_size)), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 70))  # Red with alpha
            screen.blit(overlay, (x, y))
        
        # Draw valid move positions (green)
        for row, col in self.valid_moves:
            x = center_x + col * scaled_cell_size
            y = center_y + row * scaled_cell_size
            
            # Draw semi-transparent green overlay
            overlay = pygame.Surface((int(scaled_cell_size), int(scaled_cell_size)), pygame.SRCALPHA)
            overlay.fill((0, 255, 0, 80))  # Green with alpha
            screen.blit(overlay, (x, y))
            
            # Draw border
            pygame.draw.rect(screen, (0, 255, 0), 
                           (x, y, scaled_cell_size, scaled_cell_size), 2)
        
        # Draw attackable enemies (red border)
        for enemy in self.valid_attacks:
            # Handle both Unit objects (with .position) and Structure objects (with .row, .col)
            from structure import Structure
            if isinstance(enemy, Structure):
                row, col = enemy.row, enemy.col
            else:
                row, col = enemy.position
            
            x = center_x + col * scaled_cell_size
            y = center_y + row * scaled_cell_size
            
            # Draw semi-transparent red overlay
            overlay = pygame.Surface((int(scaled_cell_size), int(scaled_cell_size)), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 100))  # Red with alpha
            screen.blit(overlay, (x, y))
            
            # Draw red border
            pygame.draw.rect(screen, (255, 0, 0), 
                           (x, y, scaled_cell_size, scaled_cell_size), 3)
        
        # Draw selected unit highlight
        if self.selected_unit:
            row, col = self.selected_unit.position
            x = center_x + col * scaled_cell_size
            y = center_y + row * scaled_cell_size
            
            # Draw yellow border for selected unit
            pygame.draw.rect(screen, (255, 255, 0), 
                           (x, y, scaled_cell_size, scaled_cell_size), 3)
            
            # Draw vision range visualization (light blue overlay)
            vision = self.selected_unit.vision_range
            unit_row, unit_col = self.selected_unit.position
            
            for r in range(max(0, unit_row - vision), min(self.grid.grid_height, unit_row + vision + 1)):
                for c in range(max(0, unit_col - vision), min(self.grid.grid_width, unit_col + vision + 1)):
                    # Calculate Euclidean distance for circular vision
                    distance = ((r - unit_row) ** 2 + (c - unit_col) ** 2) ** 0.5
                    
                    # Only draw if within circular range
                    if distance <= vision:
                        vx = center_x + c * scaled_cell_size
                        vy = center_y + r * scaled_cell_size
                        
                        # Draw semi-transparent light blue overlay for vision range
                        vision_overlay = pygame.Surface((int(scaled_cell_size), int(scaled_cell_size)), pygame.SRCALPHA)
                        vision_overlay.fill((135, 206, 250, 40))  # Sky blue with low alpha
                        screen.blit(vision_overlay, (vx, vy))
    
    def update_hover(self, mouse_x, mouse_y, screen_width, screen_height):
        """
        Update which unit (if any) is under the mouse cursor
        
        Converts mouse screen coordinates to grid coordinates and checks for units.
        Sets self.hovered_unit for tooltip display. Works for both player and enemy units.
        Also tracks hovered move destinations for move preview tooltips.
        
        Args:
            mouse_x (int): Mouse X coordinate in screen pixels
            mouse_y (int): Mouse Y coordinate in screen pixels
            screen_width (int): Width of screen in pixels
            screen_height (int): Height of screen in pixels
        """
        grid_pos = self.screen_to_grid(mouse_x, mouse_y, screen_width, screen_height)
        
        if grid_pos:
            row, col = grid_pos
            unit = self.get_unit_at(row, col)
            
            # Show hover for any unit
            self.hovered_unit = unit
            
            # Check if hovering over a valid move destination
            if (row, col) in self.valid_moves:
                self.hovered_move = (row, col)
            else:
                self.hovered_move = None
        else:
            self.hovered_unit = None
            self.hovered_move = None
    
    def draw_hover_info(self, screen, font):
        """
        Draw information tooltip for hovered unit
        
        Displays unit stats in a semi-transparent box near the mouse cursor.
        Border color indicates team (blue=player, red=enemy, white=other).
        Tooltip automatically stays on screen by adjusting position if needed.
        
        Args:
            screen (pygame.Surface): Surface to draw on
            font (pygame.Font): Font to use for text rendering
        """
        if not self.hovered_unit:
            return
        
        unit = self.hovered_unit
        
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Determine border color based on team
        if unit.is_player_unit():
            border_color = (100, 150, 255)  # Blue for player
        elif unit.is_enemy_unit():
            border_color = (255, 100, 100)  # Red for enemy
        else:
            border_color = (255, 255, 255)  # White for other teams
        
        # Create info text
        effective_attack = unit.get_effective_attack_power()
        effective_mobility = unit.get_effective_mobility()
        effective_projectiles = unit.get_effective_projectile_count()
        
        info_lines = [
            f"{unit.unit_type.capitalize()}",
            f"HP: {unit.health}/{unit.max_health}",
            f"Attack: {effective_attack}",
            f"Defense: {unit.defense}",
            f"Mobility: {unit.mobility}/{effective_mobility}",
            f"Range: {unit.attack_range}"
        ]
        
        # Add projectile info for ranged units
        if effective_projectiles > 1:
            total_damage = effective_attack * effective_projectiles
            info_lines.insert(3, f"Total DMG: {total_damage} ({effective_projectiles}x)")
        
        # Calculate tooltip size
        line_height = 22
        padding = 10
        max_width = max([font.size(line)[0] for line in info_lines])
        tooltip_width = max_width + padding * 2
        tooltip_height = len(info_lines) * line_height + padding * 2
        
        # Position tooltip (offset from mouse, keep on screen)
        tooltip_x = mouse_x + 15
        tooltip_y = mouse_y + 15
        
        # Keep tooltip on screen
        if tooltip_x + tooltip_width > screen.get_width():
            tooltip_x = mouse_x - tooltip_width - 15
        if tooltip_y + tooltip_height > screen.get_height():
            tooltip_y = mouse_y - tooltip_height - 15
        
        # Draw background
        background = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
        background.fill((0, 0, 0, 220))  # Semi-transparent black
        screen.blit(background, (tooltip_x, tooltip_y))
        
        # Draw colored border (blue for player, red for enemy)
        pygame.draw.rect(screen, border_color, 
                        (tooltip_x, tooltip_y, tooltip_width, tooltip_height), 2)
        
        # Draw text
        for i, line in enumerate(info_lines):
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (tooltip_x + padding, tooltip_y + padding + i * line_height))
    
    def calculate_attack_range_cells(self, unit, from_position=None):
        """
        Calculate all cells within attack range from a given position
        
        Args:
            unit (Unit): Unit to calculate attack range for
            from_position (tuple, optional): Position to calculate from (row, col).
                                            If None, uses unit's current position.
        
        Returns:
            list: List of (row, col) tuples within attack range
        """
        if from_position is None:
            from_position = unit.position
        
        start_row, start_col = from_position
        range_cells = []
        
        # Check all cells within Manhattan distance of attack_range
        for row in range(max(0, start_row - unit.attack_range), 
                        min(self.grid.grid_height, start_row + unit.attack_range + 1)):
            for col in range(max(0, start_col - unit.attack_range), 
                            min(self.grid.grid_width, start_col + unit.attack_range + 1)):
                # Calculate Manhattan distance
                distance = abs(row - start_row) + abs(col - start_col)
                
                if distance > 0 and distance <= unit.attack_range:
                    # For direct fire, check line of sight
                    if unit.fire_type == 'direct':
                        if self.has_line_of_sight(from_position, (row, col)):
                            range_cells.append((row, col))
                    else:
                        # Indirect fire can shoot over obstacles
                        range_cells.append((row, col))
        
        return range_cells
    
    def calculate_move_attack_range_cells(self, unit):
        """
        Calculate all cells attackable after moving (move+attack range)
        
        Finds union of attack ranges from all valid move destinations.
        
        Args:
            unit (Unit): Unit to calculate move+attack range for
        
        Returns:
            list: List of (row, col) tuples attackable after moving
        """
        move_attack_cells = set()
        
        # Add attack range from current position
        for cell in self.attack_range_cells:
            move_attack_cells.add(cell)
        
        # Add attack range from each valid move destination
        for move_dest in self.valid_moves:
            attack_from_dest = self.calculate_attack_range_cells(unit, move_dest)
            for cell in attack_from_dest:
                move_attack_cells.add(cell)
        
        # Remove cells that are already in direct attack range (to avoid overlap)
        move_attack_only = [cell for cell in move_attack_cells if cell not in self.attack_range_cells]
        
        return move_attack_only
    
    def draw_move_preview(self, screen, font):
        """
        Draw move preview tooltip when hovering over a valid move destination
        
        Shows:
        - Move cost in mobility points
        - Remaining mobility after move
        - Enemies in attack range from that position
        
        Args:
            screen (pygame.Surface): Surface to draw on
            font (pygame.Font): Font to use for text rendering
        """
        if not self.hovered_move or not self.selected_unit:
            return
        
        row, col = self.hovered_move
        
        # Calculate move cost
        if self.hovered_move in self.movement_paths:
            path = self.movement_paths[self.hovered_move]
            move_cost = len(path) - 1
        else:
            return
        
        remaining_mobility = self.selected_unit.mobility - move_cost
        
        # Count enemies in attack range from this position
        attackable_from_here = self.calculate_attack_range_cells(self.selected_unit, self.hovered_move)
        enemy_count = sum(1 for enemy in self.units 
                         if enemy.team != self.selected_unit.team 
                         and enemy.is_alive 
                         and not enemy.is_dying 
                         and enemy.position in attackable_from_here)
        
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Create info text
        info_lines = [
            f"Move Cost: {move_cost}",
            f"Remaining: {remaining_mobility}",
            f"Enemies in range: {enemy_count}"
        ]
        
        # Calculate tooltip size
        line_height = 20
        padding = 8
        max_width = max([font.size(line)[0] for line in info_lines])
        tooltip_width = max_width + padding * 2
        tooltip_height = len(info_lines) * line_height + padding * 2
        
        # Position tooltip (offset from mouse, keep on screen)
        tooltip_x = mouse_x + 15
        tooltip_y = mouse_y + 15
        
        # Keep tooltip on screen
        if tooltip_x + tooltip_width > screen.get_width():
            tooltip_x = mouse_x - tooltip_width - 15
        if tooltip_y + tooltip_height > screen.get_height():
            tooltip_y = mouse_y - tooltip_height - 15
        
        # Draw background
        background = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
        background.fill((40, 40, 80, 230))  # Dark blue background
        screen.blit(background, (tooltip_x, tooltip_y))
        
        # Draw border
        pygame.draw.rect(screen, (100, 200, 255), 
                        (tooltip_x, tooltip_y, tooltip_width, tooltip_height), 2)
        
        # Draw text
        for i, line in enumerate(info_lines):
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (tooltip_x + padding, tooltip_y + padding + i * line_height))
    
    def cycle_to_next_active_unit(self):
        """
        Cycle to the next active player unit
        
        Selects the next unit in sequence that can still act this turn.
        Wraps around to the first unit if at the end of the list.
        Updates selection, valid moves, and attack ranges.
        Works for any player-controlled team.
        """
        # Get player-controlled team IDs
        player_team_ids = [t['id'] for t in game_config.get_teams() if t.get('player_controlled', False)]
        
        # Check if current turn is player-controlled
        if self.current_turn not in player_team_ids:
            return  # Only cycle during player-controlled turns
        
        # Get all active units for current player team
        active_units = [u for u in self.units 
                       if u.team == self.current_turn and u.is_alive and not u.is_dying and u.is_active and u.mobility > 0]
        
        if not active_units:
            return
        
        # Find current unit's index in active units list
        current_index = -1
        if self.selected_unit and self.selected_unit in active_units:
            current_index = active_units.index(self.selected_unit)
        
        # Cycle to next unit (wrap around)
        next_index = (current_index + 1) % len(active_units)
        next_unit = active_units[next_index]
        
        # Select the next unit
        self.select_unit(next_unit)
    
    def add_combat_message(self, message, position, color=(255, 255, 255), x_offset=0.0):
        """
        Add a combat message (HIT/MISS) to display at a position
        
        Args:
            message (str): Text to display (e.g., "HIT!", "MISS")
            position (tuple): Grid position (row, col) where message should appear
            color (tuple): RGB color for the message
            x_offset (float): Horizontal offset in grid cells for message separation
        """
        import pygame
        timestamp = pygame.time.get_ticks() / 1000.0
        self.combat_messages.append((message, position, timestamp, color, x_offset))
    
    def draw_combat_messages(self, screen, font, cell_size, zoom, offset_x, offset_y):
        """
        Draw hit/miss messages on screen
        
        Messages fade out over time and float upward slightly.
        
        Args:
            screen: Pygame surface to draw on
            font: Font to use for rendering
            cell_size: Base cell size
            zoom: Current zoom level
            offset_x: Camera X offset
            offset_y: Camera Y offset
        """
        if not self.show_combat_messages:
            return
        
        import pygame
        current_time = pygame.time.get_ticks() / 1000.0
        
        # Calculate grid dimensions and centered position (same as units and projectiles)
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        grid_world_width, grid_world_height = self.grid.get_grid_world_size()
        scaled_cell_size = cell_size * zoom
        scaled_grid_width = grid_world_width * zoom
        scaled_grid_height = grid_world_height * zoom
        
        # Calculate centered position
        center_x = (screen_width - scaled_grid_width) / 2 + offset_x
        center_y = (screen_height - scaled_grid_height) / 2 + offset_y
        
        for msg_data in self.combat_messages:
            message, position, timestamp, color = msg_data[:4]
            x_offset_cells = msg_data[4] if len(msg_data) > 4 else 0.0
            
            # Calculate age of message (0.0 to 1.5 seconds)
            age = current_time - timestamp
            if age > 1.5:
                continue
            
            # Fade out over time
            alpha = int(255 * (1.0 - age / 1.5))
            
            # Float upward
            float_offset = -age * 40  # Move up 40 pixels per second (faster)
            
            # Convert grid position to screen position (same as units)
            row, col = position
            x = center_x + col * scaled_cell_size + scaled_cell_size / 2 + (x_offset_cells * scaled_cell_size)
            y = center_y + row * scaled_cell_size + float_offset - 10  # Start just above unit
            
            # Render text with alpha
            text_surface = font.render(message, True, color)
            text_surface.set_alpha(alpha)
            
            # Center text
            text_rect = text_surface.get_rect(center=(int(x), int(y)))
            screen.blit(text_surface, text_rect)
    
    def reset_all_units_turn(self):
        """
        Reset all units for a new turn
        
        Calls reset_turn() on all alive units, which restores mobility and
        sets them to active state.
        """
        for unit in self.units:
            if unit.is_alive:
                unit.reset_turn()
    
    def get_passability_at(self, row, col):
        """
        Get terrain passability type at a grid position
        
        Returns the passability constant for the terrain at this position.
        Out-of-bounds positions are considered blocked.
        Also checks for structures - alive structures block movement.
        
        Args:
            row (int): Grid row coordinate
            col (int): Grid column coordinate
        
        Returns:
            int: PASSABLE_EASY (0), PASSABLE_SLOW (1), or PASSABLE_BLOCKED (2)
        """
        if row < 0 or row >= self.grid.grid_height or col < 0 or col >= self.grid.grid_width:
            return PASSABLE_BLOCKED
        
        # Check if there's an alive structure blocking this cell
        structure = self.get_structure_at(row, col)
        if structure and structure.is_alive:
            return PASSABLE_BLOCKED
        
        if 0 <= row < len(self.grid.map_data) and 0 <= col < len(self.grid.map_data[row]):
            icon_id, passability = self.grid.map_data[row][col]
            return passability
        
        return PASSABLE_BLOCKED
    
    def calculate_valid_moves(self, unit):
        """
        Calculate all valid move destinations for a unit using BFS pathfinding
        
        Uses Breadth-First Search to find all reachable cells within unit's mobility.
        Takes into account:
        - Unit's current mobility points
        - Terrain passability (blocked terrain is impassable)
        - Slow terrain (halves mobility when starting from it)
        - Other units (cannot move to occupied cells)
        - Actual paths (can't move through blocked terrain)
        
        Also stores the path to each reachable cell in self.movement_paths.
        
        Args:
            unit (Unit): Unit to calculate moves for
        
        Returns:
            list: List of (row, col) tuples representing valid destinations
        """
        if not unit or not unit.is_alive or not unit.is_active:
            return []
        
        valid_moves = []
        self.movement_paths = {}
        start_row, start_col = unit.position
        
        # Check if starting from slow passable terrain (halves mobility)
        start_passability = self.get_passability_at(start_row, start_col)
        effective_mobility = unit.mobility
        if start_passability == PASSABLE_SLOW:
            effective_mobility = unit.mobility // 2
        
        # BFS to find all reachable cells
        from collections import deque
        
        # Queue contains: (row, col, distance_traveled, path)
        queue = deque([(start_row, start_col, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col): 0}  # Maps position -> minimum distance
        
        while queue:
            current_row, current_col, distance, path = queue.popleft()
            
            # Try all 4 adjacent cells (up, down, left, right)
            neighbors = [
                (current_row - 1, current_col),  # up
                (current_row + 1, current_col),  # down
                (current_row, current_col - 1),  # left
                (current_row, current_col + 1),  # right
            ]
            
            for next_row, next_col in neighbors:
                # Check if within grid bounds
                if not (0 <= next_row < self.grid.grid_height and 
                       0 <= next_col < self.grid.grid_width):
                    continue
                
                # Check if terrain is passable (not blocked)
                passability = self.get_passability_at(next_row, next_col)
                if passability == PASSABLE_BLOCKED:
                    continue
                
                # Calculate cost to move to this cell (1 per cell)
                new_distance = distance + 1
                
                # Check if within mobility range
                if new_distance > effective_mobility:
                    continue
                
                # Check if we've already visited this cell with a shorter path
                if (next_row, next_col) in visited and visited[(next_row, next_col)] <= new_distance:
                    continue
                
                # Mark as visited
                visited[(next_row, next_col)] = new_distance
                
                # Store the path to this cell
                new_path = path + [(next_row, next_col)]
                
                # Check if destination cell is available (no unit blocking)
                if not self.get_unit_at(next_row, next_col):
                    # This is a valid destination
                    if (next_row, next_col) not in valid_moves:
                        valid_moves.append((next_row, next_col))
                        self.movement_paths[(next_row, next_col)] = new_path
                
                # Continue searching from this cell (even if occupied, to find cells beyond)
                queue.append((next_row, next_col, new_distance, new_path))
        
        return valid_moves
    
    def has_line_of_sight(self, start_pos, target_pos):
        """
        Check if there's a clear line of sight between two positions
        
        Uses Bresenham's line algorithm to check all cells between start and target.
        Line of sight is blocked by impassable terrain (mountains, water, etc.)
        
        Args:
            start_pos (tuple): Starting position (row, col)
            target_pos (tuple): Target position (row, col)
        
        Returns:
            bool: True if line of sight is clear, False if blocked
        """
        start_row, start_col = start_pos
        target_row, target_col = target_pos
        
        # Bresenham's line algorithm
        dx = abs(target_col - start_col)
        dy = abs(target_row - start_row)
        
        x = start_col
        y = start_row
        
        x_inc = 1 if target_col > start_col else -1
        y_inc = 1 if target_row > start_row else -1
        
        # Calculate error
        if dx > dy:
            error = dx / 2
            while x != target_col:
                x += x_inc
                error -= dy
                if error < 0:
                    y += y_inc
                    error += dx
                
                # Skip checking the start and target positions themselves
                if (y, x) == target_pos or (y, x) == start_pos:
                    continue
                
                # Check if this cell blocks line of sight
                if 0 <= y < self.grid.grid_height and 0 <= x < self.grid.grid_width:
                    if self.get_passability_at(y, x) == PASSABLE_BLOCKED:
                        return False
        else:
            error = dy / 2
            while y != target_row:
                y += y_inc
                error -= dx
                if error < 0:
                    x += x_inc
                    error += dy
                
                # Skip checking the start and target positions themselves
                if (y, x) == target_pos or (y, x) == start_pos:
                    continue
                
                # Check if this cell blocks line of sight
                if 0 <= y < self.grid.grid_height and 0 <= x < self.grid.grid_width:
                    if self.get_passability_at(y, x) == PASSABLE_BLOCKED:
                        return False
        
        return True
    
    def calculate_valid_attacks(self, unit):
        """
        Calculate all valid attack targets for a unit
        
        Checks all enemy units and structures, determines which are within attack range.
        For direct fire units, also checks line of sight.
        Indirect fire units can shoot over obstacles.
        
        Args:
            unit (Unit): Unit to calculate attacks for
        
        Returns:
            list: List of enemy Unit objects and Structure objects that can be attacked
        """
        if not unit or not unit.is_alive or not unit.is_active:
            return []
        
        valid_attacks = []
        start_row, start_col = unit.position
        
        # Check all enemy units
        for enemy in self.units:
            # Skip if not an enemy, dead, dying, or same team
            if enemy.team == unit.team or not enemy.is_alive or enemy.is_dying:
                continue
            
            enemy_row, enemy_col = enemy.position
            
            # Calculate Manhattan distance to enemy
            distance = abs(enemy_row - start_row) + abs(enemy_col - start_col)
            
            # Check if within attack range
            if distance <= unit.attack_range:
                # For direct fire, check line of sight
                if unit.fire_type == 'direct':
                    if self.has_line_of_sight(unit.position, enemy.position):
                        valid_attacks.append(enemy)
                    # else: blocked by terrain, can't attack
                else:
                    # Indirect fire can shoot over obstacles
                    valid_attacks.append(enemy)
        
        # Check all enemy structures (and neutral structures)
        for structure in self.structures:
            # Skip if same team or destroyed
            # Neutral structures (team=None) are attackable by all teams
            if structure.team == unit.team or not structure.is_alive:
                continue
            
            struct_row, struct_col = structure.row, structure.col
            
            # Calculate Manhattan distance to structure
            distance = abs(struct_row - start_row) + abs(struct_col - start_col)
            
            # Check if within attack range
            if distance <= unit.attack_range:
                # For direct fire, check line of sight
                if unit.fire_type == 'direct':
                    if self.has_line_of_sight(unit.position, (struct_row, struct_col)):
                        valid_attacks.append(structure)
                else:
                    # Indirect fire can shoot over obstacles
                    valid_attacks.append(structure)
        
        return valid_attacks
    
    def attempt_attack(self, row, col):
        """
        Attempt to attack an enemy unit or structure at the given position
        
        Validates that target is an enemy within range, then executes the attack.
        Creates projectile for ranged attacks, applies immediate damage for melee.
        Unit becomes inactive after attacking (can't move or attack again this turn).
        
        Args:
            row (int): Target grid row
            col (int): Target grid column
        
        Returns:
            bool: True if attack was successful, False otherwise
        """
        if not self.selected_unit:
            return False
        
        # Check if there's an enemy unit at the target position
        target = self.get_unit_at(row, col)
        
        # If no unit, check for structure
        if not target:
            target = self.get_structure_at(row, col)
        
        if target and target in self.valid_attacks:
            # Check if target is a structure
            is_structure = isinstance(target, Structure)
            
            # Perform the attack (triggers animation and gets attack info)
            # For structures, we'll modify the attack process slightly
            if is_structure:
                # Set animation manually for structures (since unit.attack() expects Unit target)
                self.selected_unit.is_attacking = True
                self.selected_unit.set_attack_animation()
                
                # Get attack parameters
                is_ranged = self.selected_unit.projectile_speed > 0
                base_damage = self.selected_unit.attack_power if is_ranged else self.selected_unit.get_effective_attack_power()
                effective_projectile_count = self.selected_unit.get_effective_projectile_count()
                
                attack_info = {
                    'uses_projectile': is_ranged,
                    'base_damage': base_damage,
                    'damage': 0,
                    'projectile_speed': self.selected_unit.projectile_speed,
                    'sprite_name': self.selected_unit.get_projectile_sprite(),
                    'projectile_count': effective_projectile_count,
                    'hit_chance': 1.0,  # Structures don't dodge - always hit
                    'damage_std': self.selected_unit.damage_std
                }
                
                # For melee attacks on structures, apply damage immediately
                if not is_ranged:
                    actual_damage = self.selected_unit.calculate_variable_damage(base_damage)
                    attack_info['damage'] = actual_damage
                    attack_info['hit'] = True
                    damage_dealt = target.take_damage(actual_damage)
                    print(f"{self.selected_unit.unit_type} attacked {target.type} for {damage_dealt} damage (HP: {target.health}/{target.max_health})")
                    
                    if not target.is_alive:
                        print(f"{target.type} destroyed!")
            else:
                # Original unit attack code
                # Perform the attack
                attack_info = self.selected_unit.attack(target)
            
            # Create projectile(s) for ranged attacks
            if attack_info['uses_projectile']:
                projectile_count = attack_info.get('projectile_count', 1)
                
                # Get target position (handle both Unit and Structure)
                target_pos = (target.row, target.col) if is_structure else target.position
                target_name = target.type if is_structure else target.unit_type
                
                # Create multiple projectiles with offset for visual variety
                for i in range(projectile_count):
                    # Calculate visual offset for spread effect
                    if projectile_count > 1:
                        # Spread projectiles perpendicular to flight direction
                        spread_factor = (i / (projectile_count - 1)) - 0.5  # -0.5 to 0.5
                        spread_factor *= 0.4  # Scale down the spread
                        
                        # Calculate perpendicular offset
                        delta_row = target_pos[0] - self.selected_unit.position[0]
                        delta_col = target_pos[1] - self.selected_unit.position[1]
                        
                        # Perpendicular is (-delta_col, delta_row) rotated 90 degrees
                        offset_row = -delta_col * spread_factor * 0.2
                        offset_col = delta_row * spread_factor * 0.2
                    else:
                        offset_row, offset_col = 0.0, 0.0
                    
                    projectile = Projectile(
                        start_pos=self.selected_unit.position,
                        target_pos=target_pos,
                        speed=attack_info['projectile_speed'],
                        sprite_name=attack_info['sprite_name'],
                        attacker=self.selected_unit,
                        target=target,
                        base_damage=attack_info['base_damage'],  # Base damage (will vary with Gaussian)
                        offset=(offset_row, offset_col),
                        hit_chance=attack_info['hit_chance']
                    )
                    
                    # Add stagger delay so projectiles launch sequentially
                    projectile.progress = -i * 0.12  # Negative progress creates a delay
                    
                    self.projectiles.append(projectile)
                
                if projectile_count > 1:
                    print(f"{self.selected_unit.unit_type} fired {projectile_count} projectiles at {target_name}")
                else:
                    print(f"{self.selected_unit.unit_type} fired projectile at {target_name}")
            else:
                # Melee attack - damage already applied with hit/miss determined
                is_hit = attack_info.get('hit', False)
                
                # Get target position and name (handle both Unit and Structure)
                target_pos = (target.row, target.col) if is_structure else target.position
                target_name = target.type if is_structure else target.unit_type
                
                # Add hit/miss message with damage
                if self.show_combat_messages:
                    if is_hit:
                        # Show actual damage dealt
                        message = f"-{attack_info['damage']}"
                        color = (0, 255, 0)  # Green for damage
                    else:
                        # Show 0 for miss
                        message = "0"
                        color = (255, 0, 0)  # Red for miss
                    self.add_combat_message(message, target_pos, color, 0.0)
                
                if is_hit:
                    print(f"{self.selected_unit.unit_type} attacked {target_name} for {attack_info['damage']} damage (HP: {target.health}/{target.max_health})")
                    
                    # Check if target is dying (units) or destroyed (structures)
                    if is_structure:
                        if not target.is_alive:
                            print(f"{target_name} destroyed!")
                    else:
                        if target.is_dying:
                            print(f"{target_name} is defeated!")
                else:
                    print(f"{self.selected_unit.unit_type} missed {target_name}!")
            
            # Mark unit as inactive after attacking
            self.selected_unit.is_active = False
            
            # Deselect after attacking
            self.deselect_unit()
            return True
        
        return False
    
    def select_unit(self, row_or_unit, col=None):
        """
        Select a player unit at given position or select a specific unit object
        
        Only allows selection during player-controlled turns.
        Only units from player-controlled teams that are alive and active can be selected.
        Calculates and stores valid moves, attacks, and attack ranges for the selected unit.
        
        Args:
            row_or_unit: Either grid row coordinate (int) or Unit object
            col (int, optional): Grid column coordinate (required if row_or_unit is int)
        
        Returns:
            bool: True if unit was selected, False otherwise
        """
        # Get player-controlled team IDs
        player_team_ids = [t['id'] for t in game_config.get_teams() if t.get('player_controlled', False)]
        
        # Only allow selection during player-controlled turns
        if self.current_turn not in player_team_ids:
            return False
        
        # Handle both (row, col) and direct Unit object
        if isinstance(row_or_unit, Unit):
            unit = row_or_unit
        else:
            row, col = row_or_unit, col
            unit = self.get_unit_at(row, col)
        
        # Can only select units from player-controlled teams that are active
        if unit and unit.team in player_team_ids and unit.is_alive and unit.is_active:
            self.selected_unit = unit
            self.valid_moves = self.calculate_valid_moves(unit)
            self.valid_attacks = self.calculate_valid_attacks(unit)
            
            # Calculate attack range visualization
            self.attack_range_cells = self.calculate_attack_range_cells(unit)
            self.move_attack_range_cells = self.calculate_move_attack_range_cells(unit)
            
            print(f"Selected {unit.unit_type} at {unit.position}, {len(self.valid_moves)} valid moves, {len(self.valid_attacks)} attackable enemies")
            return True
        else:
            self.deselect_unit()
            return False
    
    def deselect_unit(self):
        """
        Deselect currently selected unit and clear valid actions
        
        Clears selected_unit, valid_moves, valid_attacks, attack ranges, and movement_paths.
        """
        self.selected_unit = None
        self.valid_moves = []
        self.valid_attacks = []
        self.movement_paths = {}
        self.attack_range_cells = []
        self.move_attack_range_cells = []
        self.hovered_move = None
    
    def attempt_move_unit(self, row, col):
        """
        Attempt to move the selected unit to a destination
        
        Validates that destination is in the valid_moves list, then executes movement.
        Deducts mobility based on distance moved. Unit remains active if mobility > 0.
        
        Args:
            row (int): Destination grid row
            col (int): Destination grid column
        
        Returns:
            bool: True if move was successful, False otherwise
        """
        if not self.selected_unit:
            return False
        
        # Check if destination is valid
        if (row, col) in self.valid_moves:
            # Move the unit along the calculated path
            path = self.movement_paths.get((row, col))
            
            # Calculate mobility cost (path length - 1, since path includes starting position)
            mobility_cost = len(path) - 1 if path else 1
            
            # Store the mobility cost to be deducted when animation completes
            self.selected_unit.pending_mobility_cost = mobility_cost
            
            print(f"Moved {self.selected_unit.unit_type} to {row},{col} (cost: {mobility_cost}, remaining: {self.selected_unit.mobility - mobility_cost})")
            
            # Start the movement animation
            self.selected_unit.move_to((row, col), path=path)
            
            # Note: Mobility deduction and activation status will be updated in update()
            # when the movement animation completes. If unit has mobility remaining,
            # it will be reselected automatically.
            
            # Temporarily deselect during movement animation
            self.deselect_unit()
            return True
        
        return False
    
    def handle_click(self, row, col):
        """
        Handle a click on a grid cell
        
        Click behavior depends on current state:
        - If unit selected: Try to attack target, or move to cell, or deselect
        - If no unit selected: Try to select unit at clicked cell
        
        Only processes clicks during player-controlled turns.
        
        Args:
            row (int): Grid row clicked
            col (int): Grid column clicked
        """
        # Get player-controlled team IDs
        player_team_ids = [t['id'] for t in game_config.get_teams() if t.get('player_controlled', False)]
        
        # Only handle clicks during player-controlled turns
        if self.current_turn in player_team_ids:
            # If we have a selected unit, try to attack or move
            if self.selected_unit:
                # Check if clicking on an attackable enemy
                if self.attempt_attack(row, col):
                    return  # Attack successful
                
                # Try to move
                if self.attempt_move_unit(row, col):
                    return  # Move successful
            
            # Otherwise, try to select a unit at this position
            self.select_unit(row, col)
    
    def screen_to_grid(self, screen_x, screen_y, screen_width, screen_height):
        """
        Convert screen pixel coordinates to grid coordinates
        
        Accounts for camera offset, zoom level, and grid centering.
        Returns None if click is outside the grid bounds.
        
        Args:
            screen_x (int): Screen X coordinate in pixels
            screen_y (int): Screen Y coordinate in pixels
            screen_width (int): Width of screen in pixels
            screen_height (int): Height of screen in pixels
        
        Returns:
            tuple: (row, col) grid coordinates, or None if outside grid
        """
        # Calculate grid dimensions (same logic as draw methods)
        grid_world_width, grid_world_height = self.grid.get_grid_world_size()
        scaled_cell_size = self.grid.cell_size * self.grid.zoom
        scaled_grid_width = grid_world_width * self.grid.zoom
        scaled_grid_height = grid_world_height * self.grid.zoom
        
        # Calculate centered position
        center_x = (screen_width - scaled_grid_width) / 2 + self.grid.offset_x
        center_y = (screen_height - scaled_grid_height) / 2 + self.grid.offset_y
        
        # Convert to grid coordinates
        grid_x = (screen_x - center_x) / scaled_cell_size
        grid_y = (screen_y - center_y) / scaled_cell_size
        
        col = int(grid_x)
        row = int(grid_y)
        
        # Check if within bounds
        if 0 <= row < self.grid.grid_height and 0 <= col < self.grid.grid_width:
            return (row, col)
        
        return None
    
    def execute_enemy_turn(self):
        """
        Execute AI logic for enemy units (team 1)
        
        Placeholder for future AI implementation.
        Currently just marks all enemy units as inactive and ends turn.
        
        Future implementation should:
        - Calculate moves for each enemy unit
        - Identify attack targets
        - Execute movement and attacks
        - Use strategy/tactics
        """
        print("Enemy turn - AI placeholder")
        
        # TODO: Implement AI logic here
        # For now, just reset enemy units and end turn
        enemy_units = self.get_units_by_team(1)
        
        for unit in enemy_units:
            if unit.is_alive and unit.is_active:
                # Placeholder: Enemy units do nothing for now
                # Future: Calculate move, attack, etc.
                unit.is_active = False
        
        # End enemy turn
        self.end_turn()
    
    def end_turn(self):
        """
        End the current turn and switch to next team
        
        Uses turn order from game configuration.
        Resets all units for the new turn (restores mobility, sets active).
        Deselects any selected unit.
        If switching to AI-controlled team, automatically executes AI.
        """
        # Get turn order from config
        turn_order = game_config.get_turn_order()
        
        # Find current turn index
        try:
            current_index = turn_order.index(self.current_turn)
        except ValueError:
            current_index = 0
        
        # Switch to next team in turn order
        next_index = (current_index + 1) % len(turn_order)
        self.current_turn = turn_order[next_index]
        
        # Reset units for the new turn
        active_team_units = self.get_units_by_team(self.current_turn)
        for unit in active_team_units:
            unit.reset_turn()
        
        # Deselect any selected unit
        self.deselect_unit()
        
        # Get team name for logging
        team_config = game_config.get_team_config(self.current_turn)
        team_name = team_config['name'] if team_config else f"Team {self.current_turn}"
        print(f"\n{team_name} turn started")
        
        # If it's AI-controlled team, execute AI
        if not game_config.is_player_controlled(self.current_turn):
            self.execute_enemy_turn()
