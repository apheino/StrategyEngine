"""
Create detailed 8-bit pixel art ships with clear sailing vessel appearance
Much larger and more detailed than before
"""

import pygame
import os
from pathlib import Path

pygame.init()

SPRITE_SIZE = 64
TRANSPARENT = (0, 0, 0, 0)

# Enhanced color palette for detailed ships
HULL_DARK_BROWN = (60, 40, 20)
HULL_MED_BROWN = (100, 70, 40)
HULL_LIGHT_BROWN = (140, 100, 60)
HULL_HIGHLIGHT = (180, 140, 90)
DECK_DARK = (80, 60, 35)
DECK_LIGHT = (120, 90, 50)
SAIL_WHITE = (250, 245, 235)
SAIL_CREAM = (230, 220, 200)
SAIL_SHADOW = (180, 170, 160)
MAST_DARK = (50, 35, 20)
MAST_LIGHT = (90, 65, 40)
ROPE_BROWN = (40, 30, 20)
METAL_DARK = (60, 60, 55)
METAL_LIGHT = (100, 100, 90)
CANNON_BLACK = (20, 20, 20)
FLAG_RED = (200, 40, 40)
FLAG_SHADOW = (140, 30, 30)
WATER_DARK = (30, 80, 120)
WATER_MED = (50, 100, 150)
WATER_LIGHT = (70, 130, 180)
FOAM_WHITE = (255, 255, 255)


def draw_detailed_sloop(team_color=None):
    """Create a detailed sloop - small single-masted merchant vessel"""
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


def draw_detailed_brigantine(team_color=None):
    """Create a detailed brigantine - fast two-masted vessel"""
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


def draw_detailed_ship_of_line(team_color=None):
    """Create a detailed ship of the line - massive three-masted warship"""
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


def draw_detailed_frigate(team_color=None):
    """Create a detailed frigate - artillery vessel with mortars"""
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
        "sloop": draw_detailed_sloop,
        "brigantine": draw_detailed_brigantine,
        "ship_of_the_line": draw_detailed_ship_of_line,
        "frigate": draw_detailed_frigate
    }
    
    for name, func in ships.items():
        sprite = func()
        pygame.image.save(sprite, str(output_dir / f"{name}_detailed.png"))
        print(f"✅ Created detailed {name}")
    
    print(f"\n🎨 Detailed ship sprites saved to {output_dir}")
    print("These are MUCH more detailed and clearly show sailing ships!")
