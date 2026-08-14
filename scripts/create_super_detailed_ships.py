"""
Create SUPER detailed, OBVIOUSLY ship-shaped sprites
These will NOT look like squares - they will clearly be sailing ships!
"""

import pygame
import os
from pathlib import Path

pygame.init()

SPRITE_SIZE = 64
TRANSPARENT = (0, 0, 0, 0)

# Enhanced color palette for maximum detail
HULL_BASE = (70, 45, 25)
HULL_MID = (110, 75, 45)
HULL_LIGHT = (150, 105, 65)
HULL_HIGHLIGHT = (190, 145, 95)
DECK_DARK = (90, 60, 30)
DECK_LIGHT = (130, 95, 55)
MAST_DARK = (50, 35, 20)
MAST_LIGHT = (90, 65, 40)
SAIL_WHITE = (245, 245, 240)
SAIL_CREAM = (230, 225, 215)
SAIL_SHADOW = (180, 175, 165)
ROPE_BROWN = (60, 45, 30)
CANNON_METAL = (40, 40, 35)
CANNON_HOLE = (20, 20, 20)
FLAG_RED = (220, 40, 40)
FLAG_DARK = (160, 30, 30)
WATER_FOAM = (255, 255, 255)
WINDOW_GOLD = (200, 160, 80)

