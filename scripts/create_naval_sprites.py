"""
Create high-quality 8-bit naval warfare sprites

This script generates pixel-art style sprites for Caribbean Naval Warfare:
- 4 Ship types (Sloop, Brigantine, Ship of the Line, Frigate)
- Naval structures (Naval Fort, Shipyard, Coastal Battery)
- Projectiles (Cannonball, Mortar Shell)
- Terrain icons (Open Water, Reef, Islands, Beach, Deep Channel)
- Multiple animations and health states for ships

All sprites are 64x64 pixels with classic 8-bit pixel art aesthetic.
Ships face downward by default and support team coloring.
"""

import pygame
import os
import sys
from pathlib import Path


# Initialize Pygame
pygame.init()

# Sprite dimensions
SPRITE_SIZE = 64
PROJECTILE_SIZE = 32

# Color palettes for pixel art

# Water colors (for backgrounds and water terrain)
WATER_LIGHT = (100, 180, 230)
WATER_MID = (60, 140, 200)
WATER_DARK = (30, 100, 160)
WATER_DEEP = (20, 70, 120)

# Ship hull colors (wooden ships)
HULL_LIGHT = (200, 160, 100)
HULL_MID = (160, 120, 70)
HULL_DARK = (120, 80, 40)
HULL_SHADOW = (80, 50, 20)

# Sail colors (sails and rigging)
SAIL_WHITE = (240, 240, 230)
SAIL_LIGHT = (200, 200, 190)
SAIL_SHADOW = (150, 150, 140)
SAIL_DARK = (100, 100, 90)
SAIL_CREAM = (230, 220, 200)

# Deck and wood details
DECK_LIGHT = (180, 140, 80)
DECK_MID = (140, 100, 50)
DECK_DARK = (100, 70, 30)

# Metal and cannon colors
METAL_LIGHT = (160, 160, 150)
METAL_MID = (120, 120, 110)
METAL_DARK = (80, 80, 70)
CANNON_DARK = (40, 40, 35)
CANNON_BLACK = (20, 20, 20)

# Additional detailed ship colors
HULL_DARK_BROWN = (60, 40, 20)
HULL_MED_BROWN = (100, 70, 40)
HULL_LIGHT_BROWN = (140, 100, 60)
HULL_HIGHLIGHT = (180, 140, 90)
MAST_DARK = (50, 35, 20)
MAST_LIGHT = (90, 65, 40)
ROPE_BROWN = (40, 30, 20)
FLAG_RED = (200, 40, 40)
FLAG_SHADOW = (140, 30, 30)

# Island and terrain colors
SAND_LIGHT = (240, 220, 180)
SAND_MID = (210, 190, 150)
GRASS_LIGHT = (100, 180, 80)
GRASS_DARK = (60, 140, 40)
ROCK_LIGHT = (140, 130, 120)
ROCK_DARK = (80, 75, 70)
JUNGLE_DARK = (40, 100, 30)

# Structure colors
STONE_LIGHT = (180, 170, 160)
STONE_MID = (140, 130, 120)
STONE_DARK = (100, 95, 90)
WOOD_LIGHT = (160, 120, 70)
WOOD_DARK = (100, 70, 40)

# Effect colors
FOAM_WHITE = (255, 255, 255)
SHADOW = (0, 0, 0, 128)
TRANSPARENT = (0, 0, 0, 0)


def draw_pixel_circle(surface, color, center, radius):
    """Draw a filled circle with pixelated edges"""
    x0, y0 = center
    for x in range(int(x0 - radius), int(x0 + radius + 1)):
        for y in range(int(y0 - radius), int(y0 + radius + 1)):
            if (x - x0) ** 2 + (y - y0) ** 2 <= radius ** 2:
                if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
                    surface.set_at((x, y), color)


def draw_pixel_rect(surface, color, rect):
    """Draw a filled rectangle"""
    pygame.draw.rect(surface, color, rect)


def draw_ship_shadow(surface, x, y, width, height):
    """Draw a soft shadow under the ship"""
    shadow_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    shadow_surf.fill(TRANSPARENT)
    pygame.draw.ellipse(shadow_surf, SHADOW, (0, 0, width, height))
    surface.blit(shadow_surf, (x, y))


