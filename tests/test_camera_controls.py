"""Test improved panning and zooming controls"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from grid import Grid


def test_drag_detection():
    """Test that drag detection works"""
    pygame.init()
    grid = Grid(cell_size=64, map_file="map_1.txt")
    
    # Create mock events
    # Simulate mouse down
    down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (100, 100)})
    grid.handle_event(down_event, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    assert grid.dragging == True, "Should be in dragging state"
    assert grid.is_dragging() == False, "Should not detect as drag yet (no movement)"
    
    # Simulate small movement (below threshold)
    motion_event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (102, 102)})
    grid.handle_event(motion_event, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    assert grid.is_dragging() == False, "Small movement should not trigger drag"
    
    # Simulate larger movement (above threshold)
    motion_event2 = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (110, 110)})
    grid.handle_event(motion_event2, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    assert grid.is_dragging() == True, "Large movement should trigger drag"
    
    # Simulate mouse up
    up_event = pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (110, 110)})
    grid.handle_event(up_event, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    assert grid.dragging == False, "Should no longer be dragging"
    
    print("✓ Drag detection works correctly")
    pygame.quit()


def test_zoom_at_position():
    """Test that zoom_at_position adjusts offsets correctly"""
    pygame.init()
    grid = Grid(cell_size=64, map_file="map_1.txt")
    
    # Initial state
    initial_zoom = grid.zoom
    initial_offset_x = grid.offset_x
    initial_offset_y = grid.offset_y
    
    # Zoom in at center of screen
    center_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    grid.zoom_at_position(center_pos, 1.5, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    assert grid.zoom > initial_zoom, "Zoom should increase"
    print(f"✓ Zoom increased from {initial_zoom:.2f} to {grid.zoom:.2f}")
    
    # Zoom out at different position
    corner_pos = (100, 100)
    old_zoom = grid.zoom
    grid.zoom_at_position(corner_pos, 0.8, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    assert grid.zoom < old_zoom, "Zoom should decrease"
    print(f"✓ Zoom decreased from {old_zoom:.2f} to {grid.zoom:.2f}")
    
    # Verify offset changed (zooming at non-center position should adjust offset)
    assert grid.offset_x != initial_offset_x or grid.offset_y != initial_offset_y, \
        "Offset should change when zooming at non-center position"
    print(f"✓ Offset adjusted: ({initial_offset_x}, {initial_offset_y}) -> ({grid.offset_x:.1f}, {grid.offset_y:.1f})")
    
    pygame.quit()


def test_panning():
    """Test that panning works correctly"""
    pygame.init()
    grid = Grid(cell_size=64, map_file="map_1.txt")
    
    initial_offset_x = grid.offset_x
    initial_offset_y = grid.offset_y
    
    # Simulate drag
    down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (100, 100)})
    grid.handle_event(down_event, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    motion_event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (150, 150)})
    grid.handle_event(motion_event, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    assert grid.offset_x == initial_offset_x + 50, f"X offset should increase by 50, got {grid.offset_x - initial_offset_x}"
    assert grid.offset_y == initial_offset_y + 50, f"Y offset should increase by 50, got {grid.offset_y - initial_offset_y}"
    
    print(f"✓ Panning works: offset moved by (50, 50)")
    
    pygame.quit()


if __name__ == "__main__":
    print("Testing improved camera controls...\n")
    
    test_drag_detection()
    test_zoom_at_position()
    test_panning()
    
    print("\n✅ All camera control tests passed!")
