"""
Strategy Game Editor - Map and Scenario Editor

A graphical editor for creating and editing maps, unit placements, and scenarios
for the strategy game engine. This is a standalone tool that saves to the game's
resource directories.

Features:
- Visual map editing with terrain tiles
- Unit placement with team assignment
- Scenario metadata editing
- Save/load functionality
- Mouse and keyboard controls

Usage:
    python editor.py
"""

import pygame
import sys
import json
from pathlib import Path
from config import game_config
import os
import os

# ============================================================================
# CONSTANTS
# ============================================================================

EDITOR_WIDTH = 1400
EDITOR_HEIGHT = 900
CELL_SIZE = 40
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
BLUE = (100, 150, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 100)

# UI Layout
TOOLBAR_HEIGHT = 60
PANEL_WIDTH = 250
STATUS_HEIGHT = 30

# Terrain types - dynamically loaded from resources/terrains.json
def load_terrain_types():
    """Load terrain types from JSON file or use defaults"""
    terrain_file = Path("resources/terrains.json")
    
    default_terrains = {
        0: {"name": "Grass", "color": (34, 139, 34), "passability": 0, "icon": "grass"},
        1: {"name": "Water", "color": (0, 105, 148), "passability": 2, "icon": "water"},
        2: {"name": "Mountain", "color": (139, 90, 43), "passability": 2, "icon": "mountain"},
        3: {"name": "Forest", "color": (0, 100, 0), "passability": 1, "icon": "forest"},
        4: {"name": "Sand", "color": (238, 214, 175), "passability": 0, "icon": "sand"},
        5: {"name": "Road", "color": (169, 169, 169), "passability": 0, "icon": "road"},
    }
    
    if not terrain_file.exists():
        # Create default terrain file
        terrain_file.parent.mkdir(parents=True, exist_ok=True)
        with open(terrain_file, 'w') as f:
            json.dump(default_terrains, f, indent=2)
        return default_terrains
    
    try:
        with open(terrain_file, 'r') as f:
            terrains = json.load(f)
            # Convert string keys to integers and ensure color is tuple
            result = {}
            for key, value in terrains.items():
                terrain_id = int(key)
                value['color'] = tuple(value['color']) if isinstance(value['color'], list) else value['color']
                result[terrain_id] = value
            return result
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error loading terrains.json: {e}")
        return default_terrains

def save_terrain_types(terrains):
    """Save terrain types to JSON file"""
    terrain_file = Path("resources/terrains.json")
    terrain_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert to serializable format
    serializable = {}
    for key, value in terrains.items():
        terrain_data = value.copy()
        terrain_data['color'] = list(terrain_data['color'])  # Convert tuple to list for JSON
        serializable[str(key)] = terrain_data
    
    with open(terrain_file, 'w') as f:
        json.dump(serializable, f, indent=2)

TERRAIN_TYPES = load_terrain_types()

# Unit types - dynamically loaded from resources/units/
def get_available_unit_types():
    """Get list of available unit types from resources/units/ directory"""
    unit_dir = Path("resources/units")
    if not unit_dir.exists():
        return ["soldier", "archer", "knight", "catapult"]  # Fallback
    
    unit_types = []
    for file in unit_dir.glob("*.json"):
        unit_types.append(file.stem)
    return sorted(unit_types) if unit_types else ["soldier", "archer", "knight", "catapult"]

UNIT_TYPES = get_available_unit_types()

# Editor modes
MODE_TERRAIN = "terrain"
MODE_UNITS = "units"
MODE_CREATE_UNIT = "create_unit"
MODE_CREATE_TERRAIN = "create_terrain"

# Passability labels
PASSABILITY_LABELS = {
    0: "Easy",
    1: "Slow",
    2: "Blocked"
}

# ============================================================================
# EDITOR CLASS
# ============================================================================

