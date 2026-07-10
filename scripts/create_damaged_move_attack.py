"""Create damaged move and attack animation frames for units"""
import pygame
import os

# Initialize pygame
pygame.init()

# Sprite dimensions
SPRITE_SIZE = 32

def create_damaged_move_frame(unit_type, base_color, health_percent, frame_variant):
    """Create move frame for damaged unit"""
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    
    # Determine damage level colors
    if health_percent >= 50:
        body_color = (base_color[0], max(0, base_color[1] - 30), max(0, base_color[2] - 30))
        damage_marks = 1
    else:
        body_color = (base_color[0], max(0, base_color[1] - 60), max(0, base_color[2] - 60))
        damage_marks = 2
    
    # Different positions for movement frames
    offsets = [(0, 0), (1, -1), (0, -2), (-1, -1)]
    offset_x, offset_y = offsets[frame_variant % 4]
    
    if unit_type == "soldier":
        # Body (moving)
        pygame.draw.rect(surface, body_color, (10 + offset_x, 8 + offset_y, 12, 16))
        # Head
        pygame.draw.circle(surface, body_color, (16 + offset_x, 8 + offset_y), 4)
        # Shield (cracked)
        pygame.draw.rect(surface, (100, 100, 100), (8 + offset_x, 12 + offset_y, 4, 8))
        if damage_marks >= 1:
            pygame.draw.line(surface, (50, 50, 50), (8, 14), (12, 18), 1)
        # Sword
        pygame.draw.line(surface, (120, 120, 120), (22 + offset_x, 10 + offset_y), (28 + offset_x, 4 + offset_y), 2)
        # Damage marks
        if damage_marks >= 1:
            pygame.draw.circle(surface, (150, 0, 0), (14 + offset_x, 16 + offset_y), 1)
        if damage_marks >= 2:
            pygame.draw.circle(surface, (150, 0, 0), (18 + offset_x, 12 + offset_y), 1)
    
    elif unit_type == "archer":
        # Body
        pygame.draw.rect(surface, body_color, (10 + offset_x, 8 + offset_y, 12, 16))
        # Head
        pygame.draw.circle(surface, body_color, (16 + offset_x, 8 + offset_y), 4)
        # Bow (damaged)
        pygame.draw.arc(surface, (80, 50, 20), (20 + offset_x, 6 + offset_y, 8, 12), 0, 3.14, 2)
        # Arrow
        pygame.draw.line(surface, (100, 80, 40), (24 + offset_x, 12 + offset_y), (30 + offset_x, 12 + offset_y), 1)
        # Damage marks
        if damage_marks >= 1:
            pygame.draw.circle(surface, (150, 0, 0), (12 + offset_x, 14 + offset_y), 1)
        if damage_marks >= 2:
            pygame.draw.circle(surface, (150, 0, 0), (18 + offset_x, 18 + offset_y), 1)
    
    elif unit_type == "knight":
        # Body (larger)
        pygame.draw.rect(surface, body_color, (8 + offset_x, 6 + offset_y, 16, 20))
        # Head with helmet
        pygame.draw.circle(surface, (max(0, body_color[0] - 30), max(0, body_color[1] - 30), max(0, body_color[2] - 30)), (16 + offset_x, 6 + offset_y), 5)
        # Shield (cracked)
        pygame.draw.rect(surface, (80, 80, 80), (6 + offset_x, 10 + offset_y, 6, 12))
        if damage_marks >= 1:
            pygame.draw.line(surface, (50, 50, 50), (6, 12), (12, 20), 1)
        # Sword
        pygame.draw.line(surface, (120, 120, 120), (24 + offset_x, 8 + offset_y), (30 + offset_x, 2 + offset_y), 3)
        # Damage marks
        if damage_marks >= 1:
            pygame.draw.circle(surface, (150, 0, 0), (12 + offset_x, 16 + offset_y), 1)
        if damage_marks >= 2:
            pygame.draw.circle(surface, (150, 0, 0), (20 + offset_x, 20 + offset_y), 1)
    
    return surface

