"""Test viewport center zoom"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from grid import Grid


def test_viewport_center_zoom():
    """Test that zooming focuses on viewport center, not map center"""
    pygame.init()
    grid = Grid(cell_size=64, map_file="map_1.txt")
    
    # Pan the view away from center to make it obvious
    grid.offset_x = 200
    grid.offset_y = 100
    
    print(f"Initial state:")
    print(f"  Zoom: {grid.zoom:.2f}")
    print(f"  Offset: ({grid.offset_x:.1f}, {grid.offset_y:.1f})")
    
    # Calculate what's at viewport center before zoom
    grid_world_width, grid_world_height = grid.get_grid_world_size()
    scaled_width = grid_world_width * grid.zoom
    scaled_height = grid_world_height * grid.zoom
    
    grid_origin_x = (SCREEN_WIDTH - scaled_width) / 2 + grid.offset_x
    grid_origin_y = (SCREEN_HEIGHT - scaled_height) / 2 + grid.offset_y
    
    viewport_center_x = SCREEN_WIDTH / 2
    viewport_center_y = SCREEN_HEIGHT / 2
    
    world_x_before = (viewport_center_x - grid_origin_x) / grid.zoom
    world_y_before = (viewport_center_y - grid_origin_y) / grid.zoom
    
    print(f"  World position at viewport center: ({world_x_before:.1f}, {world_y_before:.1f})")
    
    # Zoom in at viewport center
    print(f"\nZooming in 2x at viewport center...")
    grid.zoom_at_viewport_center(2.0, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    print(f"After zoom:")
    print(f"  Zoom: {grid.zoom:.2f}")
    print(f"  Offset: ({grid.offset_x:.1f}, {grid.offset_y:.1f})")
    
    # Calculate what's at viewport center after zoom
    scaled_width_after = grid_world_width * grid.zoom
    scaled_height_after = grid_world_height * grid.zoom
    
    grid_origin_x_after = (SCREEN_WIDTH - scaled_width_after) / 2 + grid.offset_x
    grid_origin_y_after = (SCREEN_HEIGHT - scaled_height_after) / 2 + grid.offset_y
    
    world_x_after = (viewport_center_x - grid_origin_x_after) / grid.zoom
    world_y_after = (viewport_center_y - grid_origin_y_after) / grid.zoom
    
    print(f"  World position at viewport center: ({world_x_after:.1f}, {world_y_after:.1f})")
    
    # The world position at viewport center should be the same
    delta_x = abs(world_x_after - world_x_before)
    delta_y = abs(world_y_after - world_y_before)
    
    print(f"  Delta: ({delta_x:.3f}, {delta_y:.3f})")
    
    if delta_x < 0.1 and delta_y < 0.1:
        print("✓ CORRECT: World position at viewport center remained stable")
    else:
        print(f"✗ WRONG: World position shifted by ({delta_x:.3f}, {delta_y:.3f})")
    
    # Test zoom out as well
    print(f"\nZooming out 0.5x...")
    grid.zoom_at_viewport_center(0.5, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    print(f"After zoom out:")
    print(f"  Zoom: {grid.zoom:.2f}")
    print(f"  Offset: ({grid.offset_x:.1f}, {grid.offset_y:.1f})")
    
    # Check again
    scaled_width_final = grid_world_width * grid.zoom
    scaled_height_final = grid_world_height * grid.zoom
    
    grid_origin_x_final = (SCREEN_WIDTH - scaled_width_final) / 2 + grid.offset_x
    grid_origin_y_final = (SCREEN_HEIGHT - scaled_height_final) / 2 + grid.offset_y
    
    world_x_final = (viewport_center_x - grid_origin_x_final) / grid.zoom
    world_y_final = (viewport_center_y - grid_origin_y_final) / grid.zoom
    
    print(f"  World position at viewport center: ({world_x_final:.1f}, {world_y_final:.1f})")
    
    delta_x_final = abs(world_x_final - world_x_before)
    delta_y_final = abs(world_y_final - world_y_before)
    
    print(f"  Delta from original: ({delta_x_final:.3f}, {delta_y_final:.3f})")
    
    if delta_x_final < 0.1 and delta_y_final < 0.1:
        print("✓ CORRECT: World position remained stable through zoom out")
    else:
        print(f"✗ WRONG: World position shifted by ({delta_x_final:.3f}, {delta_y_final:.3f})")
    
    pygame.quit()


if __name__ == "__main__":
    print("Testing viewport center zoom...\n")
    test_viewport_center_zoom()
    print("\n✅ Viewport center zoom test completed!")
