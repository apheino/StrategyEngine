"""
Create beautiful animated terrain tiles for Caribbean Naval Warfare

Generates:
- Animated water tiles (with wave effects)
- Detailed shore/beach tiles
- Beautiful island tiles (jungle, rocky)
- Reef tiles with coral details
- Deep channel water

All tiles are 32x32 pixels with rich 8-bit detail
"""

import pygame
import os
import math
from pathlib import Path

pygame.init()

TILE_SIZE = 32
TRANSPARENT = (0, 0, 0, 0)

# Water colors (animated gradients)
WATER_LIGHT_1 = (80, 160, 210)
WATER_LIGHT_2 = (90, 170, 220)
WATER_MID_1 = (50, 130, 180)
WATER_MID_2 = (60, 140, 190)
WATER_DARK_1 = (30, 100, 150)
WATER_DARK_2 = (40, 110, 160)
WATER_DEEP_1 = (20, 80, 130)
WATER_DEEP_2 = (25, 90, 140)
FOAM_WHITE = (255, 255, 255)
FOAM_LIGHT = (230, 240, 250)

# Beach/sand colors
SAND_LIGHT = (245, 225, 180)
SAND_MID = (220, 200, 160)
SAND_DARK = (195, 175, 140)
SAND_SHADOW = (170, 150, 120)

# Jungle colors
JUNGLE_DARK = (30, 90, 30)
JUNGLE_MID = (50, 120, 50)
JUNGLE_LIGHT = (70, 150, 70)
JUNGLE_BRIGHT = (90, 180, 90)
TREE_TRUNK = (80, 50, 30)
TREE_DARK = (60, 35, 20)

# Rock colors
ROCK_DARK = (70, 70, 65)
ROCK_MID = (100, 95, 90)
ROCK_LIGHT = (130, 125, 115)
ROCK_HIGHLIGHT = (160, 155, 145)

# Reef colors
REEF_CORAL_1 = (200, 100, 80)
REEF_CORAL_2 = (180, 120, 100)
REEF_ROCK = (90, 85, 80)
REEF_WATER = (60, 140, 160)


