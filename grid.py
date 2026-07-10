"""
Grid class for terrain rendering and camera control

This module implements the game's grid system, including:
- Terrain tile rendering with icons
- Camera controls (pan, zoom)
- Map loading from file
- Grid line display
- Coordinate conversions

The camera system supports:
- Panning: Click and drag to move the view
- Zooming: Mouse wheel to zoom in/out at viewport center
- Click vs drag detection: Distinguishes clicks from drags using threshold

Technical details:
- Grid is centered in screen space
- Zoom range: 0.1x to 5.0x
- Drag threshold: 5 pixels minimum movement
- Supports viewport-centered zoom (point at screen center stays fixed)
"""
import pygame
import os
from constants import GRAY


# ============================================================================
# TERRAIN PASSABILITY CONSTANTS
# ============================================================================

# Passability types control how units move through terrain
# These values match the format in map files (second value after comma)

PASSABLE_EASY = 0      # Easy terrain: sand, grass - normal movement cost
PASSABLE_SLOW = 1      # Slow terrain: swamp, rough - halved mobility when starting from
PASSABLE_BLOCKED = 2   # Blocked terrain: mountain, water - cannot pass through


class Grid:
    """
    Grid manager for terrain display and camera control
    
    Handles all aspects of the game map including:
    - Loading terrain data from files
    - Rendering terrain tiles with icons
    - Camera system (pan and zoom)
    - Grid coordinate conversions
    - Mouse interaction (click vs drag detection)
    
    The grid is rendered centered in screen space with camera offset applied.
    Zoom is centered at the viewport center (middle of screen) rather than cursor position.
    """
    
    def __init__(self, cell_size=64, map_file="map_1.txt"):
        """
        Initialize the grid with terrain data and camera settings
        
        Args:
            cell_size (int): Base size of each grid cell in pixels (default 64 for 64x64 icons)
            map_file (str): Name or path to map definition file in resources/maps/
        """
        # ========================================
        # GRID DIMENSIONS
        # ========================================
        
        # Base size of each cell in pixels (unscaled)
        self.cell_size = cell_size
        
        # Grid dimensions in cells (set by load_map)
        self.grid_width = 0   # Number of columns
        self.grid_height = 0  # Number of rows
        
        # ========================================
        # CAMERA PROPERTIES
        # ========================================
        
        # Camera offset in pixels (for panning)
        # Positive values move the grid right/down on screen
        self.offset_x = 0
        self.offset_y = 0
        
        # Zoom level (1.0 = normal size, >1 = zoomed in, <1 = zoomed out)
        self.zoom = 1.0
        self.min_zoom = 0.1   # Maximum zoom out (0.1x = see 10x more area)
        self.max_zoom = 5.0   # Maximum zoom in (5.0x = 5x magnification)
        
        # ========================================
        # MOUSE INTERACTION STATE
        # ========================================
        
        # Drag detection for panning
        self.dragging = False           # True while left mouse button is held
        self.last_mouse_pos = None      # Last recorded mouse position during drag
        self.drag_start_pos = None      # Position where drag started
        self.drag_threshold = 5         # Minimum pixels moved to count as drag (not click)
        
        # ========================================
        # DISPLAY OPTIONS
        # ========================================
        
        # Toggle for grid line visibility
        # Can be toggled with 'G' key
        self.show_grid_lines = True
        
        # ========================================
        # MAP DATA
        # ========================================
        
        # Icon cache: icon_id -> pygame.Surface
        self.icons = {}
        
        # Map terrain data: 2D array of (icon_id, passability) tuples
        # Example: map_data[row][col] = (2, PASSABLE_EASY)
        self.map_data = []
        
        # Load map from file
        self.load_map(map_file)
    
    def handle_event(self, event, screen_width=None, screen_height=None):
        """
        Process mouse and keyboard events for camera control
        
        Handles:
        - G key: Toggle grid line visibility
        - Left mouse button: Start/end dragging for panning
        - Mouse wheel: Zoom in/out at viewport center
        - Mouse motion: Update pan offset while dragging
        
        This method must be called for ALL events to properly track drag state.
        The drag detection system requires tracking mouse down, move, and up events.
        
        Args:
            event (pygame.Event): Pygame event to process
            screen_width (int, optional): Screen width for zoom calculations
            screen_height (int, optional): Screen height for zoom calculations
        """
        # ========================================
        # KEYBOARD INPUT
        # ========================================
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                # Toggle grid line visibility
                self.show_grid_lines = not self.show_grid_lines
        
        # ========================================
        # MOUSE BUTTON PRESS
        # ========================================
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button pressed
                # Start drag operation
                self.dragging = True
                self.last_mouse_pos = event.pos
                self.drag_start_pos = event.pos  # Remember where drag started
                
            elif event.button == 4:  # Mouse wheel up (scroll toward screen)
                # Zoom in by 10% at viewport center
                self.zoom_at_viewport_center(1.1, screen_width, screen_height)
                
            elif event.button == 5:  # Mouse wheel down (scroll away from screen)
                # Zoom out by 10% at viewport center
                self.zoom_at_viewport_center(1/1.1, screen_width, screen_height)
        
        # ========================================
        # MOUSE BUTTON RELEASE
        # ========================================
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button released
                # End drag operation
                self.dragging = False
                self.last_mouse_pos = None
                self.drag_start_pos = None
        
        # ========================================
        # MOUSE MOVEMENT
        # ========================================
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and self.last_mouse_pos:
                # Calculate mouse movement delta
                dx = event.pos[0] - self.last_mouse_pos[0]
                dy = event.pos[1] - self.last_mouse_pos[1]
                
                # Update camera offset (pan the view)
                # Positive dx moves grid right, positive dy moves grid down
                self.offset_x += dx
                self.offset_y += dy
                
                # Update last position for next frame
                self.last_mouse_pos = event.pos
    
    def is_dragging(self):
        """
        Check if user is actively dragging (moved beyond threshold)
        
        This is used to distinguish between clicks and drags. A drag is only
        considered active if the mouse has moved more than drag_threshold pixels
        from where the button was initially pressed.
        
        Returns:
            bool: True if mouse has moved beyond threshold while button is down
        """
        # Must have all three: button down, start position, and current position
        if not self.dragging or not self.drag_start_pos or not self.last_mouse_pos:
            return False
        
        # Calculate distance moved from start position
        dx = self.last_mouse_pos[0] - self.drag_start_pos[0]
        dy = self.last_mouse_pos[1] - self.drag_start_pos[1]
        distance = (dx**2 + dy**2) ** 0.5  # Euclidean distance
        
        # Compare to threshold (default 5 pixels)
        return distance > self.drag_threshold
    
    def zoom_at_viewport_center(self, zoom_factor, screen_width=None, screen_height=None):
        """
        Zoom in/out while keeping the viewport center position stable
        
        This creates an intuitive zoom experience where the point at the center
        of the screen stays fixed while zooming. This is more natural than zooming
        at the cursor position or at the map origin.
        
        Algorithm:
        1. Find the world position at viewport center (screen center)
        2. Apply zoom multiplier
        3. Adjust camera offset so that world position stays at viewport center
        
        Math explanation:
        - World position = (screen position - grid origin) / zoom
        - After zoom, we want: screen_center = new_grid_origin + world_pos * new_zoom
        - Solve for new_offset to maintain this relationship
        
        Args:
            zoom_factor (float): Multiplier for zoom (>1 to zoom in, <1 to zoom out)
            screen_width (int, optional): Screen width for calculations
            screen_height (int, optional): Screen height for calculations
        """
        if screen_width is None or screen_height is None:
            # Fallback to simple zoom if screen dimensions not provided
            # Just apply zoom without adjusting offset
            self.zoom = max(self.min_zoom, min(self.max_zoom, self.zoom * zoom_factor))
            return
        
        # Calculate viewport center position in screen coordinates
        viewport_center_x = screen_width / 2
        viewport_center_y = screen_height / 2
        
        # Get grid dimensions in world units (unscaled pixels)
        grid_world_width, grid_world_height = self.get_grid_world_size()
        
        # Calculate current scaled dimensions
        old_scaled_width = grid_world_width * self.zoom
        old_scaled_height = grid_world_height * self.zoom
        
        # Calculate where grid origin (top-left corner) is on screen before zoom
        # Grid is centered, so: origin = (screen - scaled_size) / 2 + offset
        old_grid_origin_x = (screen_width - old_scaled_width) / 2 + self.offset_x
        old_grid_origin_y = (screen_height - old_scaled_height) / 2 + self.offset_y
        
        # Calculate viewport center position relative to grid origin
        center_rel_x = viewport_center_x - old_grid_origin_x
        center_rel_y = viewport_center_y - old_grid_origin_y
        
        # Calculate world position at viewport center (unscaled coordinates)
        # This is the point we want to keep stable
        world_x = center_rel_x / self.zoom
        world_y = center_rel_y / self.zoom
        
        # Apply zoom (clamped to min/max range)
        old_zoom = self.zoom
        self.zoom = max(self.min_zoom, min(self.max_zoom, self.zoom * zoom_factor))
        
        # Calculate new scaled dimensions after zoom
        new_scaled_width = grid_world_width * self.zoom
        new_scaled_height = grid_world_height * self.zoom
        
        # Calculate where that world point will be relative to grid origin after zoom
        new_center_rel_x = world_x * self.zoom
        new_center_rel_y = world_y * self.zoom
        
        # Solve for new offset to keep world point at viewport center
        # We want: viewport_center = (screen - new_scaled) / 2 + new_offset + new_center_rel
        # Solving: new_offset = viewport_center - (screen - new_scaled) / 2 - new_center_rel
        self.offset_x = viewport_center_x - (screen_width - new_scaled_width) / 2 - new_center_rel_x
        self.offset_y = viewport_center_y - (screen_height - new_scaled_height) / 2 - new_center_rel_y
    
    def zoom_at_position(self, mouse_pos, zoom_factor, screen_width=None, screen_height=None):
        """
        Zoom in/out at a specific mouse position (alternative zoom mode)
        
        This keeps the world position under the mouse cursor stable while zooming.
        Currently not used (viewport center zoom is preferred), but kept for reference.
        
        Args:
            mouse_pos (tuple): (x, y) tuple of mouse screen coordinates
            zoom_factor (float): Multiplier for zoom (>1 to zoom in, <1 to zoom out)
            screen_width (int, optional): Screen width for calculations
            screen_height (int, optional): Screen height for calculations
        """
        if screen_width is None or screen_height is None:
            # Fallback to simple center zoom if screen dimensions not provided
            old_zoom = self.zoom
            self.zoom = max(self.min_zoom, min(self.max_zoom, self.zoom * zoom_factor))
            return
        
        # Get mouse position
        mouse_x, mouse_y = mouse_pos
        
        # Calculate grid dimensions
        grid_world_width, grid_world_height = self.get_grid_world_size()
        scaled_grid_width = grid_world_width * self.zoom
        scaled_grid_height = grid_world_height * self.zoom
        
        # Calculate grid top-left corner on screen
        center_x = (screen_width - scaled_grid_width) / 2 + self.offset_x
        center_y = (screen_height - scaled_grid_height) / 2 + self.offset_y
        
        # Calculate mouse position relative to grid origin
        mouse_rel_x = mouse_x - center_x
        mouse_rel_y = mouse_y - center_y
        
        # Calculate world position under mouse (before zoom)
        world_x = mouse_rel_x / self.zoom
        world_y = mouse_rel_y / self.zoom
        
        # Apply zoom
        old_zoom = self.zoom
        new_zoom = max(self.min_zoom, min(self.max_zoom, self.zoom * zoom_factor))
        self.zoom = new_zoom
        
        # Calculate new mouse position relative to grid origin (after zoom)
        new_mouse_rel_x = world_x * self.zoom
        new_mouse_rel_y = world_y * self.zoom
        
        # Adjust offset so that the world position stays under the mouse
        # The difference shows how much the point moved, so we move grid the opposite way
        self.offset_x -= (new_mouse_rel_x - mouse_rel_x)
        self.offset_y -= (new_mouse_rel_y - mouse_rel_y)
    
    def load_icon(self, icon_id):
        """
        Load a terrain icon from file and cache it
        
        Icons are loaded from resources/icons/ directory. Tries PNG first, then BMP.
        Loaded icons are cached in self.icons dictionary to avoid reloading.
        
        Args:
            icon_id (int): The icon number to load (e.g., 1 for icon_1.png)
        
        Returns:
            pygame.Surface: Loaded icon image, or None if not found
        """
        # Check cache first
        if icon_id in self.icons:
            return self.icons[icon_id]
        
        # Try loading PNG first (preferred format)
        png_path = f"resources/icons/icon_{icon_id}.png"
        if os.path.exists(png_path):
            try:
                icon = pygame.image.load(png_path)
                self.icons[icon_id] = icon  # Cache for future use
                return icon
            except pygame.error as e:
                print(f"Error loading {png_path}: {e}")
        
        # Fall back to BMP if PNG not found
        bmp_path = f"resources/icons/icon_{icon_id}.bmp"
        if os.path.exists(bmp_path):
            try:
                icon = pygame.image.load(bmp_path)
                self.icons[icon_id] = icon  # Cache for future use
                return icon
            except pygame.error as e:
                print(f"Error loading {bmp_path}: {e}")
        
        # Return None if icon not found - will draw placeholder
        return None
    
    def load_map(self, map_file):
        """
        Load map terrain data from file
        
        Map file format:
        - Each line represents a row of the grid
        - Each cell is "icon_id,passability" separated by spaces
        - Passability: 0=easy (normal), 1=slow (halved mobility), 2=blocked (impassable)
        - Lines starting with # are comments
        - Empty lines are skipped
        
        Example map file:
        # Simple 3x3 map
        1,0 1,0 1,0
        1,0 2,0 1,0
        1,0 1,0 1,0
        
        This creates a 3x3 map with icon_1 terrain (easy passable) everywhere
        except the center which is icon_2 (also easy passable).
        
        Args:
            map_file (str): Path to map file or just filename (will look in resources/maps/)
        """
        self.map_data = []
        
        # If just a filename, prepend resources/maps/ directory
        if not os.path.dirname(map_file):
            map_file = f"resources/maps/{map_file}"
        
        # Check if file exists
        if not os.path.exists(map_file):
            print(f"Warning: Map file {map_file} not found. Creating default 10x10 map.")
            # Create default 10x10 empty map with icon_1 (easy terrain)
            for row in range(10):
                self.map_data.append([(1, PASSABLE_EASY) for _ in range(10)])
            self.grid_height = 10
            self.grid_width = 10
            return
        
        try:
            with open(map_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse cells in this row
                    row = []
                    cells = line.split()  # Split on whitespace
                    for cell in cells:
                        if ',' in cell:
                            # Format: "icon_id,passability"
                            icon_id, passability = cell.split(',')
                            row.append((int(icon_id), int(passability)))
                        else:
                            # Just icon_id - default to easy passability
                            row.append((int(cell), PASSABLE_EASY))
                    
                    self.map_data.append(row)
            
            # Set grid dimensions from loaded data
            self.grid_height = len(self.map_data)
            self.grid_width = len(self.map_data[0]) if self.map_data else 0
            
            # Preload all unique icons used in the map
            unique_icons = set()
            for row in self.map_data:
                for icon_id, _ in row:
                    unique_icons.add(icon_id)
            
            for icon_id in unique_icons:
                self.load_icon(icon_id)
            
            print(f"Loaded map from {map_file}: {self.grid_height}x{self.grid_width}")
        
        except Exception as e:
            print(f"Error loading map file {map_file}: {e}")
            # Create default 10x10 empty map as fallback
            for row in range(10):
                self.map_data.append([(1, PASSABLE_EASY) for _ in range(10)])
            self.grid_height = 10
            self.grid_width = 10
    
    def get_grid_world_size(self):
        """
        Get the total size of the grid in world units (unscaled pixels)
        
        World size is the grid dimensions multiplied by cell size, before
        applying zoom. This is useful for camera calculations.
        
        Returns:
            tuple: (width, height) in world pixels
        """
        return (self.grid_width * self.cell_size, self.grid_height * self.cell_size)
    
    def draw(self, screen):
        """
        Render the grid with terrain icons and optional grid lines
        
        Rendering process:
        1. Calculate grid position (centered with camera offset applied)
        2. Draw terrain icons for each cell (scaled by zoom)
        3. Draw grid lines if enabled (optional overlay)
        
        The grid is rendered centered in screen space. Camera offset and zoom
        are applied to create the pan/zoom effect.
        
        Args:
            screen (pygame.Surface): Pygame surface to draw on
        """
        # Get screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Calculate grid dimensions
        grid_world_width, grid_world_height = self.get_grid_world_size()
        scaled_cell_size = self.cell_size * self.zoom
        scaled_grid_width = grid_world_width * self.zoom
        scaled_grid_height = grid_world_height * self.zoom
        
        # Calculate centered position with camera offset applied
        # Grid is centered: (screen - scaled_grid) / 2, then offset is added
        center_x = (screen_width - scaled_grid_width) / 2 + self.offset_x
        center_y = (screen_height - scaled_grid_height) / 2 + self.offset_y
        
        # ========================================
        # DRAW TERRAIN TILES
        # ========================================
        
        # Draw each cell with its terrain icon
        for row in range(len(self.map_data)):
            for col in range(len(self.map_data[row])):
                # Get terrain data for this cell
                icon_id, passability = self.map_data[row][col]
                
                # Calculate cell position on screen
                x = center_x + col * scaled_cell_size
                y = center_y + row * scaled_cell_size
                
                # Get terrain icon from cache
                icon = self.icons.get(icon_id)
                
                if icon:
                    # Scale icon to current cell size (based on zoom)
                    scaled_icon = pygame.transform.scale(icon, 
                                                        (int(scaled_cell_size), 
                                                         int(scaled_cell_size)))
                    screen.blit(scaled_icon, (x, y))
                else:
                    # Draw gray placeholder if icon not found
                    color = (100, 100, 100)  # Medium gray
                    pygame.draw.rect(screen, color, 
                                   (x, y, scaled_cell_size, scaled_cell_size))
        
        # ========================================
        # DRAW GRID LINES (OPTIONAL)
        # ========================================
        
        if self.show_grid_lines:
            # Draw vertical lines (columns)
            for i in range(self.grid_width + 1):
                x = center_x + i * scaled_cell_size
                y1 = center_y
                y2 = center_y + scaled_grid_height
                pygame.draw.line(screen, GRAY, (x, y1), (x, y2), 1)
            
            # Draw horizontal lines (rows)
            for i in range(self.grid_height + 1):
                y = center_y + i * scaled_cell_size
                x1 = center_x
                x2 = center_x + scaled_grid_width
                pygame.draw.line(screen, GRAY, (x1, y), (x2, y), 1)
    
    def scale_to_screen_height(self, screen_height, margin=50):
        """
        Auto-scale zoom to fit the entire grid height on screen
        
        Calculates and applies a zoom level that makes the grid fit vertically
        within the screen, with optional margins. Useful for initial zoom setup
        to ensure the map is visible without manual zooming.
        
        Args:
            screen_height (int): Height of the screen in pixels
            margin (int): Margin to leave at top and bottom of screen (default 50)
        """
        # Calculate available vertical space (screen minus margins)
        available_height = screen_height - (2 * margin)
        
        # Get grid world height (unscaled)
        _, grid_world_height = self.get_grid_world_size()
        
        # Calculate zoom to fit: available_height = grid_world_height * zoom
        self.zoom = available_height / grid_world_height