def create_sloop_sprite(size=SPRITE_SIZE, team_color=None):
    """
    Create Sloop ship sprite (small merchant vessel)
    Proper top-down view showing ship anatomy
    """
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    cx, cy = SPRITE_SIZE // 2, SPRITE_SIZE // 2 + 5
    
    # === HULL (side view, showing depth) ===
    # Main hull body - elongated ship shape
    hull_points = [
        (cx - 18, cy + 8),      # Stern bottom
        (cx - 18, cy + 2),      # Stern top
        (cx - 16, cy - 2),      # Stern deck
        (cx + 16, cy - 4),      # Bow deck (higher)
        (cx + 20, cy),          # Bow tip
        (cx + 18, cy + 6),      # Bow bottom
        (cx - 16, cy + 10)      # Stern bottom curve
    ]
    
    # Dark outline
    pygame.draw.polygon(surface, HULL_DARK_BROWN, hull_points, 0)
    
    # Hull shading layers
    hull_mid = [
        (cx - 16, cy + 7),
        (cx - 16, cy + 3),
        (cx - 14, cy - 1),
        (cx + 14, cy - 3),
        (cx + 18, cy + 1),
        (cx + 16, cy + 5),
        (cx - 14, cy + 9)
    ]
    pygame.draw.polygon(surface, HULL_MED_BROWN, hull_mid, 0)
    
    # Highlight on upper hull
    hull_light = [
        (cx - 14, cy + 4),
        (cx - 14, cy),
        (cx + 12, cy - 2),
        (cx + 16, cy + 2)
    ]
    pygame.draw.polygon(surface, HULL_LIGHT_BROWN, hull_light, 0)
    
    # Hull planking lines
    for i in range(5):
        y = cy + 2 + i * 2
        pygame.draw.line(surface, HULL_DARK_BROWN, (cx - 16, y), (cx + 14, y - 1), 1)
    
    # === DECK ===
    pygame.draw.rect(surface, DECK_DARK, (cx - 14, cy - 1, 28, 3))
    pygame.draw.rect(surface, DECK_LIGHT, (cx - 13, cy - 1, 26, 2))
    
    # Deck planks
    for i in range(7):
        x = cx - 12 + i * 4
        pygame.draw.line(surface, DECK_DARK, (x, cy - 1), (x, cy + 1), 1)
    
    # === MAST (tall and prominent) ===
    # Main mast
    pygame.draw.rect(surface, MAST_DARK, (cx - 2, cy - 28, 4, 28))
    pygame.draw.rect(surface, MAST_LIGHT, (cx - 1, cy - 28, 2, 28))
    
    # Yardarm (horizontal spar)
    pygame.draw.rect(surface, MAST_DARK, (cx - 14, cy - 22, 28, 3))
    pygame.draw.rect(surface, MAST_LIGHT, (cx - 14, cy - 22, 28, 2))
    
    # === SAIL (large and billowing) ===
    sail_color = team_color if team_color else SAIL_WHITE
    
    # Main sail shape (slightly curved)
    sail_points = [
        (cx - 13, cy - 20),
        (cx - 13, cy - 8),
        (cx - 11, cy - 6),
        (cx + 11, cy - 6),
        (cx + 13, cy - 8),
        (cx + 13, cy - 20)
    ]
    pygame.draw.polygon(surface, sail_color, sail_points, 0)
    
    # Sail shadow edge
    pygame.draw.line(surface, SAIL_SHADOW, (cx - 13, cy - 20), (cx - 13, cy - 8), 2)
    pygame.draw.line(surface, SAIL_SHADOW, (cx + 13, cy - 20), (cx + 13, cy - 8), 2)
    
    # Sail billowing lines (showing wind)
    for i in range(6):
        x = cx - 10 + i * 4
        pygame.draw.line(surface, SAIL_CREAM, (x, cy - 19), (x, cy - 7), 1)
    
    # Sail bottom edge
    pygame.draw.line(surface, SAIL_SHADOW, (cx - 11, cy - 6), (cx + 11, cy - 6), 2)
    
    # === RIGGING ===
    # Main lines
    pygame.draw.line(surface, ROPE_BROWN, (cx - 14, cy - 22), (cx - 16, cy), 1)
    pygame.draw.line(surface, ROPE_BROWN, (cx + 14, cy - 22), (cx + 16, cy - 2), 1)
    pygame.draw.line(surface, ROPE_BROWN, (cx - 2, cy - 28), (cx - 16, cy), 1)
    pygame.draw.line(surface, ROPE_BROWN, (cx + 2, cy - 28), (cx + 16, cy - 2), 1)
    
    # === DETAILS ===
    # Cannons (visible gun ports)
    cannon_positions = [cy + 1, cy + 4, cy + 7]
    for cy_pos in cannon_positions:
        # Port holes
        pygame.draw.rect(surface, CANNON_BLACK, (cx - 15, cy_pos, 3, 2))
        # Cannon barrel protruding
        pygame.draw.circle(surface, METAL_DARK, (cx - 16, cy_pos + 1), 1)
    
    # Stern cabin
    pygame.draw.rect(surface, HULL_DARK_BROWN, (cx - 18, cy - 1, 4, 5))
    pygame.draw.rect(surface, (100, 80, 50), (cx - 17, cy, 2, 2))  # Window
    
    # Bow detail
    pygame.draw.line(surface, HULL_HIGHLIGHT, (cx + 18, cy + 1), (cx + 20, cy - 1), 2)
    
    # Flag (pirate flag!)
    pygame.draw.rect(surface, MAST_DARK, (cx - 2, cy - 31, 2, 3))
    pygame.draw.rect(surface, FLAG_RED, (cx, cy - 30, 6, 4))
    
    # Wake
    for i in range(3):
        x = cx - 20 - i * 3
        pygame.draw.circle(surface, FOAM_WHITE, (x, cy + 9 + i), 2)
    
    return surface