def create_water_tile_animated(frame=0, is_deep=False):
    """Create animated water tile with wave effects"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    # Select colors based on depth
    if is_deep:
        base_color = WATER_DEEP_1 if frame % 2 == 0 else WATER_DEEP_2
        mid_color = WATER_DARK_1 if frame % 2 == 0 else WATER_DARK_2
    else:
        base_color = WATER_MID_1 if frame % 2 == 0 else WATER_MID_2
        mid_color = WATER_LIGHT_1 if frame % 2 == 0 else WATER_LIGHT_2
    
    # Base water
    surface.fill(base_color)
    
    # Wave patterns (animated offset)
    offset = (frame * 2) % 16
    
    # Horizontal waves
    for y in range(0, TILE_SIZE, 8):
        wave_y = (y + offset) % TILE_SIZE
        # Light wave
        for x in range(0, TILE_SIZE, 4):
            wave_x = x + (wave_y // 4)
            if wave_x < TILE_SIZE:
                pygame.draw.line(surface, mid_color, 
                               (wave_x, wave_y), (min(wave_x + 2, TILE_SIZE - 1), wave_y), 1)
    
    # Diagonal waves (for variety)
    for i in range(-TILE_SIZE, TILE_SIZE, 6):
        wave_offset = (i + offset) % (TILE_SIZE * 2)
        x1 = wave_offset
        y1 = 0
        x2 = wave_offset + TILE_SIZE
        y2 = TILE_SIZE
        
        if 0 <= x1 < TILE_SIZE * 2:
            # Draw subtle diagonal highlight
            for j in range(TILE_SIZE):
                px = x1 + j - TILE_SIZE
                py = y1 + j
                if 0 <= px < TILE_SIZE and 0 <= py < TILE_SIZE:
                    current = surface.get_at((px, py))
                    # Lighten slightly
                    new_color = (min(current[0] + 10, 255), 
                               min(current[1] + 10, 255), 
                               min(current[2] + 10, 255))
                    surface.set_at((px, py), new_color)
    
    # Occasional foam (sparkles)
    if frame % 4 < 2:
        foam_positions = [(5, 8), (20, 15), (10, 25), (28, 5), (15, 18)]
        for fx, fy in foam_positions:
            if (fx + fy + frame) % 8 < 3:
                pygame.draw.circle(surface, FOAM_LIGHT, (fx, fy), 1)
    
    return surface


def create_beach_tile():
    """Create detailed beach/sand tile"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    # Base sand
    surface.fill(SAND_MID)
    
    # Sand texture with random grains
    for i in range(200):
        x = (i * 7) % TILE_SIZE
        y = (i * 13) % TILE_SIZE
        shade = [SAND_LIGHT, SAND_MID, SAND_DARK][i % 3]
        surface.set_at((x, y), shade)
    
    # Sand ripples (wind patterns)
    for y in range(4, TILE_SIZE, 6):
        for x in range(TILE_SIZE):
            if (x + y // 2) % 8 < 4:
                pygame.draw.line(surface, SAND_LIGHT, (x, y), (x, y), 1)
            elif (x + y // 2) % 8 >= 6:
                pygame.draw.line(surface, SAND_DARK, (x, y), (x, y), 1)
    
    # Some shells/pebbles
    shell_positions = [(6, 10), (22, 8), (15, 20), (28, 25), (10, 28)]
    for sx, sy in shell_positions:
        # Small pebble
        pygame.draw.circle(surface, SAND_SHADOW, (sx, sy), 2)
        pygame.draw.circle(surface, SAND_DARK, (sx - 1, sy - 1), 1)
    
    # Beach smoothing (gradient effect at edges)
    for x in range(TILE_SIZE):
        for y in range(3):
            current = surface.get_at((x, y))
            blend = (current[0], current[1], min(current[2] + 20, 255))
            surface.set_at((x, y), blend)
    
    return surface


def create_jungle_tile():
    """Create lush jungle island tile"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    # Base jungle floor
    surface.fill(JUNGLE_DARK)
    
    # Dense foliage texture
    for i in range(300):
        x = (i * 11) % TILE_SIZE
        y = (i * 17) % TILE_SIZE
        shade = [JUNGLE_DARK, JUNGLE_MID, JUNGLE_LIGHT][i % 3]
        surface.set_at((x, y), shade)
    
    # Palm tree trunks (visible in tile)
    tree_positions = [(8, 25), (24, 12), (18, 28)]
    for tx, ty in tree_positions:
        # Trunk
        pygame.draw.line(surface, TREE_TRUNK, (tx, ty), (tx + 1, ty - 8), 2)
        pygame.draw.line(surface, TREE_DARK, (tx, ty), (tx, ty - 8), 1)
        
        # Palm fronds (top)
        if ty - 8 >= 0:
            pygame.draw.line(surface, JUNGLE_LIGHT, (tx - 3, ty - 8), (tx + 4, ty - 8), 1)
            pygame.draw.line(surface, JUNGLE_BRIGHT, (tx - 2, ty - 9), (tx + 3, ty - 9), 1)
    
    # Tropical plants (bushes)
    bush_positions = [(5, 15), (26, 20), (12, 8), (20, 22)]
    for bx, by in bush_positions:
        # Dense bush cluster
        pygame.draw.circle(surface, JUNGLE_MID, (bx, by), 3)
        pygame.draw.circle(surface, JUNGLE_LIGHT, (bx - 1, by - 1), 2)
        pygame.draw.circle(surface, JUNGLE_BRIGHT, (bx, by - 1), 1)
    
    # Vines/hanging foliage
    for x in range(0, TILE_SIZE, 8):
        vine_x = x + 2
        pygame.draw.line(surface, JUNGLE_MID, (vine_x, 0), (vine_x, 10), 1)
        pygame.draw.line(surface, JUNGLE_LIGHT, (vine_x + 1, 0), (vine_x + 2, 8), 1)
    
    return surface


def create_rocky_island_tile():
    """Create rocky/mountainous island tile"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    # Base rock
    surface.fill(ROCK_DARK)
    
    # Rock texture (grainy)
    for i in range(250):
        x = (i * 13) % TILE_SIZE
        y = (i * 19) % TILE_SIZE
        shade = [ROCK_DARK, ROCK_MID, ROCK_LIGHT][i % 3]
        surface.set_at((x, y), shade)
    
    # Rock formations (angular shapes)
    rock_shapes = [
        [(5, 15), (8, 10), (12, 15), (8, 20)],  # Rock 1
        [(20, 8), (24, 5), (28, 10), (24, 12)],  # Rock 2
        [(10, 25), (15, 22), (18, 28), (12, 30)],  # Rock 3
    ]
    
    for shape in rock_shapes:
        # Dark base
        pygame.draw.polygon(surface, ROCK_DARK, shape)
        # Mid tone
        pygame.draw.polygon(surface, ROCK_MID, shape, 2)
        # Highlight edge
        if len(shape) > 2:
            pygame.draw.line(surface, ROCK_LIGHT, shape[0], shape[1], 1)
            pygame.draw.line(surface, ROCK_HIGHLIGHT, shape[1], shape[2], 1)
    
    # Cracks and crevices
    crack_lines = [
        [(2, 5), (8, 12), (10, 18)],
        [(25, 15), (20, 20), (18, 25)],
        [(15, 3), (18, 10), (20, 15)],
    ]
    
    for crack in crack_lines:
        for i in range(len(crack) - 1):
            pygame.draw.line(surface, ROCK_DARK, crack[i], crack[i + 1], 1)
    
    # Moss/lichen patches (small green spots)
    moss_positions = [(7, 18), (22, 9), (14, 28)]
    for mx, my in moss_positions:
        pygame.draw.circle(surface, (60, 100, 60), (mx, my), 2)
        pygame.draw.circle(surface, (70, 120, 70), (mx, my), 1)
    
    return surface


def create_reef_tile():
    """Create coral reef tile (shallow water with coral)"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    # Shallow water base
    surface.fill(REEF_WATER)
    
    # Water shimmer
    for y in range(0, TILE_SIZE, 4):
        for x in range(0, TILE_SIZE, 6):
            if (x + y) % 12 < 6:
                pygame.draw.line(surface, (70, 150, 170), (x, y), (x + 2, y), 1)
    
    # Coral formations
    coral_positions = [
        (8, 12, REEF_CORAL_1),
        (20, 8, REEF_CORAL_2),
        (15, 22, REEF_CORAL_1),
        (26, 18, REEF_CORAL_2),
        (10, 26, REEF_CORAL_1),
    ]
    
    for cx, cy, color in coral_positions:
        # Coral base (rock)
        pygame.draw.circle(surface, REEF_ROCK, (cx, cy), 3)
        # Coral growth (branching)
        pygame.draw.circle(surface, color, (cx, cy - 1), 2)
        pygame.draw.line(surface, color, (cx - 1, cy - 1), (cx - 2, cy - 3), 1)
        pygame.draw.line(surface, color, (cx + 1, cy - 1), (cx + 2, cy - 3), 1)
        pygame.draw.circle(surface, (min(color[0] + 20, 255), 
                                     min(color[1] + 20, 255), 
                                     min(color[2] + 20, 255)), 
                          (cx, cy - 2), 1)
    
    # Sand/rocks on bottom
    for i in range(20):
        x = (i * 11) % TILE_SIZE
        y = (i * 17) % TILE_SIZE
        pygame.draw.circle(surface, REEF_ROCK, (x, y), 1)
    
    # Seaweed
    seaweed_x_positions = [5, 16, 28]
    for sx in seaweed_x_positions:
        pygame.draw.line(surface, (40, 100, 40), (sx, 20), (sx + 1, 10), 1)
        pygame.draw.line(surface, (50, 120, 50), (sx + 1, 20), (sx, 10), 1)
    
    return surface


def save_terrain_tiles():
    """Generate and save all terrain tiles"""
    output_dir = Path("resources/icons")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🎨 Generating beautiful terrain tiles...")
    print()
    
    # Open water - 8 animated frames
    print("Creating animated water tiles...")
    for frame in range(8):
        tile = create_water_tile_animated(frame, is_deep=False)
        filename = f"open_water_frame_{frame}.png"
        pygame.image.save(tile, str(output_dir / filename))
    
    # Also save frame 0 as the default
    tile = create_water_tile_animated(0, is_deep=False)
    pygame.image.save(tile, str(output_dir / "open_water.png"))
    print(f"  ✓ Open water (8 animated frames)")
    
    # Deep channel - 8 animated frames (darker water)
    print("Creating deep channel tiles...")
    for frame in range(8):
        tile = create_water_tile_animated(frame, is_deep=True)
        filename = f"deep_channel_frame_{frame}.png"
        pygame.image.save(tile, str(output_dir / filename))
    
    tile = create_water_tile_animated(0, is_deep=True)
    pygame.image.save(tile, str(output_dir / "deep_channel.png"))
    print(f"  ✓ Deep channel (8 animated frames)")
    
    # Beach
    print("Creating beach tile...")
    tile = create_beach_tile()
    pygame.image.save(tile, str(output_dir / "beach.png"))
    print(f"  ✓ Beach tile")
    
    # Jungle island
    print("Creating jungle island tile...")
    tile = create_jungle_tile()
    pygame.image.save(tile, str(output_dir / "jungle_island.png"))
    print(f"  ✓ Jungle island tile")
    
    # Rocky island
    print("Creating rocky island tile...")
    tile = create_rocky_island_tile()
    pygame.image.save(tile, str(output_dir / "rocky_island.png"))
    print(f"  ✓ Rocky island tile")
    
    # Reef
    print("Creating reef tile...")
    tile = create_reef_tile()
    pygame.image.save(tile, str(output_dir / "reef.png"))
    print(f"  ✓ Reef tile")
    
    print()
    print("✅ All terrain tiles generated!")
    print(f"   Total: 22 files (16 animated water + 4 static terrain + 2 base)")
    print()
    print("Tiles created:")
    print("  🌊 Open water (animated waves)")
    print("  🌊 Deep channel (animated darker water)")
    print("  🏖️  Beach (detailed sand)")
    print("  🌴 Jungle island (palm trees & foliage)")
    print("  🗻 Rocky island (stone formations)")
    print("  🪸 Reef (coral & rocks)")


if __name__ == "__main__":
    save_terrain_tiles()
    pygame.quit()
