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

# Deck and wood details
DECK_LIGHT = (180, 140, 80)
DECK_MID = (140, 100, 50)
DECK_DARK = (100, 70, 30)

# Metal and cannon colors
METAL_LIGHT = (160, 160, 150)
METAL_MID = (120, 120, 110)
METAL_DARK = (80, 80, 70)
CANNON_DARK = (40, 40, 35)

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
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    
    cx, cy = size // 2, size // 2
    sail_color = team_color if team_color else SAIL_WHITE
    
    # HULL - proper ship shape from above
    # Bow (front - pointed)
    pygame.draw.circle(surface, HULL_SHADOW, (cx, cy - 14), 4)
    pygame.draw.rect(surface, HULL_SHADOW, (cx - 4, cy - 14, 8, 2))
    
    # Main hull body (wide in middle, tapered at ends)
    pygame.draw.rect(surface, HULL_MID, (cx - 7, cy - 12, 14, 20))
    pygame.draw.rect(surface, HULL_LIGHT, (cx - 6, cy - 12, 6, 20))  # Highlight left side
    
    # Stern (back - rounded)
    pygame.draw.circle(surface, HULL_SHADOW, (cx, cy + 9), 5)
    pygame.draw.rect(surface, HULL_SHADOW, (cx - 5, cy + 8, 10, 2))
    
    # DECK planking (visible from top)
    for y in range(cy - 10, cy + 8, 2):
        pygame.draw.line(surface, DECK_DARK, (cx - 5, y), (cx + 5, y), 1)
    
    # Railings
    pygame.draw.line(surface, HULL_DARK, (cx - 7, cy - 10), (cx - 7, cy + 7), 1)
    pygame.draw.line(surface, HULL_DARK, (cx + 7, cy - 10), (cx + 7, cy + 7), 1)
    
    # MAST
    draw_pixel_rect(surface, WOOD_DARK, (cx - 1, cy - 8, 2, 16))
    
    # Yardarm (horizontal spar)
    draw_pixel_rect(surface, DECK_MID, (cx - 10, cy - 4, 20, 2))
    
    # SAIL
    draw_pixel_rect(surface, sail_color, (cx - 9, cy - 2, 18, 10))
    draw_pixel_rect(surface, SAIL_SHADOW, (cx - 9, cy - 2, 2, 10))  # Left edge shadow
    draw_pixel_rect(surface, SAIL_SHADOW, (cx + 7, cy - 2, 2, 10))  # Right edge shadow
    
    # Rigging lines
    pygame.draw.line(surface, METAL_DARK, (cx - 10, cy - 4), (cx - 7, cy + 2), 1)
    pygame.draw.line(surface, METAL_DARK, (cx + 10, cy - 4), (cx + 7, cy + 2), 1)
    
    # CANNONS (3 per side)
    for i in range(3):
        y = cy - 6 + i * 5
        draw_pixel_rect(surface, CANNON_DARK, (cx - 7, y, 2, 2))
        draw_pixel_rect(surface, CANNON_DARK, (cx + 5, y, 2, 2))
    
    # Stern cabin
    draw_pixel_rect(surface, WOOD_DARK, (cx - 3, cy + 6, 6, 3))
    surface.set_at((cx - 1, cy + 7), (200, 200, 100))  # Window
    surface.set_at((cx + 1, cy + 7), (200, 200, 100))  # Window
    
    # Bowsprit
    pygame.draw.line(surface, WOOD_DARK, (cx, cy - 16), (cx, cy - 18), 2)
    
    # Wake
    draw_pixel_circle(surface, FOAM_WHITE, (cx - 4, cy + 11), 1)
    draw_pixel_circle(surface, FOAM_WHITE, (cx + 4, cy + 11), 1)
    
    return surface