def create_brigantine_sprite(size=SPRITE_SIZE, team_color=None):
    """Create Brigantine ship sprite (fast two-masted vessel)"""
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    cx, cy = SPRITE_SIZE // 2, SPRITE_SIZE // 2 + 5
    
    # === HULL (longer and sleeker) ===
    hull_points = [
        (cx - 22, cy + 8),
        (cx - 22, cy + 1),
        (cx - 19, cy - 3),
        (cx + 19, cy - 5),
        (cx + 23, cy - 1),
        (cx + 22, cy + 6),
        (cx - 20, cy + 10)
    ]
    pygame.draw.polygon(surface, HULL_DARK_BROWN, hull_points, 0)
    
    hull_mid = [
        (cx - 20, cy + 7),
        (cx - 20, cy + 2),
        (cx - 17, cy - 2),
        (cx + 17, cy - 4),
        (cx + 21, cy),
        (cx + 20, cy + 5),
        (cx - 18, cy + 9)
    ]
    pygame.draw.polygon(surface, HULL_MED_BROWN, hull_mid, 0)
    
    hull_light = [
        (cx - 18, cy + 3),
        (cx - 17, cy - 1),
        (cx + 15, cy - 3),
        (cx + 19, cy + 1)
    ]
    pygame.draw.polygon(surface, HULL_LIGHT_BROWN, hull_light, 0)
    
    # Hull details
    for i in range(6):
        y = cy + 1 + i * 2
        pygame.draw.line(surface, HULL_DARK_BROWN, (cx - 19, y), (cx + 17, y - 1), 1)
    
    # === DECK ===
    pygame.draw.rect(surface, DECK_DARK, (cx - 17, cy - 2, 34, 3))
    pygame.draw.rect(surface, DECK_LIGHT, (cx - 16, cy - 2, 32, 2))
    
    # === TWO MASTS ===
    # Fore mast
    pygame.draw.rect(surface, MAST_DARK, (cx - 8, cy - 30, 4, 28))
    pygame.draw.rect(surface, MAST_LIGHT, (cx - 7, cy - 30, 2, 28))
    
    # Main mast (taller)
    pygame.draw.rect(surface, MAST_DARK, (cx + 6, cy - 28, 4, 26))
    pygame.draw.rect(surface, MAST_LIGHT, (cx + 7, cy - 28, 2, 26))
    
    # === YARDARMS ===
    pygame.draw.rect(surface, MAST_DARK, (cx - 18, cy - 24, 20, 3))
    pygame.draw.rect(surface, MAST_DARK, (cx + 2, cy - 22, 16, 3))
    
    # === SAILS (two large sails) ===
    sail_color = team_color if team_color else SAIL_WHITE
    
    # Fore sail
    fore_sail = [
        (cx - 17, cy - 22),
        (cx - 17, cy - 10),
        (cx - 15, cy - 8),
        (cx + 1, cy - 8),
        (cx + 2, cy - 10),
        (cx + 2, cy - 22)
    ]
    pygame.draw.polygon(surface, sail_color, fore_sail, 0)
    pygame.draw.line(surface, SAIL_SHADOW, (cx - 17, cy - 22), (cx - 17, cy - 10), 2)
    pygame.draw.line(surface, SAIL_SHADOW, (cx + 2, cy - 22), (cx + 2, cy - 10), 2)
    
    # Main sail
    main_sail = [
        (cx + 3, cy - 20),
        (cx + 3, cy - 8),
        (cx + 5, cy - 6),
        (cx + 17, cy - 6),
        (cx + 18, cy - 8),
        (cx + 18, cy - 20)
    ]
    pygame.draw.polygon(surface, sail_color, main_sail, 0)
    pygame.draw.line(surface, SAIL_SHADOW, (cx + 3, cy - 20), (cx + 3, cy - 8), 2)
    pygame.draw.line(surface, SAIL_SHADOW, (cx + 18, cy - 20), (cx + 18, cy - 8), 2)
    
    # Sail details
    for i in range(8):
        x1 = cx - 15 + i * 2
        pygame.draw.line(surface, SAIL_CREAM, (x1, cy - 21), (x1, cy - 9), 1)
    for i in range(6):
        x2 = cx + 5 + i * 2
        pygame.draw.line(surface, SAIL_CREAM, (x2, cy - 19), (x2, cy - 7), 1)
    
    # === RIGGING ===
    pygame.draw.line(surface, ROPE_BROWN, (cx - 18, cy - 24), (cx - 20, cy - 2), 1)
    pygame.draw.line(surface, ROPE_BROWN, (cx + 2, cy - 24), (cx + 4, cy - 2), 1)
    pygame.draw.line(surface, ROPE_BROWN, (cx + 18, cy - 22), (cx + 20, cy - 4), 1)
    
    # === DETAILS ===
    # Cannons (more than sloop)
    cannon_positions = [cy, cy + 3, cy + 6]
    for cy_pos in cannon_positions:
        pygame.draw.rect(surface, CANNON_BLACK, (cx - 19, cy_pos, 3, 2))
        pygame.draw.circle(surface, METAL_DARK, (cx - 20, cy_pos + 1), 1)
        pygame.draw.rect(surface, CANNON_BLACK, (cx + 14, cy_pos, 3, 2))
        pygame.draw.circle(surface, METAL_DARK, (cx + 17, cy_pos + 1), 1)
    
    # Stern cabin
    pygame.draw.rect(surface, HULL_DARK_BROWN, (cx - 22, cy - 2, 5, 6))
    pygame.draw.rect(surface, (100, 80, 50), (cx - 21, cy - 1, 2, 2))
    pygame.draw.rect(surface, (100, 80, 50), (cx - 21, cy + 2, 2, 2))
    
    # Flags
    pygame.draw.rect(surface, FLAG_RED, (cx - 8, cy - 33, 6, 4))
    pygame.draw.rect(surface, FLAG_RED, (cx + 6, cy - 31, 6, 4))
    
    # Wake (larger)
    for i in range(4):
        x = cx - 24 - i * 3
        pygame.draw.circle(surface, FOAM_WHITE, (x, cy + 9 + i), 2)
    
    return surface


