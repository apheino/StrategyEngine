#!/usr/bin/env python3
"""
Create placeholder structure bitmaps for Combat Alley 2000.
Generates simple placeholder images for headquarters, hangar, and sandbag structures.
"""

import pygame
import os
from pathlib import Path

# Initialize Pygame
pygame.init()

# Create output directory
output_dir = Path("resources/structures")
output_dir.mkdir(parents=True, exist_ok=True)

# Image size
SIZE = 64


def create_headquarters():
    """Create headquarters (base) placeholder."""
    surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    
    # Background - fortress style
    pygame.draw.rect(surface, (80, 80, 100), (4, 4, SIZE-8, SIZE-8))
    
    # Main building
    pygame.draw.rect(surface, (100, 100, 120), (8, 16, SIZE-16, SIZE-20))
    
    # Roof
    points = [(8, 16), (SIZE//2, 6), (SIZE-8, 16)]
    pygame.draw.polygon(surface, (120, 120, 140), points)
    
    # Windows
    for i in range(2):
        for j in range(2):
            x = 16 + i * 20
            y = 24 + j * 12
            pygame.draw.rect(surface, (200, 200, 100), (x, y, 8, 8))
    
    # Door
    pygame.draw.rect(surface, (60, 40, 20), (SIZE//2 - 6, SIZE-16, 12, 12))
    
    # Flag on top
    pygame.draw.line(surface, (150, 150, 150), (SIZE//2, 6), (SIZE//2, 2), 2)
    pygame.draw.polygon(surface, (255, 50, 50), [(SIZE//2, 2), (SIZE//2+8, 4), (SIZE//2, 6)])
    
    # Border
    pygame.draw.rect(surface, (0, 0, 0), (4, 4, SIZE-8, SIZE-8), 2)
    
    # Add "HQ" text
    font = pygame.font.Font(None, 20)
    text = font.render("HQ", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SIZE//2, SIZE-8))
    surface.blit(text, text_rect)
    
    return surface


def create_hangar():
    """Create hangar placeholder."""
    surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    
    # Background - industrial green
    pygame.draw.rect(surface, (60, 80, 60), (4, 8, SIZE-8, SIZE-12))
    
    # Roof - curved hangar style
    pygame.draw.arc(surface, (80, 100, 80), (4, -10, SIZE-8, 40), 0, 3.14, 4)
    
    # Main structure
    pygame.draw.rect(surface, (70, 90, 70), (8, 16, SIZE-16, SIZE-20))
    
    # Large door
    pygame.draw.rect(surface, (40, 40, 40), (12, SIZE-24, SIZE-24, 20))
    
    # Door segments (vertical lines)
    for i in range(1, 4):
        x = 12 + i * (SIZE-24) // 4
        pygame.draw.line(surface, (60, 60, 60), (x, SIZE-24), (x, SIZE-4), 1)
    
    # Windows on top
    for i in range(3):
        x = 16 + i * 12
        pygame.draw.rect(surface, (150, 200, 255), (x, 12, 8, 6))
    
    # Border
    pygame.draw.rect(surface, (0, 0, 0), (4, 8, SIZE-8, SIZE-12), 2)
    
    return surface


def create_sandbag():
    """Create sandbag placeholder."""
    surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    
    # Draw stacked sandbags
    bag_color = (160, 140, 100)
    bag_outline = (120, 100, 70)
    
    # Bottom row - 3 bags
    for i in range(3):
        x = 8 + i * 16
        y = SIZE - 16
        pygame.draw.ellipse(surface, bag_color, (x, y, 14, 12))
        pygame.draw.ellipse(surface, bag_outline, (x, y, 14, 12), 1)
    
    # Middle row - 2 bags
    for i in range(2):
        x = 16 + i * 16
        y = SIZE - 28
        pygame.draw.ellipse(surface, bag_color, (x, y, 14, 12))
        pygame.draw.ellipse(surface, bag_outline, (x, y, 14, 12), 1)
    
    # Top row - 1 bag
    x = 24
    y = SIZE - 40
    pygame.draw.ellipse(surface, bag_color, (x, y, 14, 12))
    pygame.draw.ellipse(surface, bag_outline, (x, y, 14, 12), 1)
    
    # Add some texture lines
    for i in range(6):
        bag_x = 8 + (i % 3) * 16
        bag_y = SIZE - 16 - (i // 3) * 12
        pygame.draw.line(surface, bag_outline, (bag_x+2, bag_y+6), (bag_x+12, bag_y+6), 1)
    
    return surface


def main():
    """Generate all structure placeholders."""
    structures = {
        'headquarters': create_headquarters,
        'hangar': create_hangar,
        'sandbag': create_sandbag,
    }
    
    print("Creating structure placeholders...")
    
    for name, create_func in structures.items():
        surface = create_func()
        output_path = output_dir / f"{name}.png"
        pygame.image.save(surface, str(output_path))
        print(f"  ✓ Created {output_path}")
    
    print(f"\nAll structure placeholders created in {output_dir}/")


if __name__ == "__main__":
    main()
