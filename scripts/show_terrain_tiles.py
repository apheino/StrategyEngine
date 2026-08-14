"""
Create a visual reference sheet showing all terrain tiles
Useful for verifying the quality of generated terrain graphics
"""

import pygame
import os

pygame.init()

# Tile configuration
TILE_SIZE = 32
SCALE = 3  # Scale up for better visibility
SCALED_SIZE = TILE_SIZE * SCALE
PADDING = 10

# Terrain tiles to display
terrains = [
    ('open_water', 'Open Water (animated)'),
    ('deep_channel', 'Deep Channel (animated)'),
    ('beach', 'Beach'),
    ('jungle_island', 'Jungle Island'),
    ('rocky_island', 'Rocky Island'),
    ('reef', 'Reef'),
]

# Create display surface
screen_width = (SCALED_SIZE + PADDING) * 3
screen_height = (SCALED_SIZE + PADDING + 30) * 2 + 40  # +30 for labels
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Caribbean Naval Warfare - Terrain Tiles')

# Font
font = pygame.font.Font(None, 24)
title_font = pygame.font.Font(None, 32)

# Background
screen.fill((30, 30, 40))

# Title
title = title_font.render('Caribbean Naval Warfare - Terrain Tiles', True, (255, 255, 255))
screen.blit(title, (screen_width // 2 - title.get_width() // 2, 10))

# Load and display each terrain
y_offset = 50
x_offset = PADDING

for i, (terrain_name, display_name) in enumerate(terrains):
    # Calculate position (2 rows of 3)
    row = i // 3
    col = i % 3
    x = PADDING + col * (SCALED_SIZE + PADDING)
    y = y_offset + row * (SCALED_SIZE + PADDING + 30)
    
    # Try loading animated frames first
    icon_path = f"resources/icons/{terrain_name}_frame_0.png"
    if not os.path.exists(icon_path):
        # Fall back to static image
        icon_path = f"resources/icons/{terrain_name}.png"
    
    if os.path.exists(icon_path):
        # Load and scale tile
        tile = pygame.image.load(icon_path)
        scaled_tile = pygame.transform.scale(tile, (SCALED_SIZE, SCALED_SIZE))
        
        # Draw tile
        screen.blit(scaled_tile, (x, y))
        
        # Draw border
        pygame.draw.rect(screen, (100, 100, 120), 
                        (x - 1, y - 1, SCALED_SIZE + 2, SCALED_SIZE + 2), 2)
        
        # Draw label
        label = font.render(display_name, True, (220, 220, 240))
        screen.blit(label, (x + SCALED_SIZE // 2 - label.get_width() // 2, 
                           y + SCALED_SIZE + 5))

# Update display
pygame.display.flip()

# Save screenshot
pygame.image.save(screen, 'resources/terrain_reference.png')
print('✅ Terrain reference sheet created: resources/terrain_reference.png')
print('   Press any key in the window to close...')

# Wait for user to close
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            running = False
    
    clock.tick(30)

pygame.quit()