def create_ship_of_the_line_sprite(size=SPRITE_SIZE, team_color=None):
    """Create Ship of the Line sprite (massive three-masted warship)"""
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    cx, cy = SPRITE_SIZE // 2, SPRITE_SIZE // 2 + 5
    
    # === MASSIVE HULL ===
    hull_points = [
        (cx - 26, cy + 9),
        (cx - 26, cy),
        (cx - 22, cy - 4),
        (cx + 22, cy - 6),
        (cx + 26, cy - 2),
        (cx + 25, cy + 7),
        (cx - 24, cy + 11)
    ]
    pygame.draw.polygon(surface, HULL_DARK_BROWN, hull_points, 0)
    
    # Gun deck stripe (classic warship yellow/cream)
    pygame.draw.rect(surface, (220, 200, 150), (cx - 23, cy + 2, 45, 3))
    
    hull_mid = [
        (cx - 24, cy + 8),
        (cx - 24, cy + 1),
        (cx - 20, cy - 3),
        (cx + 20, cy - 5),
        (cx + 24, cy - 1),
        (cx + 23, cy + 6),
        (cx - 22, cy + 10)
    ]
    pygame.draw.polygon(surface, HULL_MED_BROWN, hull_mid, 0)
    
    hull_light = [
        (cx - 22, cy + 3),
        (cx - 20, cy - 2),
        (cx + 18, cy - 4),
        (cx + 22, cy)
    ]
    pygame.draw.polygon(surface, HULL_LIGHT_BROWN, hull_light, 0)
    
    # Hull planking
    for i in range(7):
        y = cy + i * 2
        pygame.draw.line(surface, HULL_DARK_BROWN, (cx - 23, y), (cx + 20, y - 1), 1)
    
    # === DECK ===
    pygame.draw.rect(surface, DECK_DARK, (cx - 20, cy - 3, 40, 4))
    pygame.draw.rect(surface, DECK_LIGHT, (cx - 19, cy - 3, 38, 3))
    
    # === THREE MASTS (fore, main, mizzen) ===
    # Fore mast
    pygame.draw.rect(surface, MAST_DARK, (cx - 12, cy - 32, 4, 29))
    pygame.draw.rect(surface, MAST_LIGHT, (cx - 11, cy - 32, 2, 29))
    
    # Main mast (tallest in center)
    pygame.draw.rect(surface, MAST_DARK, (cx - 1, cy - 35, 4, 32))
    pygame.draw.rect(surface, MAST_LIGHT, (cx, cy - 35, 2, 32))
    
    # Mizzen mast
    pygame.draw.rect(surface, MAST_DARK, (cx + 10, cy - 30, 4, 27))
    pygame.draw.rect(surface, MAST_LIGHT, (cx + 11, cy - 30, 2, 27))
    
    # === YARDARMS ===
    pygame.draw.rect(surface, MAST_DARK, (cx - 22, cy - 26, 20, 3))
    pygame.draw.rect(surface, MAST_DARK, (cx - 11, cy - 29, 22, 3))
    pygame.draw.rect(surface, MAST_DARK, (cx + 6, cy - 24, 16, 3))
    
    # === THREE LARGE SAILS ===
    sail_color = team_color if team_color else SAIL_WHITE
    
    # Fore sail
    fore_sail = [(cx - 21, cy - 24), (cx - 21, cy - 12), (cx - 19, cy - 10),
                 (cx - 3, cy - 10), (cx - 2, cy - 12), (cx - 2, cy - 24)]
    pygame.draw.polygon(surface, sail_color, fore_sail, 0)
    pygame.draw.line(surface, SAIL_SHADOW, (cx - 21, cy - 24), (cx - 21, cy - 12), 2)
    
    # Main sail (largest)
    main_sail = [(cx - 10, cy - 27), (cx - 10, cy - 13), (cx - 8, cy - 11),
                 (cx + 10, cy - 11), (cx + 11, cy - 13), (cx + 11, cy - 27)]
    pygame.draw.polygon(surface, sail_color, main_sail, 0)
    pygame.draw.line(surface, SAIL_SHADOW, (cx - 10, cy - 27), (cx - 10, cy - 13), 2)
    pygame.draw.line(surface, SAIL_SHADOW, (cx + 11, cy - 27), (cx + 11, cy - 13), 2)
    
    # Mizzen sail
    mizzen_sail = [(cx + 7, cy - 22), (cx + 7, cy - 10), (cx + 9, cy - 8),
                   (cx + 21, cy - 8), (cx + 22, cy - 10), (cx + 22, cy - 22)]
    pygame.draw.polygon(surface, sail_color, mizzen_sail, 0)
    pygame.draw.line(surface, SAIL_SHADOW, (cx + 22, cy - 22), (cx + 22, cy - 10), 2)
    
    # Sail details
    for i in range(10):
        x1 = cx - 19 + i * 2
        pygame.draw.line(surface, SAIL_CREAM, (x1, cy - 23), (x1, cy - 11), 1)
    for i in range(6):
        x2 = cx + 9 + i * 2
        pygame.draw.line(surface, SAIL_CREAM, (x2, cy - 21), (x2, cy - 9), 1)
    
    # === RIGGING (complex) ===
    pygame.draw.line(surface, ROPE_BROWN, (cx - 22, cy - 26), (cx - 24, cy - 3), 1)
    pygame.draw.line(surface, ROPE_BROWN, (cx - 2, cy - 26), (cx, cy - 3), 1)
    pygame.draw.line(surface, ROPE_BROWN, (cx + 11, cy - 29), (cx + 13, cy - 3), 1)
    pygame.draw.line(surface, ROPE_BROWN, (cx + 22, cy - 24), (cx + 24, cy - 5), 1)
    
    # === TWO GUN DECKS ===
    # Upper gun deck
    cannon_y_upper = [cy - 1, cy + 2, cy + 5, cy + 8]
    for cy_pos in cannon_y_upper:
        pygame.draw.rect(surface, CANNON_BLACK, (cx - 23, cy_pos, 3, 2))
        pygame.draw.circle(surface, METAL_DARK, (cx - 24, cy_pos + 1), 1)
        pygame.draw.rect(surface, CANNON_BLACK, (cx + 18, cy_pos, 3, 2))
        pygame.draw.circle(surface, METAL_DARK, (cx + 21, cy_pos + 1), 1)
    
    # Lower gun deck (inside hull, smaller)
    cannon_y_lower = [cy + 3, cy + 6, cy + 9]
    for cy_pos in cannon_y_lower:
        pygame.draw.rect(surface, CANNON_BLACK, (cx - 21, cy_pos, 2, 2))
        pygame.draw.rect(surface, CANNON_BLACK, (cx + 17, cy_pos, 2, 2))
    
    # === DETAILS ===
    # Ornate stern gallery
    pygame.draw.rect(surface, HULL_MED_BROWN, (cx - 26, cy - 3, 6, 8))
    pygame.draw.rect(surface, (80, 60, 40), (cx - 25, cy - 2, 4, 2))
    # Windows
    for i in range(3):
        pygame.draw.rect(surface, (100, 80, 50), (cx - 25, cy + i * 2, 2, 1))
    
    # Figurehead
    pygame.draw.line(surface, (200, 160, 80), (cx + 25, cy - 2), (cx + 28, cy - 4), 2)
    pygame.draw.circle(surface, (200, 160, 80), (cx + 28, cy - 5), 2)
    
    # Flags on all masts
    pygame.draw.rect(surface, FLAG_RED, (cx - 12, cy - 35, 7, 5))
    pygame.draw.rect(surface, FLAG_RED, (cx - 1, cy - 38, 7, 5))
    pygame.draw.rect(surface, FLAG_RED, (cx + 10, cy - 33, 7, 5))
    
    # Large wake
    for i in range(5):
        x = cx - 28 - i * 3
        pygame.draw.circle(surface, FOAM_WHITE, (x, cy + 10 + i), 3)
    
    return surface


