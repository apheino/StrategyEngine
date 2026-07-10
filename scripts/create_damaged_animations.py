"""Create damaged/hurt animation frames for units"""
import pygame
import os

# Initialize pygame
pygame.init()

# Sprite dimensions
SPRITE_SIZE = 32

def create_hurt_frame(unit_type, base_color, damaged=False):
    """Create a hurt/damage reaction frame (flashing red)"""
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    
    # Draw unit shape with red tint overlay
    if unit_type == "soldier":
        # Body
        pygame.draw.rect(surface, (255, 100, 100), (10, 8, 12, 16))
        # Head
        pygame.draw.circle(surface, (255, 120, 120), (16, 8), 4)
        # Shield (darker red)
        pygame.draw.rect(surface, (200, 50, 50), (8, 12, 4, 8))
        # Sword
        pygame.draw.line(surface, (180, 180, 180), (22, 10), (28, 4), 2)
    
    elif unit_type == "archer":
        # Body
        pygame.draw.rect(surface, (255, 100, 100), (10, 8, 12, 16))
        # Head
        pygame.draw.circle(surface, (255, 120, 120), (16, 8), 4)
        # Bow
        pygame.draw.arc(surface, (200, 50, 50), (20, 6, 8, 12), 0, 3.14, 2)
        # Arrow
        pygame.draw.line(surface, (180, 100, 100), (24, 12), (30, 12), 1)
    
    elif unit_type == "knight":
        # Body (larger)
        pygame.draw.rect(surface, (255, 100, 100), (8, 6, 16, 20))
        # Head with helmet
        pygame.draw.circle(surface, (200, 50, 50), (16, 6), 5)
        # Shield (larger)
        pygame.draw.rect(surface, (180, 40, 40), (6, 10, 6, 12))
        # Sword
        pygame.draw.line(surface, (180, 180, 180), (24, 8), (30, 2), 3)
    
    return surface

def create_damaged_idle_frame(unit_type, base_color, health_percent):
    """Create idle frame for damaged unit (shows wounds/damage)"""
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    
    # Determine damage level colors (darker, more red tint as health decreases)
    if health_percent >= 50:
        # Lightly damaged (50-99%)
        body_color = (base_color[0], max(0, base_color[1] - 30), max(0, base_color[2] - 30))
        damage_marks = 1
    else:
        # Heavily damaged (1-49%)
        body_color = (base_color[0], max(0, base_color[1] - 60), max(0, base_color[2] - 60))
        damage_marks = 2
    
    if unit_type == "soldier":
        # Body
        pygame.draw.rect(surface, body_color, (10, 8, 12, 16))
        # Head
        pygame.draw.circle(surface, body_color, (16, 8), 4)
        # Shield (cracked)
        pygame.draw.rect(surface, (100, 100, 100), (8, 12, 4, 8))
        if damage_marks >= 1:
            pygame.draw.line(surface, (50, 50, 50), (8, 14), (12, 18), 1)  # Crack
        # Sword
        pygame.draw.line(surface, (120, 120, 120), (22, 10), (28, 4), 2)
        # Damage marks (red spots)
        if damage_marks >= 1:
            pygame.draw.circle(surface, (150, 0, 0), (14, 16), 1)
        if damage_marks >= 2:
            pygame.draw.circle(surface, (150, 0, 0), (18, 12), 1)
    
    elif unit_type == "archer":
        # Body
        pygame.draw.rect(surface, body_color, (10, 8, 12, 16))
        # Head
        pygame.draw.circle(surface, body_color, (16, 8), 4)
        # Bow (damaged)
        pygame.draw.arc(surface, (80, 50, 20), (20, 6, 8, 12), 0, 3.14, 2)
        # Arrow
        pygame.draw.line(surface, (100, 80, 40), (24, 12), (30, 12), 1)
        # Damage marks
        if damage_marks >= 1:
            pygame.draw.circle(surface, (150, 0, 0), (12, 14), 1)
        if damage_marks >= 2:
            pygame.draw.circle(surface, (150, 0, 0), (18, 18), 1)
    
    elif unit_type == "knight":
        # Body (larger)
        pygame.draw.rect(surface, body_color, (8, 6, 16, 20))
        # Head with helmet (damaged)
        pygame.draw.circle(surface, (max(0, body_color[0] - 30), max(0, body_color[1] - 30), max(0, body_color[2] - 30)), (16, 6), 5)
        # Shield (cracked)
        pygame.draw.rect(surface, (80, 80, 80), (6, 10, 6, 12))
        if damage_marks >= 1:
            pygame.draw.line(surface, (50, 50, 50), (6, 12), (12, 20), 1)
        # Sword
        pygame.draw.line(surface, (120, 120, 120), (24, 8), (30, 2), 3)
        # Damage marks
        if damage_marks >= 1:
            pygame.draw.circle(surface, (150, 0, 0), (12, 16), 1)
        if damage_marks >= 2:
            pygame.draw.circle(surface, (150, 0, 0), (20, 20), 1)
    
    return surface

# Create animations directory if needed
os.makedirs("resources/units", exist_ok=True)

print("Creating damaged/hurt animation frames...\n")

# Define unit types and colors
units = [
    ("soldier", (50, 50, 200)),    # Blue
    ("archer", (50, 150, 50)),     # Green
    ("knight", (150, 50, 50)),     # Red/brown
]

health_levels = [
    (100, "Normal"),
    (50, "Damaged 50%"),
    (25, "Critical 25%"),
]

for unit_type, base_color in units:
    print(f"Creating frames for {unit_type}:")
    
    # Create hurt/damage reaction animation (2 frames)
    for frame_idx in range(2):
        hurt_frame = create_hurt_frame(unit_type, base_color)
        filepath = f"resources/units/{unit_type}_hurt_{frame_idx}.png"
        pygame.image.save(hurt_frame, filepath)
        print(f"  ✓ Created hurt frame {frame_idx}")
    
    # Create damaged idle animations for different health levels
    for health_percent, desc in health_levels:
        if health_percent < 100:  # Only create damaged versions
            for frame_idx in range(2):  # 2 idle frames
                damaged_frame = create_damaged_idle_frame(unit_type, base_color, health_percent)
                filepath = f"resources/units/{unit_type}_idle_{health_percent}_{frame_idx}.png"
                pygame.image.save(damaged_frame, filepath)
            print(f"  ✓ Created idle_{health_percent} frames (2 frames) - {desc}")
    
    print()

print("✓ All damaged/hurt animations created in resources/units/")
print("\nNaming convention:")
print("  {unit}_hurt_{frame}.png - Damage reaction animation")
print("  {unit}_idle_{health%}_{frame}.png - Damaged idle animations")
print("  {unit}_idle_{frame}.png - Normal (100%) idle animation")

pygame.quit()