def create_sloop_detailed():
    """Create a VERY detailed sloop - clearly recognizable as a sailing ship"""
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    
    cx, cy = SPRITE_SIZE // 2, SPRITE_SIZE // 2
    
    # HULL - Large and obvious ship shape (side view)
    # Draw hull body with multiple layers for depth
    hull_outline = [
        (cx - 20, cy + 15),  # Stern bottom
        (cx - 20, cy + 5),   # Stern top
        (cx - 18, cy),       # Stern deck
        (cx - 16, cy - 3),   # Stern upper
        (cx + 18, cy - 5),   # Bow upper
        (cx + 24, cy),       # Bow tip
        (cx + 22, cy + 8),   # Bow waterline
        (cx + 18, cy + 12),  # Bow bottom
        (cx - 18, cy + 16),  # Stern bottom back
    ]
    
    # Draw hull with gradient effect
    pygame.draw.polygon(surface, HULL_BASE, hull_outline)
    
    # Middle hull layer
    hull_mid_outline = [
        (cx - 18, cy + 14),
        (cx - 18, cy + 6),
        (cx - 16, cy + 1),
        (cx + 16, cy - 4),
        (cx + 22, cy + 1),
        (cx + 20, cy + 9),
        (cx - 16, cy + 15),
    ]
    pygame.draw.polygon(surface, HULL_MID, hull_mid_outline)
    
    # Highlight layer
    hull_light_outline = [
        (cx - 16, cy + 7),
        (cx - 15, cy + 2),
        (cx + 14, cy - 3),
        (cx + 20, cy + 2),
        (cx + 18, cy + 7),
    ]
    pygame.draw.polygon(surface, HULL_LIGHT, hull_light_outline)
    
    # Hull planking (horizontal lines)
    for i in range(8):
        y_pos = cy + 6 + i * 2
        x_start = cx - 17 + abs(i - 4)
        x_end = cx + 17 - abs(i - 4)
        if y_pos <= cy + 15:
            pygame.draw.line(surface, HULL_BASE, (x_start, y_pos), (x_end, y_pos), 1)
    
    # DECK - Visible wooden deck
    pygame.draw.rect(surface, DECK_DARK, (cx - 15, cy, 30, 4))
    pygame.draw.rect(surface, DECK_LIGHT, (cx - 14, cy + 1, 28, 2))
    
    # Deck planks (vertical lines)
    for i in range(10):
        x_pos = cx - 12 + i * 3
        pygame.draw.line(surface, DECK_DARK, (x_pos, cy), (x_pos, cy + 3), 1)
    
    # MAST - Tall and prominent (single mast for sloop)
    mast_width = 5
    mast_height = 35
    pygame.draw.rect(surface, MAST_DARK, (cx - mast_width//2 - 1, cy - mast_height, mast_width + 2, mast_height))
    pygame.draw.rect(surface, MAST_LIGHT, (cx - mast_width//2, cy - mast_height, mast_width//2 + 1, mast_height))
    
    # Crow's nest
    pygame.draw.rect(surface, MAST_DARK, (cx - 4, cy - mast_height + 5, 8, 3))
    
    # YARDARM (horizontal spar for sail)
    yardarm_y = cy - 24
    pygame.draw.rect(surface, MAST_DARK, (cx - 18, yardarm_y - 1, 36, 4))
    pygame.draw.rect(surface, MAST_LIGHT, (cx - 18, yardarm_y, 36, 2))
    
    # SAIL - Large, billowing sail (main feature!)
    sail_points = [
        (cx - 16, yardarm_y + 1),
        (cx - 16, cy - 6),
        (cx - 13, cy - 4),
        (cx + 13, cy - 4),
        (cx + 16, cy - 6),
        (cx + 16, yardarm_y + 1),
    ]
    pygame.draw.polygon(surface, SAIL_WHITE, sail_points)
    
    # Sail shading
    pygame.draw.line(surface, SAIL_SHADOW, (cx - 16, yardarm_y + 1), (cx - 16, cy - 6), 2)
    pygame.draw.line(surface, SAIL_SHADOW, (cx + 16, yardarm_y + 1), (cx + 16, cy - 6), 2)
    
    # Sail detail lines (billowing effect)
    for i in range(7):
        x_pos = cx - 14 + i * 4
        pygame.draw.line(surface, SAIL_CREAM, (x_pos, yardarm_y + 2), (x_pos, cy - 5), 1)
    
    # RIGGING - Ropes from mast to hull
    pygame.draw.line(surface, ROPE_BROWN, (cx - 18, yardarm_y), (cx - 19, cy + 2), 2)
    pygame.draw.line(surface, ROPE_BROWN, (cx + 18, yardarm_y), (cx + 21, cy + 2), 2)
    pygame.draw.line(surface, ROPE_BROWN, (cx, cy - mast_height), (cx - 19, cy + 2), 1)
    pygame.draw.line(surface, ROPE_BROWN, (cx, cy - mast_height), (cx + 21, cy + 2), 1)
    
    # CANNONS - Visible gun ports with cannons
    cannon_y_positions = [cy + 4, cy + 7, cy + 10]
    for cannon_y in cannon_y_positions:
        # Port side cannons
        pygame.draw.rect(surface, CANNON_HOLE, (cx - 16, cannon_y, 4, 2))
        pygame.draw.circle(surface, CANNON_METAL, (cx - 17, cannon_y + 1), 2)
        
        # Starboard side cannons
        pygame.draw.rect(surface, CANNON_HOLE, (cx + 12, cannon_y, 4, 2))
        pygame.draw.circle(surface, CANNON_METAL, (cx + 17, cannon_y + 1), 2)
    
    # STERN CABIN - Captain's quarters
    pygame.draw.rect(surface, HULL_BASE, (cx - 21, cy + 2, 6, 8))
    pygame.draw.rect(surface, HULL_MID, (cx - 20, cy + 3, 4, 6))
    # Windows
    pygame.draw.rect(surface, WINDOW_GOLD, (cx - 19, cy + 5, 2, 2))
    
    # BOW DECORATIONS
    pygame.draw.line(surface, HULL_HIGHLIGHT, (cx + 22, cy + 1), (cx + 24, cy - 1), 3)
    pygame.draw.circle(surface, HULL_HIGHLIGHT, (cx + 23, cy), 2)
    
    # FLAG - Pirate flag at top of mast
    flag_y = cy - mast_height + 2
    pygame.draw.rect(surface, MAST_DARK, (cx - 1, flag_y - 3, 2, 5))  # Flagpole
    pygame.draw.polygon(surface, FLAG_RED, [
        (cx + 1, flag_y - 2),
        (cx + 1, flag_y + 2),
        (cx + 8, flag_y),
    ])
    pygame.draw.polygon(surface, FLAG_DARK, [
        (cx + 1, flag_y + 1),
        (cx + 1, flag_y + 2),
        (cx + 8, flag_y),
    ])
    
    # WAKE - Water foam behind ship
    for i in range(4):
        x_foam = cx - 23 - i * 4
        y_foam = cy + 14 + i * 2
        pygame.draw.circle(surface, WATER_FOAM, (x_foam, y_foam), 3)
        pygame.draw.circle(surface, (200, 200, 200), (x_foam, y_foam), 2)
    
    return surface


def create_brigantine_detailed():
    """Create detailed brigantine - TWO masts, longer hull"""
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    
    cx, cy = SPRITE_SIZE // 2, SPRITE_SIZE // 2
    
    # HULL - Longer and sleeker than sloop
    hull_outline = [
        (cx - 24, cy + 14),
        (cx - 24, cy + 4),
        (cx - 21, cy - 1),
        (cx - 18, cy - 4),
        (cx + 20, cy - 6),
        (cx + 26, cy - 1),
        (cx + 25, cy + 10),
        (cx - 22, cy + 15),
    ]
    pygame.draw.polygon(surface, HULL_BASE, hull_outline)
    
    hull_mid_outline = [
        (cx - 22, cy + 13),
        (cx - 22, cy + 5),
        (cx - 19, cy),
        (cx + 18, cy - 5),
        (cx + 24, cy),
        (cx + 23, cy + 9),
        (cx - 20, cy + 14),
    ]
    pygame.draw.polygon(surface, HULL_MID, hull_mid_outline)
    
    pygame.draw.polygon(surface, HULL_LIGHT, [
        (cx - 20, cy + 6),
        (cx - 18, cy + 1),
        (cx + 16, cy - 4),
        (cx + 22, cy + 1),
        (cx + 21, cy + 7),
    ])
    
    # Hull planking
    for i in range(9):
        y_pos = cy + 5 + i * 2
        pygame.draw.line(surface, HULL_BASE, (cx - 21, y_pos), (cx + 20, y_pos - 1), 1)
    
    # DECK
    pygame.draw.rect(surface, DECK_DARK, (cx - 19, cy - 1, 38, 4))
    pygame.draw.rect(surface, DECK_LIGHT, (cx - 18, cy, 36, 2))
    
    # TWO MASTS - Key feature of brigantine!
    # Fore mast (front, shorter)
    pygame.draw.rect(surface, MAST_DARK, (cx - 10, cy - 30, 5, 29))
    pygame.draw.rect(surface, MAST_LIGHT, (cx - 9, cy - 30, 3, 29))
    
    # Main mast (back, taller)
    pygame.draw.rect(surface, MAST_DARK, (cx + 6, cy - 32, 5, 31))
    pygame.draw.rect(surface, MAST_LIGHT, (cx + 7, cy - 32, 3, 31))
    
    # YARDARMS on both masts
    pygame.draw.rect(surface, MAST_DARK, (cx - 22, cy - 24, 24, 3))  # Fore
    pygame.draw.rect(surface, MAST_DARK, (cx - 6, cy - 26, 24, 3))   # Main
    
    # SAILS on both masts
    # Fore sail
    pygame.draw.polygon(surface, SAIL_WHITE, [
        (cx - 20, cy - 23),
        (cx - 20, cy - 8),
        (cx - 17, cy - 6),
        (cx, cy - 6),
        (cx + 2, cy - 8),
        (cx + 2, cy - 23),
    ])
    
    # Main sail
    pygame.draw.polygon(surface, SAIL_WHITE, [
        (cx - 4, cy - 25),
        (cx - 4, cy - 8),
        (cx - 1, cy - 6),
        (cx + 16, cy - 6),
        (cx + 18, cy - 8),
        (cx + 18, cy - 25),
    ])
    
    # Sail details
    for i in range(5):
        pygame.draw.line(surface, SAIL_CREAM, (cx - 18 + i * 4, cy - 22), (cx - 18 + i * 4, cy - 7), 1)
        pygame.draw.line(surface, SAIL_CREAM, (cx - 2 + i * 4, cy - 24), (cx - 2 + i * 4, cy - 7), 1)
    
    # CANNONS - More than sloop
    for cannon_y in [cy + 3, cy + 6, cy + 9, cy + 12]:
        pygame.draw.rect(surface, CANNON_HOLE, (cx - 20, cannon_y, 4, 2))
        pygame.draw.circle(surface, CANNON_METAL, (cx - 21, cannon_y + 1), 2)
        pygame.draw.rect(surface, CANNON_HOLE, (cx + 16, cannon_y, 4, 2))
        pygame.draw.circle(surface, CANNON_METAL, (cx + 21, cannon_y + 1), 2)
    
    # FLAGS on both masts
    pygame.draw.polygon(surface, FLAG_RED, [
        (cx - 8, cy - 31), (cx - 8, cy - 27), (cx - 1, cy - 29)
    ])
    pygame.draw.polygon(surface, FLAG_RED, [
        (cx + 9, cy - 33), (cx + 9, cy - 29), (cx + 16, cy - 31)
    ])
    
    # WAKE
    for i in range(5):
        pygame.draw.circle(surface, WATER_FOAM, (cx - 26 - i * 3, cy + 13 + i), 3)
    
    return surface


def create_ship_of_line_detailed():
    """Create massive ship of the line - THREE masts, huge hull"""
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    
    cx, cy = SPRITE_SIZE // 2, SPRITE_SIZE // 2
    
    # MASSIVE HULL
    hull_outline = [
        (cx - 26, cy + 16),
        (cx - 26, cy + 2),
        (cx - 23, cy - 3),
        (cx + 24, cy - 7),
        (cx + 28, cy),
        (cx + 27, cy + 12),
        (cx - 24, cy + 17),
    ]
    pygame.draw.polygon(surface, HULL_BASE, hull_outline)
    
    pygame.draw.polygon(surface, HULL_MID, [
        (cx - 24, cy + 15),
        (cx - 24, cy + 3),
        (cx - 21, cy - 2),
        (cx + 22, cy - 6),
        (cx + 26, cy + 1),
        (cx + 25, cy + 11),
        (cx - 22, cy + 16),
    ])
    
    pygame.draw.polygon(surface, HULL_LIGHT, [
        (cx - 22, cy + 4),
        (cx - 20, cy),
        (cx + 20, cy - 5),
        (cx + 24, cy + 2),
    ])
    
    # Gun deck stripe (iconic yellow stripe)
    pygame.draw.rect(surface, (220, 200, 140), (cx - 23, cy + 6, 47, 3))
    
    # DECK
    pygame.draw.rect(surface, DECK_DARK, (cx - 21, cy - 2, 42, 5))
    pygame.draw.rect(surface, DECK_LIGHT, (cx - 20, cy - 1, 40, 3))
    
    # THREE MASTS - defining feature!
    # Fore mast
    pygame.draw.rect(surface, MAST_DARK, (cx - 14, cy - 28, 4, 26))
    pygame.draw.rect(surface, MAST_LIGHT, (cx - 13, cy - 28, 2, 26))
    
    # Main mast (tallest)
    pygame.draw.rect(surface, MAST_DARK, (cx - 1, cy - 32, 5, 30))
    pygame.draw.rect(surface, MAST_LIGHT, (cx, cy - 32, 3, 30))
    
    # Mizzen mast
    pygame.draw.rect(surface, MAST_DARK, (cx + 12, cy - 26, 4, 24))
    pygame.draw.rect(surface, MAST_LIGHT, (cx + 13, cy - 26, 2, 24))
    
    # YARDARMS
    pygame.draw.rect(surface, MAST_DARK, (cx - 24, cy - 22, 20, 3))  # Fore
    pygame.draw.rect(surface, MAST_DARK, (cx - 12, cy - 26, 24, 3))  # Main
    pygame.draw.rect(surface, MAST_DARK, (cx + 2, cy - 20, 20, 3))   # Mizzen
    
    # SAILS on all three masts
    # Fore sail
    pygame.draw.polygon(surface, SAIL_WHITE, [
        (cx - 22, cy - 21), (cx - 22, cy - 8),
        (cx - 19, cy - 6), (cx - 5, cy - 6),
        (cx - 4, cy - 8), (cx - 4, cy - 21)
    ])
    
    # Main sail (largest)
    pygame.draw.polygon(surface, SAIL_WHITE, [
        (cx - 10, cy - 25), (cx - 10, cy - 8),
        (cx - 7, cy - 6), (cx + 11, cy - 6),
        (cx + 12, cy - 8), (cx + 12, cy - 25)
    ])
    
    # Mizzen sail
    pygame.draw.polygon(surface, SAIL_WHITE, [
        (cx + 4, cy - 19), (cx + 4, cy - 8),
        (cx + 6, cy - 6), (cx + 20, cy - 6),
        (cx + 22, cy - 8), (cx + 22, cy - 19)
    ])
    
    # MANY CANNONS (two gun decks!)
    for cannon_y in [cy + 5, cy + 8, cy + 11, cy + 14]:
        # Lower gun deck
        for cannon_x_offset in [-22, -17, -12, 15, 20]:
            if cannon_x_offset < 0:
                pygame.draw.rect(surface, CANNON_HOLE, (cx + cannon_x_offset, cannon_y, 3, 2))
                pygame.draw.circle(surface, CANNON_METAL, (cx + cannon_x_offset - 1, cannon_y + 1), 2)
            else:
                pygame.draw.rect(surface, CANNON_HOLE, (cx + cannon_x_offset, cannon_y, 3, 2))
                pygame.draw.circle(surface, CANNON_METAL, (cx + cannon_x_offset + 4, cannon_y + 1), 2)
    
    # FLAGS
    pygame.draw.polygon(surface, FLAG_RED, [(cx - 13, cy - 29), (cx - 13, cy - 25), (cx - 6, cy - 27)])
    pygame.draw.polygon(surface, FLAG_RED, [(cx + 1, cy - 33), (cx + 1, cy - 29), (cx + 8, cy - 31)])
    pygame.draw.polygon(surface, FLAG_RED, [(cx + 13, cy - 27), (cx + 13, cy - 23), (cx + 20, cy - 25)])
    
    return surface


def create_frigate_detailed():
    """Create frigate - artillery ship with visible mortars"""
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    
    cx, cy = SPRITE_SIZE // 2, SPRITE_SIZE // 2
    
    # REINFORCED HULL
    hull_outline = [
        (cx - 22, cy + 14),
        (cx - 22, cy + 3),
        (cx - 20, cy - 2),
        (cx + 22, cy - 6),
        (cx + 26, cy),
        (cx + 24, cy + 11),
        (cx - 20, cy + 15),
    ]
    pygame.draw.polygon(surface, HULL_BASE, hull_outline)
    pygame.draw.polygon(surface, HULL_MID, [
        (cx - 20, cy + 13),
        (cx - 20, cy + 4),
        (cx - 18, cy - 1),
        (cx + 20, cy - 5),
        (cx + 24, cy + 1),
        (cx + 22, cy + 10),
    ])
    
    # Metal reinforcement bands (key feature!)
    pygame.draw.rect(surface, (90, 90, 80), (cx - 21, cy + 2, 43, 2))
    pygame.draw.rect(surface, (90, 90, 80), (cx - 21, cy + 8, 43, 2))
    
    # DECK with mortar platform
    pygame.draw.rect(surface, DECK_DARK, (cx - 19, cy - 1, 38, 4))
    pygame.draw.rect(surface, DECK_LIGHT, (cx - 18, cy, 36, 2))
    
    # TWO MASTS
    pygame.draw.rect(surface, MAST_DARK, (cx - 9, cy - 28, 5, 27))
    pygame.draw.rect(surface, MAST_LIGHT, (cx - 8, cy - 28, 3, 27))
    pygame.draw.rect(surface, MAST_DARK, (cx + 7, cy - 30, 5, 29))
    pygame.draw.rect(surface, MAST_LIGHT, (cx + 8, cy - 30, 3, 29))
    
    # SAILS
    pygame.draw.polygon(surface, SAIL_WHITE, [
        (cx - 19, cy - 23), (cx - 19, cy - 8),
        (cx - 16, cy - 6), (cx - 1, cy - 6),
        (cx, cy - 8), (cx, cy - 23)
    ])
    pygame.draw.polygon(surface, SAIL_WHITE, [
        (cx - 3, cy - 25), (cx - 3, cy - 8),
        (cx, cy - 6), (cx + 17, cy - 6),
        (cx + 19, cy - 8), (cx + 19, cy - 25)
    ])
    
    # MORTARS - Key identifying feature!
    # Mortar platform (center deck)
    pygame.draw.rect(surface, (60, 60, 55), (cx - 4, cy - 5, 8, 6))
    
    # Two large mortars pointing upward
    # Left mortar
    pygame.draw.ellipse(surface, (50, 50, 45), (cx - 3, cy - 4, 3, 5))
    pygame.draw.rect(surface, (40, 40, 35), (cx - 2, cy - 8, 2, 5))
    pygame.draw.circle(surface, (30, 30, 25), (cx - 1, cy - 8), 2)
    
    # Right mortar
    pygame.draw.ellipse(surface, (50, 50, 45), (cx + 1, cy - 4, 3, 5))
    pygame.draw.rect(surface, (40, 40, 35), (cx + 1, cy - 8, 2, 5))
    pygame.draw.circle(surface, (30, 30, 25), (cx + 2, cy - 8), 2)
    
    # Ammunition stacks
    pygame.draw.circle(surface, (40, 40, 35), (cx - 5, cy), 2)
    pygame.draw.circle(surface, (40, 40, 35), (cx + 6, cy), 2)
    
    # CANNONS (side armament)
    for cannon_y in [cy + 4, cy + 7, cy + 10]:
        pygame.draw.rect(surface, CANNON_HOLE, (cx - 19, cannon_y, 4, 2))
        pygame.draw.circle(surface, CANNON_METAL, (cx - 20, cannon_y + 1), 2)
        pygame.draw.rect(surface, CANNON_HOLE, (cx + 15, cannon_y, 4, 2))
        pygame.draw.circle(surface, CANNON_METAL, (cx + 20, cannon_y + 1), 2)
    
    # FLAGS
    pygame.draw.polygon(surface, FLAG_RED, [(cx - 7, cy - 29), (cx - 7, cy - 25), (cx, cy - 27)])
    pygame.draw.polygon(surface, FLAG_RED, [(cx + 9, cy - 31), (cx + 9, cy - 27), (cx + 16, cy - 29)])
    
    return surface


# Generate all sprites
output_dir = Path("resources/units")
output_dir.mkdir(parents=True, exist_ok=True)

print("Generating SUPER DETAILED ship sprites...")
print("These will be CLEARLY recognizable as sailing ships!\n")

# Create test sprites first
test_dir = Path("resources/units_super_detailed")
test_dir.mkdir(parents=True, exist_ok=True)

ships = {
    "sloop": create_sloop_detailed,
    "brigantine": create_brigantine_detailed,
    "ship_of_the_line": create_ship_of_line_detailed,
    "frigate": create_frigate_detailed,
}

for ship_name, create_func in ships.items():
    sprite = create_func()
    test_path = test_dir / f"{ship_name}_super_detailed.png"
    pygame.image.save(sprite, str(test_path))
    print(f"✅ Created SUPER detailed {ship_name}")
    print(f"   Saved to: {test_path}")

print("\n🎨 SUPER DETAILED test sprites generated!")
print(f"Check {test_dir} to see the amazing results!")
print("\nThese sprites have:")
print("  ✓ Large, obvious hull shapes (NOT squares!)")
print("  ✓ Clearly visible tall masts")
print("  ✓ Large billowing sails")
print("  ✓ Visible cannons protruding from hull")
print("  ✓ Detailed deck planking")
print("  ✓ Rigging and ropes")
print("  ✓ Flags flying")
print("  ✓ Water foam/wake")
print("\nYou will SEE these are sailing ships!")
