"""
Game constants for Combat Alley 2000

This module defines all constant values used throughout the game, including
display settings, colors, and other global configuration values.

All color values are defined as RGB tuples (red, green, blue) with values 0-255.
"""

# ============================================================================
# SCREEN AND DISPLAY SETTINGS
# ============================================================================

# Screen dimensions in pixels
# These define the window size for the game
SCREEN_WIDTH = 1280   # Width of the game window in pixels
SCREEN_HEIGHT = 720   # Height of the game window in pixels

# Frame rate limit
# Controls how many times per second the game updates and renders
FPS = 60  # Target frames per second (60 FPS = ~16.67ms per frame)


# ============================================================================
# COLOR DEFINITIONS
# ============================================================================
# All colors are RGB tuples: (red, green, blue) with values from 0-255

# Basic colors
BLACK = (0, 0, 0)         # Pure black - used for borders and text
WHITE = (255, 255, 255)   # Pure white - used for health bar borders and text

# Grayscale colors
GRAY = (128, 128, 128)         # Medium gray - used for grid lines
LIGHT_GRAY = (192, 192, 192)   # Light gray - used for UI elements

# Themed colors
BLUE = (30, 90, 150)  # Deep blue - used for screen background (like water/ocean)