def create_brigantine_sprite(size=SPRITE_SIZE, team_color=None):
    """Create Brigantine ship sprite (fast two-masted vessel)"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    cx, cy = size // 2, size // 2
    sail_color = team_color if team_color else SAIL_WHITE
    
    # HULL (longer, sleeker than sloop)
    pygame.draw.circle(surface, HULL_SHADOW, (cx, cy - 16), 4)
    pygame.draw.rect(surface, HULL_SHADOW, (cx - 4, cy - 16, 8, 2))
    pygame.draw.rect(surface, HULL_MID, (cx - 8, cy - 14, 16, 24))
    pygame.draw.rect(surface, HULL_LIGHT, (cx - 7, cy - 14, 7, 24))
    pygame.draw.circle(surface, HULL_SHADOW, (cx, cy + 11), 6)
    pygame.draw.rect(surface, HULL_SHADOW, (cx - 6, cy + 10, 12, 2))
    
    # DECK
    for y in range(cy - 12, cy + 10, 2):
        width = 7 - abs(y - cy) // 6
        pygame.draw.line(surface, DECK_DARK, (cx - width, y), (cx + width, y), 1)
    pygame.draw.line(surface, HULL_DARK, (cx - 8, cy - 12), (cx - 8, cy + 9), 1)
    pygame.draw.line(surface, HULL_DARK, (cx + 8, cy - 12), (cx + 8, cy + 9), 1)
    
    # TWO MASTS
    draw_pixel_rect(surface, WOOD_DARK, (cx - 4, cy - 12, 2, 18))  # Fore
    draw_pixel_rect(surface, WOOD_DARK, (cx + 3, cy - 8, 2, 14))   # Main
    
    # YARDARMS & SAILS
    draw_pixel_rect(surface, DECK_MID, (cx - 12, cy - 8, 16, 2))
    draw_pixel_rect(surface, DECK_MID, (cx + 1, cy - 4, 12, 2))
    draw_pixel_rect(surface, sail_color, (cx - 11, cy - 6, 14, 8))
    draw_pixel_rect(surface, SAIL_SHADOW, (cx - 11, cy - 6, 2, 8))
    draw_pixel_rect(surface, sail_color, (cx + 2, cy - 2, 10, 6))
    draw_pixel_rect(surface, SAIL_SHADOW, (cx + 2, cy - 2, 2, 6))
    
    # RIGGING
    pygame.draw.line(surface, METAL_DARK, (cx - 12, cy - 8), (cx - 8, cy), 1)
    pygame.draw.line(surface, METAL_DARK, (cx + 4, cy - 8), (cx + 8, cy), 1)
    pygame.draw.line(surface, METAL_DARK, (cx + 12, cy - 4), (cx + 8, cy + 2), 1)
    
    # CANNONS (4 per side)
    for i in range(4):
        y = cy - 8 + i * 5
        draw_pixel_rect(surface, CANNON_DARK, (cx - 8, y, 2, 2))
        draw_pixel_rect(surface, CANNON_DARK, (cx + 6, y, 2, 2))
    
    # DETAILS
    draw_pixel_rect(surface, WOOD_DARK, (cx - 4, cy + 8, 8, 3))
    for i in range(3):
        surface.set_at((cx - 3 + i * 3, cy + 9), (200, 200, 100))
    pygame.draw.line(surface, WOOD_DARK, (cx, cy - 18), (cx, cy - 21), 2)
    for i in range(3):
        draw_pixel_circle(surface, FOAM_WHITE, (cx - 5 + i * 5, cy + 13), 1)
    
    return surface

def create_ship_of_the_line_sprite(size=SPRITE_SIZE, team_color=None):
    """Create Ship of the Line sprite (massive three-masted warship)"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    cx, cy = size // 2, size // 2
    sail_color = team_color if team_color else SAIL_WHITE
    
    # HULL (very large and wide)
    pygame.draw.circle(surface, HULL_SHADOW, (cx, cy - 14), 5)
    pygame.draw.rect(surface, HULL_SHADOW, (cx - 5, cy - 14, 10, 2))
    pygame.draw.rect(surface, HULL_MID, (cx - 12, cy - 12, 24, 22))
    pygame.draw.rect(surface, HULL_LIGHT, (cx - 11, cy - 12, 11, 22))
    pygame.draw.rect(surface, (220, 200, 150), (cx - 11, cy - 4, 22, 3))  # Gun deck stripe
    pygame.draw.circle(surface, HULL_SHADOW, (cx, cy + 11), 8)
    pygame.draw.rect(surface, HULL_SHADOW, (cx - 8, cy + 10, 16, 2))
    
    # DECK
    for y in range(cy - 10, cy + 10, 2):
        width = 10 - abs(y - cy) // 5
        pygame.draw.line(surface, DECK_DARK, (cx - width, y), (cx + width, y), 1)
    pygame.draw.line(surface, HULL_DARK, (cx - 12, cy - 10), (cx - 12, cy + 9), 1)
    pygame.draw.line(surface, HULL_DARK, (cx + 12, cy - 10), (cx + 12, cy + 9), 1)
    
    # THREE MASTS
    draw_pixel_rect(surface, WOOD_DARK, (cx - 7, cy - 16, 2, 22))  # Fore
    draw_pixel_rect(surface, WOOD_DARK, (cx - 1, cy - 18, 2, 24))  # Main (tallest)
    draw_pixel_rect(surface, WOOD_DARK, (cx + 5, cy - 14, 2, 20))  # Mizzen
    
    # YARDARMS & SAILS (three large sails)
    draw_pixel_rect(surface, DECK_MID, (cx - 14, cy - 12, 14, 2))
    draw_pixel_rect(surface, DECK_MID, (cx - 8, cy - 14, 14, 2))
    draw_pixel_rect(surface, DECK_MID, (cx + 3, cy - 10, 10, 2))
    draw_pixel_rect(surface, sail_color, (cx - 13, cy - 10, 12, 10))
    draw_pixel_rect(surface, SAIL_SHADOW, (cx - 13, cy - 10, 2, 10))
    draw_pixel_rect(surface, sail_color, (cx - 7, cy - 12, 12, 12))
    draw_pixel_rect(surface, SAIL_SHADOW, (cx - 7, cy - 12, 2, 12))
    draw_pixel_rect(surface, sail_color, (cx + 4, cy - 8, 8, 8))
    draw_pixel_rect(surface, SAIL_SHADOW, (cx + 4, cy - 8, 2, 8))
    
    # RIGGING
    pygame.draw.line(surface, METAL_DARK, (cx - 14, cy - 12), (cx - 12, cy - 2), 1)
    pygame.draw.line(surface, METAL_DARK, (cx - 1, cy - 12), (cx + 12, cy - 2), 1)
    pygame.draw.line(surface, METAL_DARK, (cx + 12, cy - 10), (cx + 12, cy), 1)
    
    # TWO GUN DECKS (upper: 5/side, lower: 4/side)
    for i in range(5):
        y = cy - 8 + i * 4
        draw_pixel_rect(surface, CANNON_DARK, (cx - 12, y, 2, 2))
        draw_pixel_rect(surface, CANNON_DARK, (cx + 10, y, 2, 2))
    for i in range(4):
        y = cy - 6 + i * 4
        draw_pixel_rect(surface, CANNON_DARK, (cx - 10, y, 2, 2))
        draw_pixel_rect(surface, CANNON_DARK, (cx + 8, y, 2, 2))
    
    # STERN GALLERY & FIGUREHEAD
    draw_pixel_rect(surface, WOOD_LIGHT, (cx - 8, cy + 8, 16, 4))
    for i in range(5):
        surface.set_at((cx - 7 + i * 4, cy + 9), (200, 180, 100))
    pygame.draw.line(surface, WOOD_DARK, (cx, cy - 16), (cx, cy - 19), 3)
    draw_pixel_circle(surface, (200, 160, 80), (cx, cy - 20), 2)
    
    # WAKE
    for i in range(5):
        draw_pixel_circle(surface, FOAM_WHITE, (cx - 8 + i * 4, cy + 13), 2)
    
    return surface

