#!/usr/bin/env python3
"""Visual demo showing animated units"""
import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLUE
from unit import Unit

# Initialize Pygame
pygame.init()

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Unit Animation Demo")
clock = pygame.time.Clock()

# Setup font
font = pygame.font.Font(None, 24)

# Create test units
units = [
    Unit(unit_type="soldier", team=0, position=(0, 0)),
    Unit(unit_type="archer", team=1, position=(0, 1)),
    Unit(unit_type="knight", team=0, position=(0, 2))
]

# Set different animations for demo
units[0].set_animation("idle")
units[1].set_animation("move")
units[2].set_animation("attack")

# Demo state
running = True
animation_cycle_timer = 0
current_demo_index = 0
animation_names = ["idle", "move", "attack", "death"]

print("Unit Animation Demo")
print("Press SPACE to cycle through animations")
print("Press ESC to quit")
print()

while running:
    dt = clock.tick(FPS) / 1000.0
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Cycle to next animation
                current_demo_index = (current_demo_index + 1) % len(animation_names)
                anim_name = animation_names[current_demo_index]
                for unit in units:
                    unit.set_animation(anim_name)
                print(f"Switched to: {anim_name}")
    
    # Update all units
    for unit in units:
        unit.update(dt)
    
    # Draw
    screen.fill(BLUE)
    
    # Draw title
    title = font.render("Unit Animation Demo - Press SPACE to cycle animations, ESC to quit", True, (255, 255, 255))
    screen.blit(title, (20, 20))
    
    # Draw units in a row
    cell_size = 128
    start_x = 100
    start_y = 200
    
    for i, unit in enumerate(units):
        x = start_x + i * (cell_size + 50)
        y = start_y
        
        # Draw unit
        unit.draw(screen, x, y, cell_size)
        
        # Draw label
        label = font.render(f"{unit.unit_type}", True, (255, 255, 255))
        label_rect = label.get_rect(centerx=x + cell_size // 2, top=y + cell_size + 10)
        screen.blit(label, label_rect)
        
        # Draw animation name
        anim_label = font.render(f"{unit.current_animation}", True, (200, 200, 200))
        anim_rect = anim_label.get_rect(centerx=x + cell_size // 2, top=y + cell_size + 35)
        screen.blit(anim_label, anim_rect)
        
        # Draw frame info
        frame_info = font.render(f"Frame: {unit.animation_frame}", True, (150, 150, 150))
        frame_rect = frame_info.get_rect(centerx=x + cell_size // 2, top=y + cell_size + 60)
        screen.blit(frame_info, frame_rect)
    
    # Draw unit stats
    stats_y = 400
    stats_title = font.render("Unit Stats:", True, (255, 255, 255))
    screen.blit(stats_title, (20, stats_y))
    
    for i, unit in enumerate(units):
        stats_text = f"{unit.unit_type}: HP={unit.health}/{unit.max_health}, ATK={unit.attack_power}, DEF={unit.defense}, MOV={unit.max_mobility}, RNG={unit.attack_range}"
        stats = font.render(stats_text, True, (200, 200, 200))
        screen.blit(stats, (40, stats_y + 25 + i * 25))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