def create_damaged_attack_frame(unit_type, base_color, health_percent, frame_variant):
    """Create attack frame for damaged unit"""
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    
    # Determine damage level colors
    if health_percent >= 50:
        body_color = (base_color[0], max(0, base_color[1] - 30), max(0, base_color[2] - 30))
        damage_marks = 1
    else:
        body_color = (base_color[0], max(0, base_color[1] - 60), max(0, base_color[2] - 60))
        damage_marks = 2
    
    # Attack animation positions (wind-up, strike, follow-through)
    if frame_variant == 0:  # Wind-up
        weapon_offset = (-2, 2)
    elif frame_variant == 1:  # Strike
        weapon_offset = (4, -4)
    else:  # Follow-through
        weapon_offset = (2, 0)
    
    if unit_type == "soldier":
        # Body
        pygame.draw.rect(surface, body_color, (10, 8, 12, 16))
        # Head
        pygame.draw.circle(surface, body_color, (16, 8), 4)
        # Shield
        pygame.draw.rect(surface, (100, 100, 100), (8, 12, 4, 8))
        if damage_marks >= 1:
            pygame.draw.line(surface, (50, 50, 50), (8, 14), (12, 18), 1)
        # Sword (attacking position)
        pygame.draw.line(surface, (120, 120, 120), (22 + weapon_offset[0], 10 + weapon_offset[1]), 
                        (28 + weapon_offset[0], 4 + weapon_offset[1]), 2)
        # Damage marks
        if damage_marks >= 1:
            pygame.draw.circle(surface, (150, 0, 0), (14, 16), 1)
        if damage_marks >= 2:
            pygame.draw.circle(surface, (150, 0, 0), (18, 12), 1)
    
    elif unit_type == "archer":
        # Body
        pygame.draw.rect(surface, body_color, (10, 8, 12, 16))
        # Head
        pygame.draw.circle(surface, body_color, (16, 8), 4)
        # Bow (pulled back for shooting)
        if frame_variant == 1:  # Drawing bow
            pygame.draw.arc(surface, (80, 50, 20), (18, 6, 10, 12), 0, 3.14, 2)
            pygame.draw.line(surface, (100, 80, 40), (20, 12), (16, 12), 1)  # Arrow drawn
        else:
            pygame.draw.arc(surface, (80, 50, 20), (20, 6, 8, 12), 0, 3.14, 2)
            pygame.draw.line(surface, (100, 80, 40), (24, 12), (30, 12), 1)
        # Damage marks
        if damage_marks >= 1:
            pygame.draw.circle(surface, (150, 0, 0), (12, 14), 1)
        if damage_marks >= 2:
            pygame.draw.circle(surface, (150, 0, 0), (18, 18), 1)
    
    elif unit_type == "knight":
        # Body
        pygame.draw.rect(surface, body_color, (8, 6, 16, 20))
        # Head with helmet
        pygame.draw.circle(surface, (max(0, body_color[0] - 30), max(0, body_color[1] - 30), max(0, body_color[2] - 30)), (16, 6), 5)
        # Shield
        pygame.draw.rect(surface, (80, 80, 80), (6, 10, 6, 12))
        if damage_marks >= 1:
            pygame.draw.line(surface, (50, 50, 50), (6, 12), (12, 20), 1)
        # Sword (attacking)
        pygame.draw.line(surface, (120, 120, 120), (24 + weapon_offset[0], 8 + weapon_offset[1]), 
                        (30 + weapon_offset[0], 2 + weapon_offset[1]), 3)
        # Damage marks
        if damage_marks >= 1:
            pygame.draw.circle(surface, (150, 0, 0), (12, 16), 1)
        if damage_marks >= 2:
            pygame.draw.circle(surface, (150, 0, 0), (20, 20), 1)
    
    return surface

# Create animations directory if needed
os.makedirs("resources/units", exist_ok=True)

print("Creating damaged move and attack animation frames...\n")

# Define unit types and colors
units = [
    ("soldier", (50, 50, 200)),
    ("archer", (50, 150, 50)),
    ("knight", (150, 50, 50)),
]

health_levels = [50, 25]

for unit_type, base_color in units:
    print(f"Creating damaged animations for {unit_type}:")
    
    for health_percent in health_levels:
        # Create damaged move animations (4 frames)
        for frame_idx in range(4):
            move_frame = create_damaged_move_frame(unit_type, base_color, health_percent, frame_idx)
            filepath = f"resources/units/{unit_type}_move_{health_percent}_{frame_idx}.png"
            pygame.image.save(move_frame, filepath)
        print(f"  ✓ Created move_{health_percent} frames (4 frames)")
        
        # Create damaged attack animations (3 frames)
        for frame_idx in range(3):
            attack_frame = create_damaged_attack_frame(unit_type, base_color, health_percent, frame_idx)
            filepath = f"resources/units/{unit_type}_attack_{health_percent}_{frame_idx}.png"
            pygame.image.save(attack_frame, filepath)
        print(f"  ✓ Created attack_{health_percent} frames (3 frames)")
    
    print()

print("✓ All damaged move and attack animations created!")
print("\nNaming convention:")
print("  {unit}_move_{health%}_{frame}.png - Damaged move animations")
print("  {unit}_attack_{health%}_{frame}.png - Damaged attack animations")

pygame.quit()
