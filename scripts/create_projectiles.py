"""Create projectile sprites for ranged attacks"""
import pygame
import os

# Initialize pygame
pygame.init()

# Projectile dimensions
PROJECTILE_SIZE = 16

def create_arrow():
    """Create an arrow projectile (for archers)"""
    surface = pygame.Surface((PROJECTILE_SIZE, PROJECTILE_SIZE), pygame.SRCALPHA)
    
    # Draw arrow shaft (brown)
    pygame.draw.line(surface, (139, 69, 19), (2, 8), (12, 8), 2)
    
    # Draw arrowhead (gray)
    pygame.draw.polygon(surface, (128, 128, 128), [
        (12, 8),
        (14, 6),
        (14, 10)
    ])
    
    # Draw fletching (red)
    pygame.draw.line(surface, (200, 0, 0), (2, 6), (2, 10), 2)
    
    return surface

def create_spear():
    """Create a spear/javelin projectile (alternative ranged weapon)"""
    surface = pygame.Surface((PROJECTILE_SIZE, PROJECTILE_SIZE), pygame.SRCALPHA)
    
    # Draw shaft (brown)
    pygame.draw.line(surface, (101, 67, 33), (2, 8), (11, 8), 2)
    
    # Draw spearhead (silver)
    pygame.draw.polygon(surface, (192, 192, 192), [
        (11, 8),
        (14, 5),
        (14, 11)
    ])
    
    return surface

def create_magic_bolt():
    """Create a magic bolt projectile (for future magic units)"""
    surface = pygame.Surface((PROJECTILE_SIZE, PROJECTILE_SIZE), pygame.SRCALPHA)
    
    # Draw glowing orb (blue)
    pygame.draw.circle(surface, (100, 150, 255), (8, 8), 5)
    pygame.draw.circle(surface, (150, 200, 255), (8, 8), 3)
    pygame.draw.circle(surface, (200, 230, 255), (8, 8), 1)
    
    return surface

# Create projectiles directory if it doesn't exist
os.makedirs("resources/projectiles", exist_ok=True)

print("Creating projectile sprites...\n")

# Create and save projectiles
projectiles = [
    ("arrow.png", create_arrow(), "Arrow projectile for archers"),
    ("spear.png", create_spear(), "Spear projectile for spearmen"),
    ("magic_bolt.png", create_magic_bolt(), "Magic bolt for future magic units"),
]

for filename, sprite, description in projectiles:
    filepath = os.path.join("resources/projectiles", filename)
    pygame.image.save(sprite, filepath)
    print(f"✓ Created {filename} - {description}")

print(f"\n✓ All projectiles created in resources/projectiles/")

pygame.quit()