def create_frigate_sprite(size=SPRITE_SIZE, team_color=None):
    """Create Frigate sprite (artillery vessel with visible mortars)"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    cx, cy = size // 2, size // 2
    sail_color = team_color if team_color else SAIL_WHITE
    
    # HULL (sturdy, reinforced)
    pygame.draw.circle(surface, HULL_SHADOW, (cx, cy - 15), 4)
    pygame.draw.rect(surface, HULL_SHADOW, (cx - 4, cy - 15, 8, 2))
    pygame.draw.rect(surface, HULL_MID, (cx - 10, cy - 13, 20, 22))
    pygame.draw.rect(surface, HULL_LIGHT, (cx - 9, cy - 13, 9, 22))
    pygame.draw.circle(surface, HULL_SHADOW, (cx, cy + 10), 7)
    pygame.draw.rect(surface, HULL_SHADOW, (cx - 7, cy + 9, 14, 2))
    
    # REINFORCEMENT BANDS (metal)
    pygame.draw.line(surface, METAL_MID, (cx - 9, cy - 6), (cx + 9, cy - 6), 2)
    pygame.draw.line(surface, METAL_MID, (cx - 9, cy + 2), (cx + 9, cy + 2), 2)
    
    # DECK
    for y in range(cy - 11, cy + 9, 2):
        width = 8 - abs(y - cy) // 5
        pygame.draw.line(surface, DECK_DARK, (cx - width, y), (cx + width, y), 1)
    
    # ARMORED MORTAR PLATFORM (center deck - key feature)
    draw_pixel_rect(surface, METAL_MID, (cx - 6, cy - 4, 12, 8))
    draw_pixel_rect(surface, (80, 80, 70), (cx - 5, cy - 3, 10, 6))
    
    # TWO MASTS
    draw_pixel_rect(surface, WOOD_DARK, (cx - 5, cy - 14, 2, 18))
    draw_pixel_rect(surface, WOOD_DARK, (cx + 4, cy - 12, 2, 16))
    
    # YARDARMS & SAILS
    draw_pixel_rect(surface, DECK_MID, (cx - 12, cy - 10, 14, 2))
    draw_pixel_rect(surface, DECK_MID, (cx + 2, cy - 8, 12, 2))
    draw_pixel_rect(surface, sail_color, (cx - 11, cy - 8, 12, 8))
    draw_pixel_rect(surface, SAIL_SHADOW, (cx - 11, cy - 8, 2, 8))
    draw_pixel_rect(surface, sail_color, (cx + 3, cy - 6, 10, 6))
    draw_pixel_rect(surface, SAIL_SHADOW, (cx + 3, cy - 6, 2, 6))
    
    # RIGGING
    pygame.draw.line(surface, METAL_DARK, (cx - 12, cy - 10), (cx - 10, cy - 2), 1)
    pygame.draw.line(surface, METAL_DARK, (cx + 1, cy - 10), (cx + 10, cy - 2), 1)
    pygame.draw.line(surface, METAL_DARK, (cx + 12, cy - 8), (cx + 10, cy), 1)
    
    # MORTAR CANNONS (prominent on deck - main feature!)
    draw_pixel_circle(surface, METAL_MID, (cx - 3, cy - 1), 3)
    draw_pixel_circle(surface, (60, 60, 60), (cx - 3, cy - 1), 2)
    draw_pixel_circle(surface, CANNON_DARK, (cx - 3, cy - 1), 1)
    draw_pixel_circle(surface, METAL_MID, (cx + 3, cy - 1), 3)
    draw_pixel_circle(surface, (60, 60, 60), (cx + 3, cy - 1), 2)
    draw_pixel_circle(surface, CANNON_DARK, (cx + 3, cy - 1), 1)
    
    # AMMUNITION STACKS
    for i in range(2):
        draw_pixel_circle(surface, (70, 70, 70), (cx - 6, cy + 2 + i * 2), 1)
        draw_pixel_circle(surface, (70, 70, 70), (cx + 6, cy + 2 + i * 2), 1)
    
    # SIDE CANNONS (3 per side)
    for i in range(3):
        y = cy - 8 + i * 6
        draw_pixel_rect(surface, CANNON_DARK, (cx - 10, y, 2, 2))
        draw_pixel_rect(surface, CANNON_DARK, (cx + 8, y, 2, 2))
    
    # STERN CABIN & BOW REINFORCEMENT
    draw_pixel_rect(surface, WOOD_DARK, (cx - 5, cy + 7, 10, 3))
    for i in range(3):
        surface.set_at((cx - 4 + i * 4, cy + 8), (200, 200, 100))
    pygame.draw.line(surface, METAL_MID, (cx - 2, cy - 15), (cx - 2, cy - 11), 2)
    pygame.draw.line(surface, METAL_MID, (cx + 2, cy - 15), (cx + 2, cy - 11), 2)
    
    # WAKE
    for i in range(4):
        draw_pixel_circle(surface, FOAM_WHITE, (cx - 6 + i * 4, cy + 12), 1)
    
    return surface

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
