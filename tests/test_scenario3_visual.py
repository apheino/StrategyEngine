"""Visual test for scenario 3 large map"""
import pygame
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE
from scenario import Scenario

def test_scenario3_visual():
    """Run a quick visual test of scenario 3"""
    
    # Initialize Pygame
    pygame.init()
    
    # Setup display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Scenario 3 - Large Battle Map Test")
    clock = pygame.time.Clock()
    
    # Setup font
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    # Load scenario 3
    print("Loading Scenario 3...")
    scenario = Scenario(scenario_number=3, cell_size=32)
    scenario.grid.scale_to_screen_height(SCREEN_HEIGHT)
    
    print(f"Map size: {scenario.grid.grid_width}x{scenario.grid.grid_height}")
    print(f"Units: {len(scenario.units)}")
    print(f"Cell size: {scenario.grid.cell_size}")
    print(f"Zoom: {scenario.grid.zoom}")
    print("\nControls:")
    print("  - Left-click drag: Pan")
    print("  - Mouse wheel: Zoom")
    print("  - G: Toggle grid lines")
    print("  - ESC: Exit")
    print("\nLook for:")
    print("  - Brown swamp tiles (slow passable)")
    print("  - Gray mountain tiles (blocked)")
    print("  - Green grass and beige sand (normal)")
    
    running = True
    
    while running:
        dt = clock.tick(FPS) / 1000.0
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            # Pass events to grid for pan/zoom
            scenario.grid.handle_event(event)
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw scenario
        scenario.draw_map(screen)
        scenario.draw_units(screen)
        
        # Draw info
        info_lines = [
            f"Scenario 3: {scenario.grid.grid_width}x{scenario.grid.grid_height} map",
            f"Units: {len(scenario.units)} (Player: {len([u for u in scenario.units if u.is_player_unit()])}, Enemy: {len([u for u in scenario.units if u.is_enemy_unit()])})",
            f"Zoom: {scenario.grid.zoom:.2f}x",
            f"Pan/Zoom with mouse - ESC to exit",
        ]
        
        y_offset = 10
        for line in info_lines:
            text = small_font.render(line, True, WHITE)
            screen.blit(text, (10, y_offset))
            y_offset += 25
        
        # Draw legend
        legend_y = SCREEN_HEIGHT - 110
        legend_items = [
            ("Beige: Sand (passable)", (238, 214, 175)),
            ("Green: Grass (passable)", (34, 139, 34)),
            ("Brown: Swamp (slow)", (101, 67, 33)),
            ("Gray: Mountain (blocked)", (105, 105, 105)),
        ]
        
        for i, (text, color) in enumerate(legend_items):
            # Draw color box
            pygame.draw.rect(screen, color, (10, legend_y + i*25, 20, 20))
            pygame.draw.rect(screen, WHITE, (10, legend_y + i*25, 20, 20), 1)
            # Draw text
            label = small_font.render(text, True, WHITE)
            screen.blit(label, (35, legend_y + i*25 + 2))
        
        pygame.display.flip()
    
    pygame.quit()
    print("\n✓ Visual test completed")


if __name__ == "__main__":
    test_scenario3_visual()
