"""Script to create placeholder icons for the game"""
import pygame
import os

# Initialize Pygame
pygame.init()

# Icon size
ICON_SIZE = 64

# Colors
SAND = (238, 214, 175)  # Shoreline
GREEN = (34, 139, 34)   # Grassland

# Ensure resources/icons directory exists
os.makedirs("resources/icons", exist_ok=True)

def create_icon(filename, color):
    """Create a simple solid color icon"""
    surface = pygame.Surface((ICON_SIZE, ICON_SIZE))
    surface.fill(color)
    filepath = f"resources/icons/{filename}"
    pygame.image.save(surface, filepath)
    print(f"Created {filepath}")

# Create icons
create_icon("icon_1.png", SAND)
create_icon("icon_2.png", GREEN)

print("Icon creation complete!")