def create_frigate_sprite(size=SPRITE_SIZE, team_color=None):
    """Create Frigate sprite (artillery vessel with visible mortars)"""
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    cx, cy = SPRITE_SIZE // 2, SPRITE_SIZE // 2 + 5
    
    # === REINFORCED HULL ===
    hull_points = [
        (cx - 24, cy + 8),
        (cx - 24, cy),
        (cx - 21, cy - 4),
        (cx + 21, cy - 6),
        (cx + 24, cy - 2),
        (cx + 23, cy + 6),
        (cx - 22, cy + 10)
    ]
    pygame.draw.polygon(surface, HULL_DARK_BROWN, hull_points, 0)
    
    hull_mid = [
        (cx - 22, cy + 7),
        (cx - 22, cy + 1),
        (cx - 19, cy - 3),
        (cx + 19, cy - 5),
        (cx + 22, cy - 1),
        (cx + 21, cy + 5),
        (cx - 20, cy + 9)
    ]
    pygame.draw.polygon(surface, HULL_MED_BROWN, hull_mid, 0)
    
    # Metal reinforcement bands (visible)
    pygame.draw.line(surface, METAL_DARK, (cx - 20, cy), (cx + 18, cy - 2), 3)
    pygame.draw.line(surface, METAL_LIGHT, (cx - 20, cy), (cx + 18, cy - 2), 1)
    pygame.draw.line(surface, METAL_DARK, (cx - 19, cy + 4), (cx + 17, cy + 2), 3)
    pygame.draw.line(surface, METAL_LIGHT, (cx - 19, cy + 4), (cx + 17, cy + 2), 1)
    
    # === DECK ===
    pygame.draw.rect(surface, DECK_DARK, (cx - 19, cy - 3, 38, 4))
    
    # ARMORED MORTAR PLATFORM (center - key feature!)
    pygame.draw.rect(surface, METAL_DARK, (cx - 10, cy - 2, 20, 8))
    pygame.draw.rect(surface, (80, 80, 70), (cx - 9, cy - 1, 18, 6))
    
    # Platform bracing (metal beams)
    for i in range(4):
        x = cx - 7 + i * 5
        pygame.draw.line(surface, METAL_DARK, (x, cy - 2), (x, cy + 5), 2)
    
    # === TWO MASTS ===
    pygame.draw.rect(surface, MAST_DARK, (cx - 10, cy - 30, 4, 27))
    pygame.draw.rect(surface, MAST_LIGHT, (cx - 9, cy - 30, 2, 27))
    pygame.draw.rect(surface, MAST_DARK, (cx + 8, cy - 28, 4, 25))
    pygame.draw.rect(surface, MAST_LIGHT, (cx + 9, cy - 28, 2, 25))
    
    # === YARDARMS ===
    pygame.draw.rect(surface, MAST_DARK, (cx - 20, cy - 24, 20, 3))
    pygame.draw.rect(surface, MAST_DARK, (cx + 4, cy - 22, 16, 3))
    
    # === SAILS ===
    sail_color = team_color if team_color else SAIL_WHITE
    
    fore_sail = [(cx - 19, cy - 22), (cx - 19, cy - 10), (cx - 17, cy - 8),
                 (cx - 1, cy - 8), (cx, cy - 10), (cx, cy - 22)]
    pygame.draw.polygon(surface, sail_color, fore_sail, 0)
    pygame.draw.line(surface, SAIL_SHADOW, (cx - 19, cy - 22), (cx - 19, cy - 10), 2)
    
    main_sail = [(cx + 5, cy - 20), (cx + 5, cy - 8), (cx + 7, cy - 6),
                 (cx + 19, cy - 6), (cx + 20, cy - 8), (cx + 20, cy - 20)]
    pygame.draw.polygon(surface, sail_color, main_sail, 0)
    pygame.draw.line(surface, SAIL_SHADOW, (cx + 20, cy - 20), (cx + 20, cy - 8), 2)
    
    # === MORTAR CANNONS (prominent!) ===
    # Left mortar
    pygame.draw.circle(surface, METAL_DARK, (cx - 5, cy + 1), 4)
    pygame.draw.circle(surface, (50, 50, 45), (cx - 5, cy + 1), 3)
    pygame.draw.circle(surface, CANNON_BLACK, (cx - 5, cy + 1), 2)
    # Barrel pointing up
    pygame.draw.rect(surface, METAL_DARK, (cx - 6, cy - 2, 2, 3))
    
    # Right mortar
    pygame.draw.circle(surface, METAL_DARK, (cx + 5, cy + 1), 4)
    pygame.draw.circle(surface, (50, 50, 45), (cx + 5, cy + 1), 3)
    pygame.draw.circle(surface, CANNON_BLACK, (cx + 5, cy + 1), 2)
    pygame.draw.rect(surface, METAL_DARK, (cx + 4, cy - 2, 2, 3))
    
    # Ammunition (cannonballs stacked)
    for i in range(3):
        pygame.draw.circle(surface, METAL_DARK, (cx - 8, cy + 3 + i), 1)
        pygame.draw.circle(surface, METAL_DARK, (cx + 8, cy + 3 + i), 1)
    
    # Powder keg
    pygame.draw.rect(surface, HULL_DARK_BROWN, (cx - 2, cy + 3, 4, 3))
    pygame.draw.circle(surface, METAL_DARK, (cx, cy + 4), 1)
    
    # === SIDE CANNONS ===
    cannon_positions = [cy - 1, cy + 5, cy + 8]
    for cy_pos in cannon_positions:
        pygame.draw.rect(surface, CANNON_BLACK, (cx - 21, cy_pos, 3, 2))
        pygame.draw.circle(surface, METAL_DARK, (cx - 22, cy_pos + 1), 1)
        pygame.draw.rect(surface, CANNON_BLACK, (cx + 16, cy_pos, 3, 2))
        pygame.draw.circle(surface, METAL_DARK, (cx + 19, cy_pos + 1), 1)
    
    # === DETAILS ===
    # Stern cabin
    pygame.draw.rect(surface, HULL_DARK_BROWN, (cx - 24, cy - 3, 5, 7))
    pygame.draw.rect(surface, (100, 80, 50), (cx - 23, cy - 2, 2, 2))
    pygame.draw.rect(surface, (100, 80, 50), (cx - 23, cy + 1, 2, 2))
    
    # Bow reinforcement (metal armor)
    pygame.draw.line(surface, METAL_DARK, (cx + 22, cy - 5), (cx + 24, cy - 3), 3)
    pygame.draw.line(surface, METAL_LIGHT, (cx + 22, cy - 5), (cx + 24, cy - 3), 1)
    
    # Flags
    pygame.draw.rect(surface, FLAG_RED, (cx - 10, cy - 33, 7, 5))
    pygame.draw.rect(surface, FLAG_RED, (cx + 8, cy - 31, 7, 5))
    
    # Wake
    for i in range(4):
        x = cx - 26 - i * 3
        pygame.draw.circle(surface, FOAM_WHITE, (x, cy + 9 + i), 2)
    
    return surface


