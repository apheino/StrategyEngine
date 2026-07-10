"""Create placeholder icons for terrain types"""
import pygame
import os

# Initialize pygame
pygame.init()

# Icon dimensions
ICON_SIZE = 64

def create_icon(filename, color, label):
    """Create a simple colored icon without text label"""
    surface = pygame.Surface((ICON_SIZE, ICON_SIZE))
    surface.fill(color)
    
    # Add border
    pygame.draw.rect(surface, (50, 50, 50), (0, 0, ICON_SIZE, ICON_SIZE), 2)
    
    return surface

# Create icons directory if it doesn't exist
os.makedirs("resources/icons", exist_ok=True)

# Define icons
icons = [
    ("icon_1.png", (238, 214, 175), "Sand"),     # Beige/sand
    ("icon_2.png", (34, 139, 34), "Grass"),      # Green grass
    ("icon_3.png", (101, 67, 33), "Swamp"),      # Brown swamp
    ("icon_4.png", (105, 105, 105), "Mountain"), # Gray mountain
]

print("Creating terrain icons...\n")

for filename, color, label in icons:
    filepath = os.path.join("resources/icons", filename)
    icon = create_icon(filename, color, label)
    pygame.image.save(icon, filepath)
    print(f"✓ Created {filename} - {label} {color}")

print(f"\n✓ All icons created in resources/icons/")
print("\nIcon Legend:")
print("  icon_1.png - Sand/Shoreline (passable)")
print("  icon_2.png - Grassland (passable)")
print("  icon_3.png - Swamp/Rough (slow)")
print("  icon_4.png - Mountain/Water (blocked)")

pygame.quit()
