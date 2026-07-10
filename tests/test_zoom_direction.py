"""Test zoom direction is correct"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from grid import Grid


def test_zoom_direction():
    """Test that zooming in moves the map away from cursor and zooming out toward cursor"""
    pygame.init()
    grid = Grid(cell_size=64, map_file="map_1.txt")
    
    # Position cursor in top-left area (100, 100)
    cursor_pos = (100, 100)
    
    # Get initial grid position at cursor
    # Calculate where grid origin is on screen initially
    grid_world_width, grid_world_height = grid.get_grid_world_size()
    scaled_width = grid_world_width * grid.zoom
    scaled_height = grid_world_height * grid.zoom
    
    initial_grid_x = (SCREEN_WIDTH - scaled_width) / 2 + grid.offset_x
    initial_grid_y = (SCREEN_HEIGHT - scaled_height) / 2 + grid.offset_y
    
    print(f"Initial state:")
    print(f"  Cursor at: {cursor_pos}")
    print(f"  Grid origin on screen: ({initial_grid_x:.1f}, {initial_grid_y:.1f})")
    print(f"  Zoom: {grid.zoom:.2f}")
    print(f"  Offset: ({grid.offset_x:.1f}, {grid.offset_y:.1f})")
    
    # Zoom IN at cursor position (should zoom toward the cursor area)
    # This means the grid should move RIGHT and DOWN (toward the cursor at 100,100)
    print(f"\nZooming IN (2x) at cursor {cursor_pos}...")
    grid.zoom_at_position(cursor_pos, 2.0, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    scaled_width_after = grid_world_width * grid.zoom
    scaled_height_after = grid_world_height * grid.zoom
    new_grid_x = (SCREEN_WIDTH - scaled_width_after) / 2 + grid.offset_x
    new_grid_y = (SCREEN_HEIGHT - scaled_height_after) / 2 + grid.offset_y
    
    print(f"After zoom in:")
    print(f"  Grid origin on screen: ({new_grid_x:.1f}, {new_grid_y:.1f})")
    print(f"  Zoom: {grid.zoom:.2f}")
    print(f"  Offset: ({grid.offset_x:.1f}, {grid.offset_y:.1f})")
    
    # When zooming IN toward top-left corner (100, 100):
    # The grid should shift toward that corner (move right and down)
    # So new_grid_x should be > initial_grid_x (moving right)
    # And new_grid_y should be > initial_grid_y (moving down)
    # Actually wait - if we're zooming toward a point, the grid around that point expands
    # The corner should move AWAY from the center
    # Since cursor is in top-left, grid should move UP and LEFT (negative direction)
    
    delta_x = new_grid_x - initial_grid_x
    delta_y = new_grid_y - initial_grid_y
    
    print(f"  Grid moved: ({delta_x:.1f}, {delta_y:.1f})")
    
    # When zooming IN toward top-left (cursor at 100,100 which is left and up from center):
    # The world content should expand around that point
    # Things above and left of cursor should move more up and left
    # Things below and right should move more down and right
    # The grid origin (top-left of map) is likely above and left of cursor
    # So it should move UP (negative Y) and LEFT (negative X)
    
    if delta_x < 0 and delta_y < 0:
        print("✓ CORRECT: Grid moved up-left when zooming in toward top-left cursor")
    else:
        print(f"✗ WRONG: Expected negative delta when zooming toward top-left, got ({delta_x:.1f}, {delta_y:.1f})")
    
    pygame.quit()


if __name__ == "__main__":
    test_zoom_direction()