# Generate all ship sprites
if __name__ == "__main__":
    print("Creating detailed 8-bit ship sprites...")
    
    output_dir = Path("resources/units_detailed")
    output_dir.mkdir(exist_ok=True)
    
    ships = {
        "sloop": create_sloop_sprite,
        "brigantine": create_brigantine_sprite,
        "ship_of_the_line": create_ship_of_the_line_sprite,
        "frigate": create_frigate_sprite
    }
    
    for name, func in ships.items():
        sprite = func()
        pygame.image.save(sprite, str(output_dir / f"{name}_detailed.png"))
        print(f"✅ Created detailed {name}")
    
    print(f"\n🎨 Detailed ship sprites saved to {output_dir}")
    print("These are MUCH more detailed and clearly show sailing ships!")


def create_damaged_version(original_surface):
    """Add damage effects to a ship sprite"""
    damaged = original_surface.copy()
    width, height = damaged.get_size()
    
    # Add dark spots (damage)
    for _ in range(8):
        x, y = pygame.math.Vector2(width * 0.3, height * 0.4) + pygame.math.Vector2(
            pygame.math.Vector2(width * 0.4, height * 0.4).elementwise() * pygame.math.Vector2(
                (hash(str(_)) % 100) / 100.0,
                (hash(str(_ * 2)) % 100) / 100.0
            )
        )
        draw_pixel_circle(damaged, HULL_SHADOW, (int(x), int(y)), 2)
    
    return damaged


def create_cannonball_sprite(size=PROJECTILE_SIZE):
    """Create cannonball projectile sprite"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    
    center = size // 2
    
    # Cannonball (dark iron sphere)
    draw_pixel_circle(surface, METAL_DARK, (center, center), 8)
    draw_pixel_circle(surface, CANNON_DARK, (center + 1, center + 1), 7)
    
    # Highlight
    draw_pixel_circle(surface, METAL_LIGHT, (center - 2, center - 2), 2)
    
    # Smoke trail
    for i in range(3):
        alpha = 100 - i * 30
        smoke_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        draw_pixel_circle(smoke_surf, (60, 60, 60, alpha), (center + 8 + i * 2, center), 3 - i)
        surface.blit(smoke_surf, (0, 0))
    
    return surface


def create_mortar_shell_sprite(size=PROJECTILE_SIZE):
    """Create mortar shell projectile sprite"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    
    center = size // 2
    
    # Mortar shell (explosive projectile)
    draw_pixel_circle(surface, METAL_MID, (center, center), 9)
    draw_pixel_circle(surface, METAL_DARK, (center + 1, center + 1), 8)
    
    # Fuse (sparking)
    draw_pixel_rect(surface, WOOD_DARK, (center - 1, center - 10, 2, 6))
    
    # Spark
    draw_pixel_circle(surface, (255, 200, 0), (center, center - 11), 2)
    draw_pixel_circle(surface, (255, 100, 0), (center, center - 12), 1)
    
    # Smoke trail (larger)
    for i in range(4):
        alpha = 120 - i * 25
        smoke_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        draw_pixel_circle(smoke_surf, (80, 80, 70, alpha), (center + 6 + i * 2, center + i), 4 - i)
        surface.blit(smoke_surf, (0, 0))
    
    return surface


def create_naval_fort_sprite(size=SPRITE_SIZE):
    """Create naval fort structure sprite"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    
    center_x, center_y = size // 2, size // 2
    
    # Foundation/base (stone)
    draw_pixel_rect(surface, STONE_DARK, (center_x - 20, center_y - 5, 40, 15))
    draw_pixel_rect(surface, STONE_MID, (center_x - 19, center_y - 4, 38, 13))
    
    # Main fort walls
    draw_pixel_rect(surface, STONE_MID, (center_x - 18, center_y - 20, 36, 15))
    draw_pixel_rect(surface, STONE_LIGHT, (center_x - 17, center_y - 19, 34, 13))
    
    # Battlements (top of walls)
    for i in range(7):
        draw_pixel_rect(surface, STONE_DARK, (center_x - 16 + i * 5, center_y - 22, 3, 3))
    
    # Tower on right
    draw_pixel_rect(surface, STONE_MID, (center_x + 12, center_y - 26, 8, 12))
    draw_pixel_rect(surface, STONE_LIGHT, (center_x + 13, center_y - 25, 6, 10))
    
    # Flag pole
    draw_pixel_rect(surface, WOOD_DARK, (center_x + 15, center_y - 32, 1, 6))
    
    # Flag (team colored)
    draw_pixel_rect(surface, (200, 50, 50), (center_x + 16, center_y - 32, 4, 3))
    
    # Cannons pointing out
    for i, offset in enumerate([-10, 0, 10]):
        pygame.draw.circle(surface, CANNON_DARK, (center_x + offset, center_y - 12), 2)
    
    # Stone texture
    for i in range(15):
        x = center_x - 15 + (i % 5) * 6
        y = center_y - 18 + (i // 5) * 5
        pygame.draw.line(surface, STONE_DARK, (x, y), (x + 5, y), 1)
    
    return surface


def create_shipyard_sprite(size=SPRITE_SIZE):
    """Create shipyard structure sprite"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    
    center_x, center_y = size // 2, size // 2
    
    # Dock/platform (wooden)
    draw_pixel_rect(surface, WOOD_DARK, (center_x - 22, center_y + 5, 44, 8))
    draw_pixel_rect(surface, DECK_MID, (center_x - 21, center_y + 6, 42, 6))
    
    # Wooden planks (horizontal lines)
    for i in range(4):
        pygame.draw.line(surface, WOOD_DARK, (center_x - 21, center_y + 7 + i * 2), 
                        (center_x + 21, center_y + 7 + i * 2), 1)
    
    # Building structure
    draw_pixel_rect(surface, WOOD_DARK, (center_x - 15, center_y - 15, 30, 20))
    draw_pixel_rect(surface, WOOD_LIGHT, (center_x - 14, center_y - 14, 28, 18))
    
    # Roof (peaked)
    roof_points = [
        (center_x - 16, center_y - 15),
        (center_x, center_y - 24),
        (center_x + 16, center_y - 15)
    ]
    pygame.draw.polygon(surface, HULL_DARK, roof_points)
    
    # Windows
    draw_pixel_rect(surface, (50, 50, 50), (center_x - 10, center_y - 10, 4, 6))
    draw_pixel_rect(surface, (50, 50, 50), (center_x + 6, center_y - 10, 4, 6))
    
    # Ship under construction (small hull)
    draw_pixel_rect(surface, HULL_MID, (center_x - 8, center_y, 16, 5))
    pygame.draw.line(surface, WOOD_DARK, (center_x - 5, center_y), (center_x - 5, center_y - 8), 1)
    
    # Support poles in water
    draw_pixel_rect(surface, WOOD_DARK, (center_x - 20, center_y + 5, 2, 8))
    draw_pixel_rect(surface, WOOD_DARK, (center_x + 18, center_y + 5, 2, 8))
    
    return surface


