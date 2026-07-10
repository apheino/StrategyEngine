"""Visual test for health bars with different health levels"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from scenario import Scenario
import time


def test_health_bar_visual():
    """Run a visual test showing health bars at different levels"""
    pygame.init()
    
    # Create display
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Health Bar Visual Test")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Load scenario
    scenario = Scenario(scenario_number=1)
    
    # Damage some units to show different health bar colors
    unit_index = 0
    for unit in scenario.units:
        if unit_index == 0:
            unit.health = unit.max_health  # 100% - Green
        elif unit_index == 1:
            unit.health = int(unit.max_health * 0.8)  # 80% - Green
        elif unit_index == 2:
            unit.health = int(unit.max_health * 0.6)  # 60% - Green
        elif unit_index == 3:
            unit.health = int(unit.max_health * 0.5)  # 50% - Yellow
        elif unit_index == 4:
            unit.health = int(unit.max_health * 0.4)  # 40% - Yellow
        elif unit_index == 5:
            unit.health = int(unit.max_health * 0.3)  # 30% - Yellow
        elif unit_index == 6:
            unit.health = int(unit.max_health * 0.2)  # 20% - Red
        elif unit_index == 7:
            unit.health = int(unit.max_health * 0.1)  # 10% - Red
        elif unit_index == 8:
            unit.health = 1  # 1 HP - Red
        unit_index += 1
    
    print("Visual test running...")
    print("Health bar colors demonstrated:")
    print("  Green: >60% health")
    print("  Yellow: 30-60% health")
    print("  Red: <30% health")
    print("Press ESC to close the test window")
    
    running = True
    test_duration = 5.0  # Run for 5 seconds
    start_time = time.time()
    
    while running and (time.time() - start_time) < test_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Draw scenario
        scenario.draw_map(screen)
        scenario.draw_units(screen)
        
        # Draw instructions
        text = font.render("Health bars with different levels - ESC to exit", True, (255, 255, 255))
        screen.blit(text, (20, 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("✓ Visual test completed")


if __name__ == "__main__":
    test_health_bar_visual()
