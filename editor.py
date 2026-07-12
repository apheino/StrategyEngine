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

# Terrain types (matching grid.py)
TERRAIN_TYPES = {
    0: {"name": "Grass", "color": (34, 139, 34), "passability": 0},    # Easy
    1: {"name": "Water", "color": (0, 105, 148), "passability": 2},     # Blocked
    2: {"name": "Mountain", "color": (139, 90, 43), "passability": 2},  # Blocked
    3: {"name": "Forest", "color": (0, 100, 0), "passability": 1},      # Slow
    4: {"name": "Sand", "color": (238, 214, 175), "passability": 0},    # Easy
    5: {"name": "Road", "color": (169, 169, 169), "passability": 0},    # Easy
}

# Unit types
UNIT_TYPES = ["soldier", "archer", "knight", "catapult"]

# Editor modes
MODE_TERRAIN = "terrain"
MODE_UNITS = "units"

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
        self.selected_unit = "soldier"
        self.selected_team = 0
        
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
        elif key == pygame.K_u:
            self.mode = MODE_UNITS
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
        elif pygame.K_1 <= key <= pygame.K_6:
            terrain_id = key - pygame.K_1
            if terrain_id < len(TERRAIN_TYPES):
                self.selected_terrain = terrain_id
    
    def handle_mouse_click(self, button, pos):
        """Handle mouse clicks"""
        x, y = pos
        
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
    
    def handle_mouse_drag(self, pos):
        """Handle mouse dragging"""
        # Could implement camera pan here if needed
        pass
    
    def handle_panel_click(self, x, y):
        """Handle clicks in the left panel"""
        if self.mode == MODE_TERRAIN:
            # Terrain selection area
            start_y = TOOLBAR_HEIGHT + 40
            for i, (terrain_id, terrain_info) in enumerate(TERRAIN_TYPES.items()):
                btn_y = start_y + i * 40
                if btn_y <= y < btn_y + 35:
                    self.selected_terrain = terrain_id
                    break
        
        elif self.mode == MODE_UNITS:
            # Unit type selection
            start_y = TOOLBAR_HEIGHT + 40
            for i, unit_type in enumerate(UNIT_TYPES):
                btn_y = start_y + i * 40
                if btn_y <= y < btn_y + 35:
                    self.selected_unit = unit_type
                    break
            
            # Team selection
            team_y = start_y + len(UNIT_TYPES) * 40 + 20
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
        """Load a scenario from files"""
        map_file = f"resources/maps/map_{self.scenario_number}.txt"
        units_file = f"resources/maps/units_{self.scenario_number}.json"
        
        # Load map
        if Path(map_file).exists():
            with open(map_file, 'r') as f:
                lines = f.readlines()
                height, width = map(int, lines[0].strip().split())
                
                self.map_height = height
                self.map_width = width
                self.map_data = []
                
                for i in range(1, height + 1):
                    row_data = list(map(int, lines[i].strip().split()))
                    # Convert passability back to terrain type (simple mapping)
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
            
            print(f"Loaded map from {map_file}")
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
        
        # Scenario number
        scenario_text = f"Scenario: {self.scenario_number}"
        scenario_surf = self.font.render(scenario_text, True, WHITE)
        self.screen.blit(scenario_surf, (400, 20))
    
    def draw_left_panel(self):
        """Draw the left selection panel"""
        panel_rect = pygame.Rect(0, TOOLBAR_HEIGHT, PANEL_WIDTH, EDITOR_HEIGHT - TOOLBAR_HEIGHT)
        pygame.draw.rect(self.screen, LIGHT_GRAY, panel_rect)
        pygame.draw.line(self.screen, BLACK, (PANEL_WIDTH, TOOLBAR_HEIGHT), 
                        (PANEL_WIDTH, EDITOR_HEIGHT), 2)
        
        y_offset = TOOLBAR_HEIGHT + 10
        
        if self.mode == MODE_TERRAIN:
            # Terrain selection
            title = self.font.render("Terrain Types:", True, BLACK)
            self.screen.blit(title, (10, y_offset))
            y_offset += 30
            
            for terrain_id, terrain_info in TERRAIN_TYPES.items():
                # Draw button
                btn_rect = pygame.Rect(10, y_offset, PANEL_WIDTH - 20, 35)
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
                self.screen.blit(name_surf, (45, y_offset + 8))
                
                y_offset += 40
        
        elif self.mode == MODE_UNITS:
            # Unit type selection
            title = self.font.render("Unit Types:", True, BLACK)
            self.screen.blit(title, (10, y_offset))
            y_offset += 30
            
            for unit_type in UNIT_TYPES:
                btn_rect = pygame.Rect(10, y_offset, PANEL_WIDTH - 20, 35)
                is_selected = (unit_type == self.selected_unit)
                color = YELLOW if is_selected else WHITE
                pygame.draw.rect(self.screen, color, btn_rect)
                pygame.draw.rect(self.screen, BLACK, btn_rect, 2)
                
                name_surf = self.small_font.render(unit_type.capitalize(), True, BLACK)
                self.screen.blit(name_surf, (15, y_offset + 8))
                
                y_offset += 40
            
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
