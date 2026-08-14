"""
View animated water tiles in action
Shows all 8 frames cycling to see the wave motion
"""

import pygame
import os
import time

pygame.init()

# Display configuration
TILE_SIZE = 32
SCALE = 4  # Scale up for better viewing
DISPLAY_SIZE = TILE_SIZE * SCALE
PADDING = 20

# Create window
screen = pygame.display.set_mode((DISPLAY_SIZE * 2 + PADDING * 3, DISPLAY_SIZE + PADDING * 2 + 50))
pygame.display.set_caption('Caribbean Water Animation - Wave Flow')

# Load all 8 frames for both water types
open_water_frames = []
deep_channel_frames = []

for i in range(8):
    # Open water
    path = f"resources/icons/open_water_frame_{i}.png"
    if os.path.exists(path):
        frame = pygame.image.load(path)
        scaled = pygame.transform.scale(frame, (DISPLAY_SIZE, DISPLAY_SIZE))
        open_water_frames.append(scaled)
    
    # Deep channel
    path = f"resources/icons/deep_channel_frame_{i}.png"
    if os.path.exists(path):
        frame = pygame.image.load(path)
        scaled = pygame.transform.scale(frame, (DISPLAY_SIZE, DISPLAY_SIZE))
        deep_channel_frames.append(scaled)

# Font
font = pygame.font.Font(None, 28)
title_font = pygame.font.Font(None, 36)

# Animation control
clock = pygame.time.Clock()
frame_index = 0
frame_time = 0
FPS = 60
FRAME_DURATION = 0.15  # Same as in game

print("🌊 Water Animation Viewer")
print("   Watch the waves flow naturally!")
print("   Press any key or close window to exit")

running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
    frame_time += dt
    
    # Advance frame
    if frame_time >= FRAME_DURATION:
        frame_time = 0
        frame_index = (frame_index + 1) % 8
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            running = False
    
    # Clear screen
    screen.fill((20, 30, 50))
    
    # Title
    title = title_font.render('Caribbean Water Animation', True, (255, 255, 255))
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 10))
    
    # Draw current frames
    if open_water_frames:
        screen.blit(open_water_frames[frame_index], (PADDING, PADDING + 40))
        label = font.render('Open Water', True, (200, 220, 255))
        screen.blit(label, (PADDING + DISPLAY_SIZE // 2 - label.get_width() // 2, 
                           PADDING + DISPLAY_SIZE + 45))
    
    if deep_channel_frames:
        screen.blit(deep_channel_frames[frame_index], (PADDING * 2 + DISPLAY_SIZE, PADDING + 40))
        label = font.render('Deep Channel', True, (150, 180, 220))
        screen.blit(label, (PADDING * 2 + DISPLAY_SIZE + DISPLAY_SIZE // 2 - label.get_width() // 2, 
                           PADDING + DISPLAY_SIZE + 45))
    
    # Frame counter
    frame_text = font.render(f'Frame {frame_index + 1}/8', True, (180, 180, 180))
    screen.blit(frame_text, (screen.get_width() // 2 - frame_text.get_width() // 2, 
                            screen.get_height() - 25))
    
    pygame.display.flip()

pygame.quit()
print("✅ Animation viewer closed")