def create_coastal_battery_sprite(size=SPRITE_SIZE):
    """Create coastal battery structure sprite"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    
    center_x, center_y = size // 2, size // 2
    
    # Sandbag walls (protective barrier)
    for i in range(3):
        for j in range(4):
            # Individual sandbags
            x = center_x - 12 + j * 8
            y = center_y - 8 + i * 6
            
            # Sandbag (tan/brown rounded rectangle)
            bag_color = SAND_MID if (i + j) % 2 == 0 else SAND_LIGHT
            draw_pixel_rect(surface, bag_color, (x, y, 6, 4))
            pygame.draw.line(surface, SAND_LIGHT, (x, y), (x + 5, y), 1)  # Highlight
    
    # Cannon emplacement (central)
    # Base platform
    draw_pixel_rect(surface, WOOD_DARK, (center_x - 10, center_y + 2, 20, 6))
    
    # Cannon (large shore gun)
    # Barrel
    draw_pixel_rect(surface, METAL_DARK, (center_x - 8, center_y - 6, 16, 4))
    draw_pixel_rect(surface, CANNON_DARK, (center_x - 8, center_y - 5, 16, 2))
    
    # Barrel opening
    pygame.draw.circle(surface, (30, 30, 30), (center_x - 9, center_y - 4), 2)
    
    # Carriage (wooden gun mount)
    draw_pixel_rect(surface, WOOD_DARK, (center_x - 2, center_y - 3, 4, 5))
    
    # Wheels
    pygame.draw.circle(surface, METAL_MID, (center_x - 6, center_y + 3), 3)
    pygame.draw.circle(surface, METAL_MID, (center_x + 6, center_y + 3), 3)
    pygame.draw.circle(surface, METAL_DARK, (center_x - 6, center_y + 3), 2)
    pygame.draw.circle(surface, METAL_DARK, (center_x + 6, center_y + 3), 2)
    
    # Cannonballs stacked
    for i, offset in enumerate([4, 8]):
        pygame.draw.circle(surface, METAL_DARK, (center_x + 12, center_y + offset), 2)
    
    return surface


def create_terrain_icon(terrain_type, size=SPRITE_SIZE):
    """Create terrain icon sprites"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    
    if terrain_type == "open_water":
        # Open water - simple wave pattern
        surface.fill(WATER_MID)
        # Waves
        for i in range(0, size, 8):
            pygame.draw.line(surface, WATER_LIGHT, (i, size//3), (i + 4, size//3 - 2), 2)
            pygame.draw.line(surface, WATER_DARK, (i, size*2//3), (i + 4, size*2//3 + 2), 2)
        
    elif terrain_type == "reef":
        # Shallow reef - turquoise water with coral
        surface.fill((0, 140, 140))
        # Coral shapes
        for i in range(5):
            x, y = (i % 3) * 20 + 8, (i // 3) * 20 + 10
            pygame.draw.circle(surface, ROCK_LIGHT, (x, y), 4)
            pygame.draw.circle(surface, (200, 150, 100), (x + 2, y + 2), 2)
        
    elif terrain_type == "rocky_island":
        # Rocky island - gray rocks
        surface.fill(WATER_DARK)
        # Rock formation
        draw_pixel_rect(surface, ROCK_DARK, (size//4, size//4, size//2, size//2))
        draw_pixel_rect(surface, ROCK_LIGHT, (size//4 + 2, size//4 + 2, size//2 - 4, size//2 - 4))
        # Rock texture
        for i in range(10):
            x = size//4 + (i % 3) * 8
            y = size//4 + (i // 3) * 8
            pygame.draw.circle(surface, ROCK_DARK, (x, y), 2)
        
    elif terrain_type == "jungle_island":
        # Jungle island - green vegetation
        surface.fill(WATER_MID)
        # Island base (sand)
        draw_pixel_circle(surface, SAND_LIGHT, (size//2, size//2), size//3)
        # Trees/jungle
        for i, offset in enumerate([(-8, -8), (8, -8), (0, 8)]):
            x, y = size//2 + offset[0], size//2 + offset[1]
            pygame.draw.circle(surface, JUNGLE_DARK, (x, y), 6)
            pygame.draw.circle(surface, GRASS_LIGHT, (x - 1, y - 1), 5)
        
    elif terrain_type == "beach":
        # Sandy beach
        surface.fill(SAND_LIGHT)
        # Sand texture (dots)
        for i in range(30):
            x = (hash(str(i)) % size)
            y = (hash(str(i * 2)) % size)
            surface.set_at((x, y), SAND_MID)
        # Water edge
        pygame.draw.line(surface, WATER_LIGHT, (0, size - 10), (size, size - 10), 4)
        pygame.draw.line(surface, WATER_MID, (0, size - 6), (size, size - 6), 3)
        
    elif terrain_type == "deep_channel":
        # Deep channel - dark blue water
        surface.fill(WATER_DEEP)
        # Current lines
        for i in range(0, size, 16):
            pygame.draw.line(surface, WATER_DARK, (0, i), (size, i + 8), 2)
    
    return surface


def save_all_sprites():
    """Generate and save all game sprites"""
    print("Generating Caribbean Naval Warfare sprites...")
    
    # Create directories
    units_dir = Path("resources/units")
    structures_dir = Path("resources/structures")
    projectiles_dir = Path("resources/projectiles")
    icons_dir = Path("resources/icons")
    
    for directory in [units_dir, structures_dir, projectiles_dir, icons_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Ship types and their sprite functions
    ships = {
        "sloop": create_sloop_sprite,
        "brigantine": create_brigantine_sprite,
        "ship_of_the_line": create_ship_of_the_line_sprite,
        "frigate": create_frigate_sprite
    }
    
    # Generate ship sprites with animations
    for ship_name, ship_func in ships.items():
        print(f"Creating {ship_name} sprites...")
        
        # Create base sprite
        base_sprite = ship_func()
        
        # Generate for different health states and animations
        for health in [100, 50, 25]:
            # Choose sprite version
            if health == 100:
                sprite = base_sprite.copy()
            else:
                sprite = create_damaged_version(base_sprite)
            
            # Idle animation (3 frames - slight bobbing)
            for frame in range(3):
                idle_sprite = sprite.copy()
                # Slight vertical offset for bobbing
                offset_y = (frame - 1) * 1
                final = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
                final.blit(idle_sprite, (0, offset_y))
                
                filename = f"{ship_name}_idle_{health}_{frame}.png"
                pygame.image.save(final, str(units_dir / filename))
            
            # Move animation (4 frames - forward motion)
            for frame in range(4):
                move_sprite = sprite.copy()
                # Add wake effect
                if frame > 0:
                    wake_y = SPRITE_SIZE // 2 + 15 + frame * 3
                    for i in range(3):
                        pygame.draw.circle(move_sprite, FOAM_WHITE, 
                                         (SPRITE_SIZE // 2 - 8 + i * 8, wake_y), 2)
                
                filename = f"{ship_name}_move_{health}_{frame}.png"
                pygame.image.save(move_sprite, str(units_dir / filename))
            
            # Attack animation (3 frames - cannon fire)
            for frame in range(3):
                attack_sprite = sprite.copy()
                if frame == 1:
                    # Muzzle flash on frame 1
                    flash_positions = [(SPRITE_SIZE // 2 - 10, SPRITE_SIZE // 2),
                                      (SPRITE_SIZE // 2 + 10, SPRITE_SIZE // 2)]
                    for pos in flash_positions:
                        pygame.draw.circle(attack_sprite, (255, 200, 0), pos, 4)
                        pygame.draw.circle(attack_sprite, (255, 255, 0), pos, 2)
                
                filename = f"{ship_name}_attack_{health}_{frame}.png"
                pygame.image.save(attack_sprite, str(units_dir / filename))
        
        # Hurt animation (1 frame - no health variant)
        hurt_sprite = base_sprite.copy()
        # Flash red tint
        hurt_overlay = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
        hurt_overlay.fill((255, 0, 0, 100))
        hurt_sprite.blit(hurt_overlay, (0, 0))
        pygame.image.save(hurt_sprite, str(units_dir / f"{ship_name}_hurt_0.png"))
        
        # Death animation (4 frames - sinking)
        for frame in range(4):
            death_sprite = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
            # Ship sinking progressively
            offset_y = frame * 8
            opacity = 255 - frame * 60
            sinking = base_sprite.copy()
            sinking.set_alpha(opacity)
            death_sprite.blit(sinking, (0, offset_y))
            
            # Add bubbles
            for i in range(frame * 2):
                bubble_x = SPRITE_SIZE // 2 + (i - frame) * 5
                bubble_y = SPRITE_SIZE // 2 + frame * 5 - i * 3
                pygame.draw.circle(death_sprite, FOAM_WHITE, (bubble_x, bubble_y), 2)
            
            pygame.image.save(death_sprite, str(units_dir / f"{ship_name}_death_{frame}.png"))
    
    # Projectiles
    print("Creating projectile sprites...")
    cannonball = create_cannonball_sprite()
    pygame.image.save(cannonball, str(projectiles_dir / "cannonball.png"))
    
    mortar = create_mortar_shell_sprite()
    pygame.image.save(mortar, str(projectiles_dir / "mortar_shell.png"))
    
    # Structures
    print("Creating structure sprites...")
    naval_fort = create_naval_fort_sprite()
    pygame.image.save(naval_fort, str(structures_dir / "naval_fort.png"))
    
    shipyard = create_shipyard_sprite()
    pygame.image.save(shipyard, str(structures_dir / "shipyard.png"))
    
    coastal_battery = create_coastal_battery_sprite()
    pygame.image.save(coastal_battery, str(structures_dir / "coastal_battery.png"))
    
    # Terrain icons
    print("Creating terrain icons...")
    terrains = ["open_water", "reef", "rocky_island", "jungle_island", "beach", "deep_channel"]
    for terrain in terrains:
        icon = create_terrain_icon(terrain)
        pygame.image.save(icon, str(icons_dir / f"{terrain}.png"))
    
    print("✅ All sprites generated successfully!")
    print(f"   - {len(ships) * 46} ship sprites (4 ships × 46 sprites each)")
    print(f"   - 2 projectile sprites")
    print(f"   - 3 structure sprites")
    print(f"   - {len(terrains)} terrain icons")
    print(f"Total: {len(ships) * 46 + 2 + 3 + len(terrains)} files")


if __name__ == "__main__":
    save_all_sprites()
    print("\n🚢 Caribbean Naval Warfare sprites ready!")
