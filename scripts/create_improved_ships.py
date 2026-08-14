"""
Create proper pixel art naval ship sprites with realistic top-down views
"""

import pygame
import os
from pathlib import Path

# Initialize Pygame
pygame.init()

SPRITE_SIZE = 64
TRANSPARENT = (0, 0, 0, 0)

# Color palettes
HULL_DARK = (90, 60, 30)
HULL_MID = (140, 100, 60)
HULL_LIGHT = (180, 140, 90)
DECK_DARK = (110, 80, 40)
DECK_MID = (150, 110, 60)
SAIL_WHITE = (240, 240, 230)
SAIL_SHADOW = (180, 180, 170)
WOOD_DARK = (80, 50, 20)
WOOD_MID = (120, 80, 40)
CANNON_BLACK = (30, 30, 30)
METAL_GRAY = (100, 100, 90)
WATER_FOAM = (255, 255, 255)
ROPE_BROWN = (60, 40, 20)


def create_pixel_ship(ship_type, team_color=None):
    """Create a ship sprite with proper pixel art from top-down view"""
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    
    cx, cy = SPRITE_SIZE // 2, SPRITE_SIZE // 2
    sail_color = team_color if team_color else SAIL_WHITE
    
    if ship_type == "sloop":
        # SLOOP - Small merchant vessel
        # Hull (proper ship shape)
        # Bow (front - pointed)
        pygame.draw.circle(surface, HULL_DARK, (cx, cy - 14), 4)
        pygame.draw.rect(surface, HULL_DARK, (cx - 4, cy - 14, 8, 2))
        
        # Main hull body (wide in middle, tapered at ends)
        pygame.draw.rect(surface, HULL_MID, (cx - 7, cy - 12, 14, 20))
        pygame.draw.rect(surface, HULL_LIGHT, (cx - 6, cy - 12, 6, 20))  # Highlight left side
        
        # Stern (back - rounded)
        pygame.draw.circle(surface, HULL_DARK, (cx, cy + 9), 5)
        pygame.draw.rect(surface, HULL_DARK, (cx - 5, cy + 8, 10, 2))
        
        # Deck planking (visible from top)
        for y in range(cy - 10, cy + 8, 2):
            pygame.draw.line(surface, DECK_DARK, (cx - 5, y), (cx + 5, y), 1)
        
        # Railings
        pygame.draw.line(surface, HULL_DARK, (cx - 7, cy - 10), (cx - 7, cy + 7), 1)
        pygame.draw.line(surface, HULL_DARK, (cx + 7, cy - 10), (cx + 7, cy + 7), 1)
        
        # Mast
        pygame.draw.rect(surface, WOOD_DARK, (cx - 1, cy - 8, 2, 16))
        
        # Yardarm (horizontal spar)
        pygame.draw.rect(surface, WOOD_MID, (cx - 10, cy - 4, 20, 2))
        
        # Sail
        pygame.draw.rect(surface, sail_color, (cx - 9, cy - 2, 18, 10))
        pygame.draw.rect(surface, SAIL_SHADOW, (cx - 9, cy - 2, 2, 10))  # Left edge shadow
        pygame.draw.rect(surface, SAIL_SHADOW, (cx + 7, cy - 2, 2, 10))  # Right edge shadow
        
        # Rigging lines
        pygame.draw.line(surface, ROPE_BROWN, (cx - 10, cy - 4), (cx - 7, cy + 2), 1)
        pygame.draw.line(surface, ROPE_BROWN, (cx + 10, cy - 4), (cx + 7, cy + 2), 1)
        
        # Cannons (3 per side)
        for i in range(3):
            y = cy - 6 + i * 5
            pygame.draw.rect(surface, CANNON_BLACK, (cx - 7, y, 2, 2))
            pygame.draw.rect(surface, CANNON_BLACK, (cx + 5, y, 2, 2))
        
        # Stern cabin
        pygame.draw.rect(surface, WOOD_DARK, (cx - 3, cy + 6, 6, 3))
        surface.set_at((cx - 1, cy + 7), (200, 200, 100))  # Window
        surface.set_at((cx + 1, cy + 7), (200, 200, 100))  # Window
        
        # Bow detail
        pygame.draw.line(surface, WOOD_DARK, (cx, cy - 16), (cx, cy - 18), 2)  # Bowsprit
        
        # Wake
        pygame.draw.circle(surface, WATER_FOAM, (cx - 4, cy + 11), 1)
        pygame.draw.circle(surface, WATER_FOAM, (cx + 4, cy + 11), 1)
        
    elif ship_type == "brigantine":
        # BRIGANTINE - Fast two-masted vessel
        # Hull (longer, sleeker)
        pygame.draw.circle(surface, HULL_DARK, (cx, cy - 16), 4)
        pygame.draw.rect(surface, HULL_DARK, (cx - 4, cy - 16, 8, 2))
        pygame.draw.rect(surface, HULL_MID, (cx - 8, cy - 14, 16, 24))
        pygame.draw.rect(surface, HULL_LIGHT, (cx - 7, cy - 14, 7, 24))
        pygame.draw.circle(surface, HULL_DARK, (cx, cy + 11), 6)
        pygame.draw.rect(surface, HULL_DARK, (cx - 6, cy + 10, 12, 2))
        
        # Deck
        for y in range(cy - 12, cy + 10, 2):
            width = 7 - abs(y - cy) // 6
            pygame.draw.line(surface, DECK_DARK, (cx - width, y), (cx + width, y), 1)
        
        # Railings
        pygame.draw.line(surface, HULL_DARK, (cx - 8, cy - 12), (cx - 8, cy + 9), 1)
        pygame.draw.line(surface, HULL_DARK, (cx + 8, cy - 12), (cx + 8, cy + 9), 1)
        
        # Two masts
        pygame.draw.rect(surface, WOOD_DARK, (cx - 4, cy - 12, 2, 18))  # Fore mast
        pygame.draw.rect(surface, WOOD_DARK, (cx + 3, cy - 8, 2, 14))   # Main mast
        
        # Yardarms
        pygame.draw.rect(surface, WOOD_MID, (cx - 12, cy - 8, 16, 2))
        pygame.draw.rect(surface, WOOD_MID, (cx + 1, cy - 4, 12, 2))
        
        # Sails
        pygame.draw.rect(surface, sail_color, (cx - 11, cy - 6, 14, 8))
        pygame.draw.rect(surface, SAIL_SHADOW, (cx - 11, cy - 6, 2, 8))
        pygame.draw.rect(surface, sail_color, (cx + 2, cy - 2, 10, 6))
        pygame.draw.rect(surface, SAIL_SHADOW, (cx + 2, cy - 2, 2, 6))
        
        # Rigging
        pygame.draw.line(surface, ROPE_BROWN, (cx - 12, cy - 8), (cx - 8, cy), 1)
        pygame.draw.line(surface, ROPE_BROWN, (cx + 4, cy - 8), (cx + 8, cy), 1)
        pygame.draw.line(surface, ROPE_BROWN, (cx + 12, cy - 4), (cx + 8, cy + 2), 1)
        
        # Cannons (4 per side)
        for i in range(4):
            y = cy - 8 + i * 5
            pygame.draw.rect(surface, CANNON_BLACK, (cx - 8, y, 2, 2))
            pygame.draw.rect(surface, CANNON_BLACK, (cx + 6, y, 2, 2))
        
        # Stern cabin
        pygame.draw.rect(surface, WOOD_DARK, (cx - 4, cy + 8, 8, 3))
        for i in range(3):
            surface.set_at((cx - 3 + i * 3, cy + 9), (200, 200, 100))
        
        # Bowsprit
        pygame.draw.line(surface, WOOD_DARK, (cx, cy - 18), (cx, cy - 21), 2)
        
        # Wake
        for i in range(3):
            pygame.draw.circle(surface, WATER_FOAM, (cx - 5 + i * 5, cy + 13), 1)
        
    elif ship_type == "ship_of_the_line":
        # SHIP OF THE LINE - Massive warship
        # Hull (very large and wide)
        pygame.draw.circle(surface, HULL_DARK, (cx, cy - 14), 5)
        pygame.draw.rect(surface, HULL_DARK, (cx - 5, cy - 14, 10, 2))
        pygame.draw.rect(surface, HULL_MID, (cx - 12, cy - 12, 24, 22))
        pygame.draw.rect(surface, HULL_LIGHT, (cx - 11, cy - 12, 11, 22))
        
        # Gun deck stripe (classic warship)
        pygame.draw.rect(surface, (220, 200, 150), (cx - 11, cy - 4, 22, 3))
        
        # Stern
        pygame.draw.circle(surface, HULL_DARK, (cx, cy + 11), 8)
        pygame.draw.rect(surface, HULL_DARK, (cx - 8, cy + 10, 16, 2))
        
        # Deck
        for y in range(cy - 10, cy + 10, 2):
            width = 10 - abs(y - cy) // 5
            pygame.draw.line(surface, DECK_DARK, (cx - width, y), (cx + width, y), 1)
        
        # Railings
        pygame.draw.line(surface, HULL_DARK, (cx - 12, cy - 10), (cx - 12, cy + 9), 1)
        pygame.draw.line(surface, HULL_DARK, (cx + 12, cy - 10), (cx + 12, cy + 9), 1)
        
        # Three masts
        pygame.draw.rect(surface, WOOD_DARK, (cx - 7, cy - 16, 2, 22))  # Fore
        pygame.draw.rect(surface, WOOD_DARK, (cx - 1, cy - 18, 2, 24))  # Main (tallest)
        pygame.draw.rect(surface, WOOD_DARK, (cx + 5, cy - 14, 2, 20))  # Mizzen
        
        # Yardarms
        pygame.draw.rect(surface, WOOD_MID, (cx - 14, cy - 12, 14, 2))
        pygame.draw.rect(surface, WOOD_MID, (cx - 8, cy - 14, 14, 2))
        pygame.draw.rect(surface, WOOD_MID, (cx + 3, cy - 10, 10, 2))
        
        # Sails (three large sails)
        pygame.draw.rect(surface, sail_color, (cx - 13, cy - 10, 12, 10))
        pygame.draw.rect(surface, SAIL_SHADOW, (cx - 13, cy - 10, 2, 10))
        pygame.draw.rect(surface, sail_color, (cx - 7, cy - 12, 12, 12))
        pygame.draw.rect(surface, SAIL_SHADOW, (cx - 7, cy - 12, 2, 12))
        pygame.draw.rect(surface, sail_color, (cx + 4, cy - 8, 8, 8))
        pygame.draw.rect(surface, SAIL_SHADOW, (cx + 4, cy - 8, 2, 8))
        
        # Rigging (complex)
        pygame.draw.line(surface, ROPE_BROWN, (cx - 14, cy - 12), (cx - 12, cy - 2), 1)
        pygame.draw.line(surface, ROPE_BROWN, (cx - 1, cy - 12), (cx + 12, cy - 2), 1)
        pygame.draw.line(surface, ROPE_BROWN, (cx + 12, cy - 10), (cx + 12, cy), 1)
        
        # Two gun decks!
        # Upper deck (5 guns per side)
        for i in range(5):
            y = cy - 8 + i * 4
            pygame.draw.rect(surface, CANNON_BLACK, (cx - 12, y, 2, 2))
            pygame.draw.rect(surface, CANNON_BLACK, (cx + 10, y, 2, 2))
        
        # Lower deck (4 guns per side)
        for i in range(4):
            y = cy - 6 + i * 4
            pygame.draw.rect(surface, CANNON_BLACK, (cx - 10, y, 2, 2))
            pygame.draw.rect(surface, CANNON_BLACK, (cx + 8, y, 2, 2))
        
        # Ornate stern gallery
        pygame.draw.rect(surface, WOOD_MID, (cx - 8, cy + 8, 16, 4))
        for i in range(5):
            surface.set_at((cx - 7 + i * 4, cy + 9), (200, 180, 100))
        
        # Figurehead
        pygame.draw.line(surface, WOOD_DARK, (cx, cy - 16), (cx, cy - 19), 3)
        pygame.draw.circle(surface, (200, 160, 80), (cx, cy - 20), 2)
        
        # Large wake
        for i in range(5):
            pygame.draw.circle(surface, WATER_FOAM, (cx - 8 + i * 4, cy + 13), 2)
        
    elif ship_type == "frigate":
        # FRIGATE - Artillery vessel with mortars
        # Hull (sturdy, reinforced)
        pygame.draw.circle(surface, HULL_DARK, (cx, cy - 15), 4)
        pygame.draw.rect(surface, HULL_DARK, (cx - 4, cy - 15, 8, 2))
        pygame.draw.rect(surface, HULL_MID, (cx - 10, cy - 13, 20, 22))
        pygame.draw.rect(surface, HULL_LIGHT, (cx - 9, cy - 13, 9, 22))
        pygame.draw.circle(surface, HULL_DARK, (cx, cy + 10), 7)
        pygame.draw.rect(surface, HULL_DARK, (cx - 7, cy + 9, 14, 2))
        
        # Reinforcement bands (metal)
        pygame.draw.line(surface, METAL_GRAY, (cx - 9, cy - 6), (cx + 9, cy - 6), 2)
        pygame.draw.line(surface, METAL_GRAY, (cx - 9, cy + 2), (cx + 9, cy + 2), 2)
        
        # Deck
        for y in range(cy - 11, cy + 9, 2):
            width = 8 - abs(y - cy) // 5
            pygame.draw.line(surface, DECK_DARK, (cx - width, y), (cx + width, y), 1)
        
        # Armored mortar platform (center deck)
        pygame.draw.rect(surface, METAL_GRAY, (cx - 6, cy - 4, 12, 8))
        pygame.draw.rect(surface, (80, 80, 70), (cx - 5, cy - 3, 10, 6))
        
        # Two masts
        pygame.draw.rect(surface, WOOD_DARK, (cx - 5, cy - 14, 2, 18))
        pygame.draw.rect(surface, WOOD_DARK, (cx + 4, cy - 12, 2, 16))
        
        # Yardarms
        pygame.draw.rect(surface, WOOD_MID, (cx - 12, cy - 10, 14, 2))
        pygame.draw.rect(surface, WOOD_MID, (cx + 2, cy - 8, 12, 2))
        
        # Sails
        pygame.draw.rect(surface, sail_color, (cx - 11, cy - 8, 12, 8))
        pygame.draw.rect(surface, SAIL_SHADOW, (cx - 11, cy - 8, 2, 8))
        pygame.draw.rect(surface, sail_color, (cx + 3, cy - 6, 10, 6))
        pygame.draw.rect(surface, SAIL_SHADOW, (cx + 3, cy - 6, 2, 6))
        
        # Rigging
        pygame.draw.line(surface, ROPE_BROWN, (cx - 12, cy - 10), (cx - 10, cy - 2), 1)
        pygame.draw.line(surface, ROPE_BROWN, (cx + 1, cy - 10), (cx + 10, cy - 2), 1)
        pygame.draw.line(surface, ROPE_BROWN, (cx + 12, cy - 8), (cx + 10, cy), 1)
        
        # MORTAR CANNONS (prominent on deck - main feature!)
        # Left mortar
        pygame.draw.circle(surface, METAL_GRAY, (cx - 3, cy - 1), 3)
        pygame.draw.circle(surface, (60, 60, 60), (cx - 3, cy - 1), 2)
        pygame.draw.circle(surface, CANNON_BLACK, (cx - 3, cy - 1), 1)
        # Right mortar  
        pygame.draw.circle(surface, METAL_GRAY, (cx + 3, cy - 1), 3)
        pygame.draw.circle(surface, (60, 60, 60), (cx + 3, cy - 1), 2)
        pygame.draw.circle(surface, CANNON_BLACK, (cx + 3, cy - 1), 1)
        
        # Ammunition stacks
        for i in range(2):
            pygame.draw.circle(surface, (70, 70, 70), (cx - 6, cy + 2 + i * 2), 1)
            pygame.draw.circle(surface, (70, 70, 70), (cx + 6, cy + 2 + i * 2), 1)
        
        # Side cannons (3 per side)
        for i in range(3):
            y = cy - 8 + i * 6
            pygame.draw.rect(surface, CANNON_BLACK, (cx - 10, y, 2, 2))
            pygame.draw.rect(surface, CANNON_BLACK, (cx + 8, y, 2, 2))
        
        # Stern cabin
        pygame.draw.rect(surface, WOOD_DARK, (cx - 5, cy + 7, 10, 3))
        for i in range(3):
            surface.set_at((cx - 4 + i * 4, cy + 8), (200, 200, 100))
        
        # Bow reinforcement
        pygame.draw.line(surface, METAL_GRAY, (cx - 2, cy - 15), (cx - 2, cy - 11), 2)
        pygame.draw.line(surface, METAL_GRAY, (cx + 2, cy - 15), (cx + 2, cy - 11), 2)
        
        # Wake
        for i in range(4):
            pygame.draw.circle(surface, WATER_FOAM, (cx - 6 + i * 4, cy + 12), 1)
    
    return surface


# Test generation
if __name__ == "__main__":
    print("Generating improved naval sprites...")
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "resources" / "units_improved"
    output_dir.mkdir(exist_ok=True)
    
    ship_types = ["sloop", "brigantine", "ship_of_the_line", "frigate"]
    
    for ship_type in ship_types:
        print(f"Creating {ship_type}...")
        sprite = create_pixel_ship(ship_type)
        filename = output_dir / f"{ship_type}_test.png"
        pygame.image.save(sprite, str(filename))
        print(f"  Saved: {filename}")
    
    print("\n✅ Improved ship sprites generated!")
    print(f"Check {output_dir} to see the results")