class ScenarioEditor:
    """
    Main editor class for creating and editing game scenarios
    """
    
    def __init__(self):
        """Initialize the editor"""
        pygame.init()
        
        # Setup display
        self.screen = pygame.display.set_mode((EDITOR_WIDTH, EDITOR_HEIGHT))
        pygame.display.set_caption("Strategy Game Editor")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.large_font = pygame.font.Font(None, 32)
        
        # Editor state
        self.running = True
        self.mode = MODE_TERRAIN
        self.selected_terrain = 0
        self.selected_unit = UNIT_TYPES[0] if UNIT_TYPES else "soldier"
        self.selected_team = 0
        
        # Unit creator state
        self.creating_unit = False
        self.editing_unit_name = None  # Name of unit being edited (None if creating new)
        self.unit_form_data = {}
        self.active_input_field = None
        self.input_text = ""
        
        # Terrain creator state
        self.creating_terrain = False
        self.editing_terrain_id = None  # ID of terrain being edited (None if creating new)
        self.terrain_form_data = {}
        self.color_component = 0  # 0=R, 1=G, 2=B
        
        # Map data
        self.map_width = 15
        self.map_height = 10
        self.map_data = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.units = []  # List of {"type": str, "team": int, "row": int, "col": int}
        
        # Scenario metadata
        self.scenario_number = 1
        self.scenario_description = "New scenario"
        
        # UI state
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        
        # Calculate grid area
        self.grid_x = PANEL_WIDTH
        self.grid_y = TOOLBAR_HEIGHT
        self.grid_width = EDITOR_WIDTH - PANEL_WIDTH * 2
        self.grid_height = EDITOR_HEIGHT - TOOLBAR_HEIGHT - STATUS_HEIGHT
        
        print("Strategy Game Editor started")
        print("Controls:")
        print("  Left Panel: Select terrain/unit type")
        print("  Click on grid: Place terrain/unit")
        print("  Right-click: Erase")
        print("  T: Terrain mode")
        print("  U: Units mode")
        print("  S: Save scenario")
        print("  L: Load scenario")
        print("  N: New scenario")
        print("  [ / ]: Change scenario number")
        print("  +/-: Change grid size")
        print("  1-6: Quick select terrain")
        print("  Q: Quit")
    
    def run(self):
        """Main editor loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Check if unit creator handles this event
                if not self.handle_unit_creator_input(event):
                    # Check if terrain creator handles this event
                    if not self.handle_terrain_creator_input(event):
                        # If not, handle normal keypresses
                        self.handle_keypress(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.button, event.pos)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    self.handle_mouse_drag(event.pos)
    
    def handle_keypress(self, key):
        """Handle keyboard input"""
        if key == pygame.K_q or key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_t:
            self.mode = MODE_TERRAIN
            self.creating_terrain = False
        elif key == pygame.K_u:
            self.mode = MODE_UNITS
            self.creating_unit = False
        elif key == pygame.K_s:
            self.save_scenario()
        elif key == pygame.K_l:
            self.load_scenario()
        elif key == pygame.K_n:
            self.new_scenario()
        elif key == pygame.K_PLUS or key == pygame.K_EQUALS:
            self.change_grid_size(1, 1)
        elif key == pygame.K_MINUS:
            self.change_grid_size(-1, -1)
        elif key == pygame.K_LEFTBRACKET:  # [ key
            self.change_scenario(-1)
        elif key == pygame.K_RIGHTBRACKET:  # ] key
            self.change_scenario(1)
        elif pygame.K_1 <= key <= pygame.K_6:
            terrain_id = key - pygame.K_1
            if terrain_id < len(TERRAIN_TYPES):
                self.selected_terrain = terrain_id
    
    def handle_mouse_click(self, button, pos):
        """Handle mouse clicks"""
        x, y = pos
        
        # Check if clicking in toolbar (scenario selector)
        if y < TOOLBAR_HEIGHT:
            self.handle_toolbar_click(x, y)
            return
        
        # Check if clicking in grid area
        if self.grid_x <= x < self.grid_x + self.grid_width and \
           self.grid_y <= y < self.grid_y + self.grid_height:
            
            # Convert to grid coordinates
            grid_x = (x - self.grid_x) // CELL_SIZE
            grid_y = (y - self.grid_y) // CELL_SIZE
            
            if 0 <= grid_x < self.map_width and 0 <= grid_y < self.map_height:
                if button == 1:  # Left click
                    if self.mode == MODE_TERRAIN:
                        self.map_data[grid_y][grid_x] = self.selected_terrain
                    elif self.mode == MODE_UNITS:
                        self.place_unit(grid_y, grid_x)
                elif button == 3:  # Right click
                    if self.mode == MODE_TERRAIN:
                        self.map_data[grid_y][grid_x] = 0  # Reset to grass
                    elif self.mode == MODE_UNITS:
                        self.remove_unit(grid_y, grid_x)
        
        # Check if clicking in left panel (terrain/unit selection)
        elif x < PANEL_WIDTH:
            self.handle_panel_click(x, y)
    
    def handle_toolbar_click(self, x, y):
        """Handle clicks in the toolbar"""
        # Scenario selector buttons (< and > around scenario number)
        # Position around x=400, y=20
        prev_btn = pygame.Rect(380, 15, 30, 30)
        next_btn = pygame.Rect(560, 15, 30, 30)
        
        if prev_btn.collidepoint(x, y):
            self.change_scenario(-1)
        elif next_btn.collidepoint(x, y):
            self.change_scenario(1)
    
    def change_scenario(self, delta):
        """Change the active scenario number and auto-load if exists"""
        new_number = max(1, min(99, self.scenario_number + delta))
        if new_number != self.scenario_number:
            self.scenario_number = new_number
            print(f"Switched to scenario {self.scenario_number}")
            # Check if scenario exists and auto-load
            map_file = Path(f"resources/maps/map_{self.scenario_number}.txt")
            if map_file.exists():
                print(f"  → Scenario exists, loading automatically...")
                self.load_scenario()
            else:
                print(f"  → New scenario - build your map and press 'S' to save")
                # Clear map and units for new scenario
                self.map_data = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
                self.units = []
                self.scenario_description = "New scenario"
    
    def handle_mouse_drag(self, pos):
        """Handle mouse dragging"""
        # Could implement camera pan here if needed
        pass
    
    def handle_panel_click(self, x, y):
        """Handle clicks in the left panel"""
        if self.mode == MODE_TERRAIN:
            if self.creating_terrain:
                # Handle clicks in terrain creator form
                self.handle_terrain_creator_click(x, y)
            else:
                # Terrain selection area
                start_y = TOOLBAR_HEIGHT + 40
                for i, (terrain_id, terrain_info) in enumerate(TERRAIN_TYPES.items()):
                    btn_y = start_y + i * 40
                    if btn_y <= y < btn_y + 35:
                        # Check if clicking edit button
                        edit_btn_rect = pygame.Rect(PANEL_WIDTH - 55, btn_y, 45, 35)
                        if edit_btn_rect.collidepoint(x, y):
                            self.start_terrain_editor(terrain_id)
                            return
                        else:
                            # Regular selection
                            self.selected_terrain = terrain_id
                        break
                
                # Create New Terrain button
                create_btn_y = start_y + len(TERRAIN_TYPES) * 40 + 10
                if create_btn_y <= y < create_btn_y + 40:
                    self.start_terrain_creator()
                    return
        
        elif self.mode == MODE_UNITS:
            if self.creating_unit:
                # Handle clicks in unit creator form
                self.handle_unit_creator_click(x, y)
            else:
                # Unit type selection
                start_y = TOOLBAR_HEIGHT + 40
                for i, unit_type in enumerate(UNIT_TYPES):
                    btn_y = start_y + i * 40
                    if btn_y <= y < btn_y + 35:
                        # Check if clicking edit button
                        edit_btn_rect = pygame.Rect(PANEL_WIDTH - 55, btn_y, 45, 35)
                        if edit_btn_rect.collidepoint(x, y):
                            self.start_unit_editor(unit_type)
                            return
                        else:
                            # Regular selection
                            self.selected_unit = unit_type
                        break
                
                # Create New Unit button
                create_btn_y = start_y + len(UNIT_TYPES) * 40 + 10
                if create_btn_y <= y < create_btn_y + 40:
                    self.start_unit_creator()
                    return
                
                # Team selection
                team_y = create_btn_y + 50 + 40
                for i, team in enumerate(game_config.get_teams()):
                    btn_y = team_y + i * 35
                    if btn_y <= y < btn_y + 30:
                        self.selected_team = team['id']
                        break
    
    def place_unit(self, row, col):
        """Place a unit at the specified position"""
        # Remove any existing unit at this position
        self.remove_unit(row, col)
        
        # Add new unit
        self.units.append({
            "type": self.selected_unit,
            "team": self.selected_team,
            "row": row,
            "col": col
        })
    
    def remove_unit(self, row, col):
        """Remove unit at the specified position"""
        self.units = [u for u in self.units if not (u["row"] == row and u["col"] == col)]
    
    def get_unit_at(self, row, col):
        """Get unit at specified position"""
        for unit in self.units:
            if unit["row"] == row and unit["col"] == col:
                return unit
        return None
    
    def start_unit_creator(self):
        """Start the unit creation process"""
        self.creating_unit = True
        self.editing_unit_name = None
        self.unit_form_data = {
            "name": "",
            "max_health": "100",
            "attack_power": "20",
            "defense": "5",
            "attack_range": "1",
            "max_mobility": "3",
            "speed": "10",
            "projectile_speed": "15",
            "projectile_count": "1",
            "projectile_sprite": "null",
            "hit_chance": "0.95",
            "damage_std": "2.0",
            "fire_type": "direct",
            "vision_range": "5"
        }
        self.active_input_field = "name"
        print("Unit creator started. Enter unit details.")
    
    def start_unit_editor(self, unit_name):
        """Start editing an existing unit"""
        unit_file = Path(f"resources/units/{unit_name}.json")
        if not unit_file.exists():
            print(f"Error: Unit file not found: {unit_file}")
            return
        
        try:
            with open(unit_file, 'r') as f:
                unit_data = json.load(f)
            
            self.creating_unit = True
            self.editing_unit_name = unit_name
            self.unit_form_data = {
                "name": unit_name,
                "max_health": str(unit_data.get("max_health", 100)),
                "attack_power": str(unit_data.get("attack_power", 20)),
                "defense": str(unit_data.get("defense", 5)),
                "attack_range": str(unit_data.get("attack_range", 1)),
                "max_mobility": str(unit_data.get("max_mobility", 3)),
                "speed": str(unit_data.get("speed", 10)),
                "projectile_speed": str(unit_data.get("projectile_speed", 15)),
                "projectile_count": str(unit_data.get("projectile_count", 1)),
                "projectile_sprite": str(unit_data.get("projectile_sprite") or "null"),
                "hit_chance": str(unit_data.get("hit_chance", 0.95)),
                "damage_std": str(unit_data.get("damage_std", 2.0)),
                "fire_type": str(unit_data.get("fire_type", "direct")),
                "vision_range": str(unit_data.get("vision_range", 5))
            }
            self.active_input_field = "name"
            print(f"Editing unit: {unit_name}")
        except Exception as e:
            print(f"Error loading unit data: {e}")
    
    def draw_unit_creator(self, y_start):
        """Draw the unit creator form"""
        y_offset = y_start
        
        # Title
        title_text = "Edit Unit" if self.editing_unit_name else "Create New Unit"
        title = self.font.render(title_text, True, BLACK)
        self.screen.blit(title, (10, y_offset))
        y_offset += 35
        
        # Form fields - now includes projectile_sprite
        fields = [
            ("name", "Name:"),
            ("max_health", "Health:"),
            ("attack_power", "Attack:"),
            ("defense", "Defense:"),
            ("attack_range", "Range:"),
            ("max_mobility", "Mobility:"),
            ("vision_range", "Vision:"),
            ("projectile_sprite", "Proj Sprite:"),
        ]
        
        for field_key, field_label in fields:
            # Field label
            label_surf = self.small_font.render(field_label, True, BLACK)
            self.screen.blit(label_surf, (15, y_offset))
            
            # Input box
            input_rect = pygame.Rect(120, y_offset - 2, 110, 20)
            is_active = (self.active_input_field == field_key)
            color = YELLOW if is_active else WHITE
            pygame.draw.rect(self.screen, color, input_rect)
            pygame.draw.rect(self.screen, BLACK, input_rect, 1)
            
            # Input text
            value = self.unit_form_data.get(field_key, "")
            if is_active:
                value = self.input_text
            value_surf = self.small_font.render(str(value), True, BLACK)
            self.screen.blit(value_surf, (123, y_offset))
            
            y_offset += 25
        
        # Save and Cancel buttons
        y_offset += 10
        
        # Save button
        save_btn = pygame.Rect(10, y_offset, 110, 30)
        pygame.draw.rect(self.screen, GREEN, save_btn)
        pygame.draw.rect(self.screen, BLACK, save_btn, 2)
        save_text = self.small_font.render("Save Unit", True, BLACK)
        self.screen.blit(save_text, (20, y_offset + 7))
        
        # Cancel button
        cancel_btn = pygame.Rect(130, y_offset, 110, 30)
        pygame.draw.rect(self.screen, RED, cancel_btn)
        pygame.draw.rect(self.screen, BLACK, cancel_btn, 2)
        cancel_text = self.small_font.render("Cancel", True, BLACK)
        self.screen.blit(cancel_text, (155, y_offset + 7))
    
    def handle_unit_creator_click(self, x, y):
        """Handle clicks in unit creator form"""
        # Check field clicks
        y_offset = TOOLBAR_HEIGHT + 45
        fields = ["name", "max_health", "attack_power", "defense", "attack_range", "max_mobility", "vision_range", "projectile_sprite"]
        
        for field in fields:
            input_rect = pygame.Rect(120, y_offset - 2, 110, 20)
            if input_rect.collidepoint(x, y):
                self.active_input_field = field
                self.input_text = str(self.unit_form_data.get(field, ""))
                return
            y_offset += 25
        
        # Check button clicks
        y_offset += 10
        
        # Save button
        save_btn = pygame.Rect(10, y_offset, 110, 30)
        if save_btn.collidepoint(x, y):
            self.save_unit_definition()
            return
        
        # Cancel button
        cancel_btn = pygame.Rect(130, y_offset, 110, 30)
        if cancel_btn.collidepoint(x, y):
            self.creating_unit = False
            self.active_input_field = None
            self.input_text = ""
            print("Unit creation cancelled")
    
    def handle_unit_creator_input(self, event):
        """Handle text input for unit creator"""
        if not self.creating_unit or not self.active_input_field:
            return False
        
        if event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
            # Save current field and move to next or save
            self.unit_form_data[self.active_input_field] = self.input_text
            
            # Move to next field
            fields = ["name", "max_health", "attack_power", "defense", "attack_range", "max_mobility", "vision_range", "projectile_sprite"]
            try:
                current_idx = fields.index(self.active_input_field)
                if current_idx < len(fields) - 1:
                    self.active_input_field = fields[current_idx + 1]
                    self.input_text = str(self.unit_form_data.get(self.active_input_field, ""))
                else:
                    # Last field, save unit
                    self.save_unit_definition()
            except ValueError:
                pass
            return True
        
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
            return True
        
        elif event.key == pygame.K_ESCAPE:
            self.creating_unit = False
            self.active_input_field = None
            self.input_text = ""
            return True
        
        elif event.unicode and event.unicode.isprintable():
            self.input_text += event.unicode
            return True
        
        return False
    
    def save_unit_definition(self):
        """Save the unit definition to a JSON file"""
        # Update form data with current input
        if self.active_input_field:
            self.unit_form_data[self.active_input_field] = self.input_text
        
        unit_name = self.unit_form_data.get("name", "").strip().lower()
        if not unit_name:
            print("Error: Unit name is required")
            return
        
        # Check if this is an edit and name changed
        if self.editing_unit_name and self.editing_unit_name != unit_name:
            old_file = Path(f"resources/units/{self.editing_unit_name}.json")
            if old_file.exists():
                old_file.unlink()
                print(f"Renamed unit from '{self.editing_unit_name}' to '{unit_name}'")
        
        # Check if unit already exists (for new units)
        unit_file = Path(f"resources/units/{unit_name}.json")
        if not self.editing_unit_name and unit_file.exists():
            print(f"Warning: Unit '{unit_name}' already exists. Overwriting...")
        
        # Build unit definition
        try:
            # Handle projectile_sprite - convert "null" or "None" strings to None
            projectile_sprite_value = self.unit_form_data.get("projectile_sprite", "null").strip()
            if projectile_sprite_value.lower() in ["null", "none", ""]:
                projectile_sprite_value = None
            
            unit_def = {
                "max_health": int(self.unit_form_data.get("max_health", "100")),
                "attack_power": int(self.unit_form_data.get("attack_power", "20")),
                "defense": int(self.unit_form_data.get("defense", "5")),
                "attack_range": int(self.unit_form_data.get("attack_range", "1")),
                "max_mobility": int(self.unit_form_data.get("max_mobility", "3")),
                "speed": int(self.unit_form_data.get("speed", "10")),
                "projectile_speed": int(self.unit_form_data.get("projectile_speed", "15")),
                "projectile_count": int(self.unit_form_data.get("projectile_count", "1")),
                "projectile_sprite": projectile_sprite_value,
                "hit_chance": float(self.unit_form_data.get("hit_chance", "0.95")),
                "damage_std": float(self.unit_form_data.get("damage_std", "2.0")),
                "fire_type": self.unit_form_data.get("fire_type", "direct"),
                "vision_range": int(self.unit_form_data.get("vision_range", "5"))
            }
        except ValueError as e:
            print(f"Error: Invalid unit attribute values: {e}")
            return
        
        # Create directory if needed
        Path("resources/units").mkdir(parents=True, exist_ok=True)
        
        # Save to file
        with open(unit_file, 'w') as f:
            json.dump(unit_def, f, indent=2)
        
        action = "updated" if self.editing_unit_name else "created"
        print(f"Unit '{unit_name}' {action} successfully!")
        print(f"  File: {unit_file}")
        if unit_def.get("projectile_sprite") and unit_def["projectile_sprite"] != "null":
            print(f"  Projectile: {unit_def['projectile_sprite']}")
        
        # Refresh unit types list
        global UNIT_TYPES
        UNIT_TYPES = get_available_unit_types()
        self.selected_unit = unit_name
        
        # Exit creator mode
        self.creating_unit = False
        self.editing_unit_name = None
        self.active_input_field = None
        self.input_text = ""
    
    def start_terrain_creator(self):
        """Start the terrain creation process"""
        self.creating_terrain = True
        self.editing_terrain_id = None  # Reset editing mode
        self.terrain_form_data = {
            "name": "",
            "passability": "0",
            "color_r": "100",
            "color_g": "200",
            "color_b": "100",
            "icon": "custom"
        }
        self.active_input_field = "name"
        self.color_component = 0
        print("Terrain creator started. Enter terrain details.")
    
    def start_terrain_editor(self, terrain_id):
        """Load an existing terrain for editing"""
        global TERRAIN_TYPES
        terrain_data = TERRAIN_TYPES[terrain_id]
        self.creating_terrain = True
        self.editing_terrain_id = terrain_id
        self.terrain_form_data = {
            "name": terrain_data.get("name", ""),
            "passability": str(terrain_data.get("passability", 0)),
            "color_r": str(terrain_data.get("color", (100, 200, 100))[0]),
            "color_g": str(terrain_data.get("color", (100, 200, 100))[1]),
            "color_b": str(terrain_data.get("color", (100, 200, 100))[2]),
            "icon": terrain_data.get("icon", "custom")
        }
        self.active_input_field = "name"
        self.input_text = self.terrain_form_data["name"]  # Pre-fill name in input
        self.color_component = 0
        print(f"Editing terrain: {terrain_data.get('name', 'Unknown')} (ID: {terrain_id})")
    
    def draw_terrain_creator(self, y_start):
        """Draw the terrain creator form"""
        y_offset = y_start
        
        # Title
        title_text = "Edit Terrain" if self.editing_terrain_id is not None else "Create Terrain"
        title = self.font.render(title_text, True, BLACK)
        self.screen.blit(title, (10, y_offset))
        y_offset += 35
        
        # Name field
        label_surf = self.small_font.render("Name:", True, BLACK)
        self.screen.blit(label_surf, (15, y_offset))
        input_rect = pygame.Rect(120, y_offset - 2, 110, 20)
        is_active = (self.active_input_field == "name")
        color = YELLOW if is_active else WHITE
        pygame.draw.rect(self.screen, color, input_rect)
        pygame.draw.rect(self.screen, BLACK, input_rect, 1)
        value = self.input_text if is_active else self.terrain_form_data.get("name", "")
        value_surf = self.small_font.render(str(value), True, BLACK)
        self.screen.blit(value_surf, (123, y_offset))
        y_offset += 25
        
        # Passability selector
        label_surf = self.small_font.render("Mobility:", True, BLACK)
        self.screen.blit(label_surf, (15, y_offset))
        
        # Passability buttons
        btn_y = y_offset - 2
        for pass_val, pass_label in [(0, "Easy"), (1, "Slow"), (2, "Block")]:
            btn_x = 90 + pass_val * 50
            btn_rect = pygame.Rect(btn_x, btn_y, 45, 20)
            current_pass = int(self.terrain_form_data.get("passability", "0"))
            btn_color = YELLOW if current_pass == pass_val else WHITE
            pygame.draw.rect(self.screen, btn_color, btn_rect)
            pygame.draw.rect(self.screen, BLACK, btn_rect, 1)
            text_surf = self.small_font.render(pass_label, True, BLACK)
            text_rect = text_surf.get_rect(center=btn_rect.center)
            self.screen.blit(text_surf, text_rect)
        y_offset += 25
        
        # Color fields (RGB)
        color_fields = [("R", "color_r"), ("G", "color_g"), ("B", "color_b")]
        for i, (label, field_key) in enumerate(color_fields):
            label_surf = self.small_font.render(f"Color {label}:", True, BLACK)
            self.screen.blit(label_surf, (15, y_offset))
            
            input_rect = pygame.Rect(120, y_offset - 2, 110, 20)
            is_active = (self.active_input_field == field_key)
            color = YELLOW if is_active else WHITE
            pygame.draw.rect(self.screen, color, input_rect)
            pygame.draw.rect(self.screen, BLACK, input_rect, 1)
            
            value = self.input_text if is_active else self.terrain_form_data.get(field_key, "0")
            value_surf = self.small_font.render(str(value), True, BLACK)
            self.screen.blit(value_surf, (123, y_offset))
            y_offset += 25
        
        # Color preview
        y_offset += 5
        try:
            r = int(self.terrain_form_data.get("color_r", "100"))
            g = int(self.terrain_form_data.get("color_g", "200"))
            b = int(self.terrain_form_data.get("color_b", "100"))
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            preview_color = (r, g, b)
        except ValueError:
            preview_color = (100, 200, 100)
        
        label_surf = self.small_font.render("Preview:", True, BLACK)
        self.screen.blit(label_surf, (15, y_offset))
        preview_rect = pygame.Rect(90, y_offset - 2, 140, 30)
        pygame.draw.rect(self.screen, preview_color, preview_rect)
        pygame.draw.rect(self.screen, BLACK, preview_rect, 2)
        y_offset += 40
        
        # Icon field
        label_surf = self.small_font.render("Icon:", True, BLACK)
        self.screen.blit(label_surf, (15, y_offset))
        input_rect = pygame.Rect(120, y_offset - 2, 110, 20)
        is_active = (self.active_input_field == "icon")
        color = YELLOW if is_active else WHITE
        pygame.draw.rect(self.screen, color, input_rect)
        pygame.draw.rect(self.screen, BLACK, input_rect, 1)
        value = self.input_text if is_active else self.terrain_form_data.get("icon", "")
        value_surf = self.small_font.render(str(value), True, BLACK)
        self.screen.blit(value_surf, (123, y_offset))
        y_offset += 30
        
        # Save and Cancel buttons
        save_btn = pygame.Rect(10, y_offset, 110, 30)
        pygame.draw.rect(self.screen, GREEN, save_btn)
        pygame.draw.rect(self.screen, BLACK, save_btn, 2)
        save_text = self.small_font.render("Save Terrain", True, BLACK)
        self.screen.blit(save_text, (17, y_offset + 7))
        
        cancel_btn = pygame.Rect(130, y_offset, 110, 30)
        pygame.draw.rect(self.screen, RED, cancel_btn)
        pygame.draw.rect(self.screen, BLACK, cancel_btn, 2)
        cancel_text = self.small_font.render("Cancel", True, BLACK)
        self.screen.blit(cancel_text, (155, y_offset + 7))
    
    def handle_terrain_creator_click(self, x, y):
        """Handle clicks in terrain creator form"""
        y_offset = TOOLBAR_HEIGHT + 45
        
        # Name field
        input_rect = pygame.Rect(120, y_offset - 2, 110, 20)
        if input_rect.collidepoint(x, y):
            self.active_input_field = "name"
            self.input_text = str(self.terrain_form_data.get("name", ""))
            return
        y_offset += 25
        
        # Passability buttons
        for pass_val in [0, 1, 2]:
            btn_x = 90 + pass_val * 50
            btn_rect = pygame.Rect(btn_x, y_offset - 2, 45, 20)
            if btn_rect.collidepoint(x, y):
                self.terrain_form_data["passability"] = str(pass_val)
                return
        y_offset += 25
        
        # Color fields
        for field_key in ["color_r", "color_g", "color_b"]:
            input_rect = pygame.Rect(120, y_offset - 2, 110, 20)
            if input_rect.collidepoint(x, y):
                self.active_input_field = field_key
                self.input_text = str(self.terrain_form_data.get(field_key, "0"))
                return
            y_offset += 25
        
        y_offset += 45  # Skip preview
        
        # Icon field
        input_rect = pygame.Rect(120, y_offset - 2, 110, 20)
        if input_rect.collidepoint(x, y):
            self.active_input_field = "icon"
            self.input_text = str(self.terrain_form_data.get("icon", ""))
            return
        y_offset += 30
        
        # Save button
        save_btn = pygame.Rect(10, y_offset, 110, 30)
        if save_btn.collidepoint(x, y):
            self.save_terrain_definition()
            return
        
        # Cancel button
        cancel_btn = pygame.Rect(130, y_offset, 110, 30)
        if cancel_btn.collidepoint(x, y):
            self.creating_terrain = False
            self.active_input_field = None
            self.input_text = ""
            print("Terrain creation cancelled")
    
    def handle_terrain_creator_input(self, event):
        """Handle text input for terrain creator"""
        if not self.creating_terrain or not self.active_input_field:
            return False
        
        if event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
            # Save current field and move to next
            self.terrain_form_data[self.active_input_field] = self.input_text
            
            # Move to next field
            fields = ["name", "color_r", "color_g", "color_b", "icon"]
            try:
                current_idx = fields.index(self.active_input_field)
                if current_idx < len(fields) - 1:
                    self.active_input_field = fields[current_idx + 1]
                    self.input_text = str(self.terrain_form_data.get(self.active_input_field, ""))
                else:
                    # Last field, save terrain
                    self.save_terrain_definition()
            except ValueError:
                pass
            return True
        
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
            return True
        
        elif event.key == pygame.K_ESCAPE:
            self.creating_terrain = False
            self.active_input_field = None
            self.input_text = ""
            return True
        
        elif event.unicode and event.unicode.isprintable():
            # Limit color inputs to 3 digits
            if self.active_input_field in ["color_r", "color_g", "color_b"]:
                if len(self.input_text) < 3 and event.unicode.isdigit():
                    self.input_text += event.unicode
            else:
                self.input_text += event.unicode
            return True
        
        return False
    
    def save_terrain_definition(self):
        """Save the terrain definition (create new or update existing)"""
        # Update form data with current input
        if self.active_input_field:
            self.terrain_form_data[self.active_input_field] = self.input_text
        
        terrain_name = self.terrain_form_data.get("name", "").strip()
        if not terrain_name:
            print("Error: Terrain name is required")
            return
        
        # Build terrain definition
        try:
            r = int(self.terrain_form_data.get("color_r", "100"))
            g = int(self.terrain_form_data.get("color_g", "200"))
            b = int(self.terrain_form_data.get("color_b", "100"))
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            terrain_def = {
                "name": terrain_name,
                "color": (r, g, b),
                "passability": int(self.terrain_form_data.get("passability", "0")),
                "icon": self.terrain_form_data.get("icon", "custom")
            }
        except ValueError as e:
            print(f"Error: Invalid terrain attribute values: {e}")
            return
        
        global TERRAIN_TYPES
        
        if self.editing_terrain_id is not None:
            # Update existing terrain
            terrain_id = self.editing_terrain_id
            TERRAIN_TYPES[terrain_id] = terrain_def
            action = "updated"
        else:
            # Create new terrain with next available ID
            terrain_id = max(TERRAIN_TYPES.keys()) + 1 if TERRAIN_TYPES else 0
            TERRAIN_TYPES[terrain_id] = terrain_def
            action = "created"
        
        # Save to file
        save_terrain_types(TERRAIN_TYPES)
        
        print(f"Terrain '{terrain_name}' {action} successfully!")
        print(f"  ID: {terrain_id}")
        print(f"  Color: RGB{terrain_def['color']}")
        print(f"  Passability: {PASSABILITY_LABELS.get(terrain_def['passability'], 'Unknown')}")
        
        # Select the terrain
        self.selected_terrain = terrain_id
        
        # Exit creator mode
        self.creating_terrain = False
        self.editing_terrain_id = None
        self.active_input_field = None
        self.input_text = ""
    
    def change_grid_size(self, dw, dh):
        """Change the grid dimensions"""
        new_width = max(5, min(50, self.map_width + dw))
        new_height = max(5, min(50, self.map_height + dh))
        
        # Create new map data
        new_map = [[0 for _ in range(new_width)] for _ in range(new_height)]
        
        # Copy existing data
        for y in range(min(self.map_height, new_height)):
            for x in range(min(self.map_width, new_width)):
                new_map[y][x] = self.map_data[y][x]
        
        self.map_width = new_width
        self.map_height = new_height
        self.map_data = new_map
        
        # Remove units outside new bounds
        self.units = [u for u in self.units if u["row"] < new_height and u["col"] < new_width]
    
    def new_scenario(self):
        """Create a new empty scenario"""
        self.map_data = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.units = []
        print("New scenario created")
    
    def save_scenario(self):
        """Save the current scenario to files"""
        # Create resources directories if they don't exist
        Path("resources/maps").mkdir(parents=True, exist_ok=True)
        
        # Save map file
        map_file = f"resources/maps/map_{self.scenario_number}.txt"
        with open(map_file, 'w') as f:
            f.write(f"{self.map_height} {self.map_width}\n")
            for row in self.map_data:
                f.write(" ".join(str(TERRAIN_TYPES[cell]["passability"]) for cell in row) + "\n")
        
        # Save units file
        units_file = f"resources/maps/units_{self.scenario_number}.json"
        
        # Organize units by team
        teams_data = {}
        for unit in self.units:
            team_id = unit["team"]
            if team_id not in teams_data:
                team_config = game_config.get_team_config(team_id)
                teams_data[team_id] = {
                    "id": team_id,
                    "name": team_config["name"] if team_config else f"Team {team_id}",
                    "description": team_config.get("description", "") if team_config else "",
                    "units": []
                }
            
            teams_data[team_id]["units"].append({
                "type": unit["type"],
                "row": unit["row"],
                "col": unit["col"]
            })
        
        units_data = {
            "scenario": self.scenario_number,
            "description": self.scenario_description,
            "teams": list(teams_data.values())
        }
        
        with open(units_file, 'w') as f:
            json.dump(units_data, f, indent=2)
        
        print(f"Scenario {self.scenario_number} saved:")
        print(f"  Map: {map_file}")
        print(f"  Units: {units_file}")
        print(f"  Grid: {self.map_width}x{self.map_height}")
        print(f"  Units placed: {len(self.units)}")
    
    def load_scenario(self):
        """Load a scenario from files (supports both old and new formats)"""
        map_file = f"resources/maps/map_{self.scenario_number}.txt"
        units_file = f"resources/maps/units_{self.scenario_number}.json"
        
        # Load map
        if Path(map_file).exists():
            with open(map_file, 'r') as f:
                lines = f.readlines()
                
                # Skip comment lines and empty lines
                data_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
                
                if not data_lines:
                    print(f"No map data found in {map_file}")
                    return
                
                # Detect format: new format has "height width" on first line, old format has comma-separated values
                first_line = data_lines[0]
                
                if ',' in first_line:
                    # Old format: comma-separated icon,passability pairs
                    self.map_data = []
                    for line in data_lines:
                        row_data = []
                        cells = line.split()
                        for cell in cells:
                            if ',' in cell:
                                icon_str, pass_str = cell.split(',')
                                passability = int(pass_str)
                            else:
                                # Fallback if no comma
                                passability = int(cell)
                            
                            # Find terrain with matching passability
                            terrain_id = 0
                            for tid, tinfo in TERRAIN_TYPES.items():
                                if tinfo["passability"] == passability:
                                    terrain_id = tid
                                    break
                            row_data.append(terrain_id)
                        self.map_data.append(row_data)
                    
                    # Infer dimensions from data
                    self.map_height = len(self.map_data)
                    self.map_width = len(self.map_data[0]) if self.map_data else 0
                    print(f"Loaded map from {map_file} (old format)")
                    
                else:
                    # New format: height width on first line, then space-separated passability values
                    height, width = map(int, first_line.split())
                    
                    self.map_height = height
                    self.map_width = width
                    self.map_data = []
                    
                    for i in range(1, min(height + 1, len(data_lines))):
                        row_data = list(map(int, data_lines[i].split()))
                        # Convert passability back to terrain type
                        terrain_row = []
                        for passability in row_data:
                            # Find first terrain with matching passability
                            terrain_id = 0
                            for tid, tinfo in TERRAIN_TYPES.items():
                                if tinfo["passability"] == passability:
                                    terrain_id = tid
                                    break
                            terrain_row.append(terrain_id)
                        self.map_data.append(terrain_row)
                    
                    print(f"Loaded map from {map_file} (new format)")
                
                print(f"  Grid: {self.map_width}x{self.map_height}")
        else:
            print(f"Map file not found: {map_file}")
        
        # Load units
        if Path(units_file).exists():
            with open(units_file, 'r') as f:
                units_data = json.load(f)
                self.scenario_description = units_data.get("description", "")
                
                self.units = []
                for team in units_data.get("teams", []):
                    team_id = team["id"]
                    for unit in team.get("units", []):
                        self.units.append({
                            "type": unit["type"],
                            "team": team_id,
                            "row": unit["row"],
                            "col": unit["col"]
                        })
            
            print(f"Loaded units from {units_file}")
            print(f"  Units loaded: {len(self.units)}")
        else:
            print(f"Units file not found: {units_file}")
    
    def update(self):
        """Update editor state"""
        pass
    
    def draw(self):
        """Draw the editor interface"""
        self.screen.fill(DARK_GRAY)
        
        # Draw panels
        self.draw_toolbar()
        self.draw_left_panel()
        self.draw_grid()
        self.draw_right_panel()
        self.draw_status_bar()
        
        pygame.display.flip()
    
    def draw_toolbar(self):
        """Draw the top toolbar"""
        pygame.draw.rect(self.screen, GRAY, (0, 0, EDITOR_WIDTH, TOOLBAR_HEIGHT))
        pygame.draw.line(self.screen, BLACK, (0, TOOLBAR_HEIGHT), (EDITOR_WIDTH, TOOLBAR_HEIGHT), 2)
        
        # Title
        title = self.large_font.render("Strategy Game Editor", True, WHITE)
        self.screen.blit(title, (10, 15))
        
        # Mode indicator
        mode_text = f"Mode: {self.mode.upper()}"
        mode_surf = self.font.render(mode_text, True, YELLOW)
        self.screen.blit(mode_surf, (EDITOR_WIDTH - 300, 20))
        
        # Scenario selector with < > buttons
        scenario_text = f"Scenario: {self.scenario_number}"
        scenario_surf = self.font.render(scenario_text, True, WHITE)
        self.screen.blit(scenario_surf, (415, 20))
        
        # Previous scenario button
        prev_btn = pygame.Rect(380, 15, 30, 30)
        pygame.draw.rect(self.screen, LIGHT_GRAY, prev_btn)
        pygame.draw.rect(self.screen, WHITE, prev_btn, 2)
        prev_text = self.font.render("<", True, BLACK)
        prev_text_rect = prev_text.get_rect(center=prev_btn.center)
        self.screen.blit(prev_text, prev_text_rect)
        
        # Next scenario button
        next_btn = pygame.Rect(560, 15, 30, 30)
        pygame.draw.rect(self.screen, LIGHT_GRAY, next_btn)
        pygame.draw.rect(self.screen, WHITE, next_btn, 2)
        next_text = self.font.render(">", True, BLACK)
        next_text_rect = next_text.get_rect(center=next_btn.center)
        self.screen.blit(next_text, next_text_rect)
        
        # Show if scenario exists
        map_file = Path(f"resources/maps/map_{self.scenario_number}.txt")
        if map_file.exists():
            exists_text = self.small_font.render("(exists)", True, YELLOW)
            self.screen.blit(exists_text, (600, 25))
        else:
            exists_text = self.small_font.render("(new)", True, GREEN)
            self.screen.blit(exists_text, (600, 25))
    
    def draw_left_panel(self):
        """Draw the left selection panel"""
        panel_rect = pygame.Rect(0, TOOLBAR_HEIGHT, PANEL_WIDTH, EDITOR_HEIGHT - TOOLBAR_HEIGHT)
        pygame.draw.rect(self.screen, LIGHT_GRAY, panel_rect)
        pygame.draw.line(self.screen, BLACK, (PANEL_WIDTH, TOOLBAR_HEIGHT), 
                        (PANEL_WIDTH, EDITOR_HEIGHT), 2)
        
        y_offset = TOOLBAR_HEIGHT + 10
        
        if self.mode == MODE_TERRAIN:
            if self.creating_terrain:
                # Show terrain creation form
                self.draw_terrain_creator(y_offset)
            else:
                # Terrain selection
                title = self.font.render("Terrain Types:", True, BLACK)
                self.screen.blit(title, (10, y_offset))
                y_offset += 30
                
                for terrain_id, terrain_info in TERRAIN_TYPES.items():
                    # Draw main button
                    btn_rect = pygame.Rect(10, y_offset, PANEL_WIDTH - 70, 35)
                    is_selected = (terrain_id == self.selected_terrain)
                    color = YELLOW if is_selected else WHITE
                    pygame.draw.rect(self.screen, color, btn_rect)
                    pygame.draw.rect(self.screen, BLACK, btn_rect, 2)
                    
                    # Draw terrain color sample
                    color_rect = pygame.Rect(15, y_offset + 5, 25, 25)
                    pygame.draw.rect(self.screen, terrain_info["color"], color_rect)
                    pygame.draw.rect(self.screen, BLACK, color_rect, 1)
                    
                    # Draw terrain name
                    name_surf = self.small_font.render(terrain_info["name"], True, BLACK)
                    self.screen.blit(name_surf, (45, y_offset + 4))
                    
                    # Draw passability label
                    passability = terrain_info["passability"]
                    pass_label = PASSABILITY_LABELS.get(passability, "Unknown")
                    pass_surf = self.small_font.render(f"({pass_label})", True, DARK_GRAY)
                    self.screen.blit(pass_surf, (45, y_offset + 20))
                    
                    # Edit button for each terrain
                    edit_btn = pygame.Rect(PANEL_WIDTH - 55, y_offset, 45, 35)
                    pygame.draw.rect(self.screen, LIGHT_GRAY, edit_btn)
                    pygame.draw.rect(self.screen, BLACK, edit_btn, 2)
                    edit_text = self.small_font.render("Edit", True, BLACK)
                    edit_text_rect = edit_text.get_rect(center=edit_btn.center)
                    self.screen.blit(edit_text, edit_text_rect)
                    
                    y_offset += 40
                
                # Create New Terrain button
                y_offset += 10
                create_btn = pygame.Rect(10, y_offset, PANEL_WIDTH - 20, 40)
                pygame.draw.rect(self.screen, GREEN, create_btn)
                pygame.draw.rect(self.screen, BLACK, create_btn, 2)
                create_text = self.small_font.render("+ Create New Terrain", True, BLACK)
                text_rect = create_text.get_rect(center=create_btn.center)
                self.screen.blit(create_text, text_rect)
        
        elif self.mode == MODE_UNITS:
            if self.creating_unit:
                # Show unit creation form
                self.draw_unit_creator(y_offset)
            else:
                # Unit type selection
                title = self.font.render("Unit Types:", True, BLACK)
                self.screen.blit(title, (10, y_offset))
                y_offset += 30
                
                for unit_type in UNIT_TYPES:
                    btn_rect = pygame.Rect(10, y_offset, PANEL_WIDTH - 70, 35)
                    is_selected = (unit_type == self.selected_unit)
                    color = YELLOW if is_selected else WHITE
                    pygame.draw.rect(self.screen, color, btn_rect)
                    pygame.draw.rect(self.screen, BLACK, btn_rect, 2)
                    
                    name_surf = self.small_font.render(unit_type.capitalize(), True, BLACK)
                    self.screen.blit(name_surf, (15, y_offset + 8))
                    
                    # Edit button for each unit
                    edit_btn = pygame.Rect(PANEL_WIDTH - 55, y_offset, 45, 35)
                    pygame.draw.rect(self.screen, LIGHT_GRAY, edit_btn)
                    pygame.draw.rect(self.screen, BLACK, edit_btn, 1)
                    edit_text = self.small_font.render("Edit", True, BLACK)
                    edit_rect = edit_text.get_rect(center=edit_btn.center)
                    self.screen.blit(edit_text, edit_rect)
                    
                    y_offset += 40
                
                # Create New Unit button
                y_offset += 10
                create_btn = pygame.Rect(10, y_offset, PANEL_WIDTH - 20, 40)
                pygame.draw.rect(self.screen, GREEN, create_btn)
                pygame.draw.rect(self.screen, BLACK, create_btn, 2)
                create_text = self.small_font.render("+ Create New Unit Type", True, BLACK)
                text_rect = create_text.get_rect(center=create_btn.center)
                self.screen.blit(create_text, text_rect)
                y_offset += 50
                
                # Team selection
                y_offset += 10
                team_title = self.font.render("Team:", True, BLACK)
                self.screen.blit(team_title, (10, y_offset))
                y_offset += 30
                
                for team in game_config.get_teams():
                    btn_rect = pygame.Rect(10, y_offset, PANEL_WIDTH - 20, 30)
                    is_selected = (team['id'] == self.selected_team)
                    color = YELLOW if is_selected else tuple(team['color'])
                    pygame.draw.rect(self.screen, color, btn_rect)
                    pygame.draw.rect(self.screen, BLACK, btn_rect, 2)
                    
                    name_surf = self.small_font.render(team['name'], True, BLACK)
                    self.screen.blit(name_surf, (15, y_offset + 6))
                    
                    y_offset += 35
    
    def draw_grid(self):
        """Draw the main editing grid"""
        # Grid background
        grid_rect = pygame.Rect(self.grid_x, self.grid_y, 
                               self.map_width * CELL_SIZE, self.map_height * CELL_SIZE)
        pygame.draw.rect(self.screen, WHITE, grid_rect)
        
        # Draw terrain
        for y in range(self.map_height):
            for x in range(self.map_width):
                terrain_id = self.map_data[y][x]
                terrain_info = TERRAIN_TYPES[terrain_id]
                
                cell_rect = pygame.Rect(
                    self.grid_x + x * CELL_SIZE,
                    self.grid_y + y * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                pygame.draw.rect(self.screen, terrain_info["color"], cell_rect)
                pygame.draw.rect(self.screen, DARK_GRAY, cell_rect, 1)
        
        # Draw units
        for unit in self.units:
            x = self.grid_x + unit["col"] * CELL_SIZE
            y = self.grid_y + unit["row"] * CELL_SIZE
            
            # Get team color
            team_config = game_config.get_team_config(unit["team"])
            team_color = tuple(team_config["color"]) if team_config else GRAY
            
            # Draw unit circle
            center_x = x + CELL_SIZE // 2
            center_y = y + CELL_SIZE // 2
            pygame.draw.circle(self.screen, team_color, (center_x, center_y), CELL_SIZE // 3)
            pygame.draw.circle(self.screen, BLACK, (center_x, center_y), CELL_SIZE // 3, 2)
            
            # Draw unit type letter
            letter = unit["type"][0].upper()
            text_surf = self.small_font.render(letter, True, BLACK)
            text_rect = text_surf.get_rect(center=(center_x, center_y))
            self.screen.blit(text_surf, text_rect)
        
        # Draw grid border
        pygame.draw.rect(self.screen, BLACK, grid_rect, 3)
    
    def draw_right_panel(self):
        """Draw the right info panel"""
        panel_rect = pygame.Rect(EDITOR_WIDTH - PANEL_WIDTH, TOOLBAR_HEIGHT, 
                                 PANEL_WIDTH, EDITOR_HEIGHT - TOOLBAR_HEIGHT)
        pygame.draw.rect(self.screen, LIGHT_GRAY, panel_rect)
        pygame.draw.line(self.screen, BLACK, (EDITOR_WIDTH - PANEL_WIDTH, TOOLBAR_HEIGHT),
                        (EDITOR_WIDTH - PANEL_WIDTH, EDITOR_HEIGHT), 2)
        
        y_offset = TOOLBAR_HEIGHT + 10
        
        # Instructions
        title = self.font.render("Controls:", True, BLACK)
        self.screen.blit(title, (EDITOR_WIDTH - PANEL_WIDTH + 10, y_offset))
        y_offset += 30
        
        controls = [
            "T - Terrain mode",
            "U - Units mode",
            "S - Save scenario",
            "L - Load scenario",
            "N - New scenario",
            "+/- - Grid size",
            "1-6 - Quick terrain",
            "Left Click - Place",
            "Right Click - Erase",
            "Q - Quit"
        ]
        
        for control in controls:
            text = self.small_font.render(control, True, BLACK)
            self.screen.blit(text, (EDITOR_WIDTH - PANEL_WIDTH + 10, y_offset))
            y_offset += 22
        
        # Statistics
        y_offset += 20
        stats_title = self.font.render("Statistics:", True, BLACK)
        self.screen.blit(stats_title, (EDITOR_WIDTH - PANEL_WIDTH + 10, y_offset))
        y_offset += 25
        
        stats = [
            f"Grid: {self.map_width}x{self.map_height}",
            f"Units: {len(self.units)}",
            f"Scenario: {self.scenario_number}"
        ]
        
        for stat in stats:
            text = self.small_font.render(stat, True, BLACK)
            self.screen.blit(text, (EDITOR_WIDTH - PANEL_WIDTH + 10, y_offset))
            y_offset += 22
    
    def draw_status_bar(self):
        """Draw the bottom status bar"""
        status_rect = pygame.Rect(0, EDITOR_HEIGHT - STATUS_HEIGHT, EDITOR_WIDTH, STATUS_HEIGHT)
        pygame.draw.rect(self.screen, GRAY, status_rect)
        pygame.draw.line(self.screen, BLACK, (0, EDITOR_HEIGHT - STATUS_HEIGHT),
                        (EDITOR_WIDTH, EDITOR_HEIGHT - STATUS_HEIGHT), 2)
        
        # Status text
        if self.mode == MODE_TERRAIN:
            terrain_info = TERRAIN_TYPES[self.selected_terrain]
            status_text = f"Selected: {terrain_info['name']} terrain"
        else:
            team_config = game_config.get_team_config(self.selected_team)
            team_name = team_config['name'] if team_config else f"Team {self.selected_team}"
            status_text = f"Selected: {self.selected_unit.capitalize()} - {team_name}"
        
        status_surf = self.font.render(status_text, True, WHITE)
        self.screen.blit(status_surf, (10, EDITOR_HEIGHT - STATUS_HEIGHT + 5))


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the editor"""
    editor = ScenarioEditor()
    editor.run()


if __name__ == "__main__":
    main()
