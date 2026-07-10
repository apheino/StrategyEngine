"""Test simple center zoom"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from grid import Grid


def test_simple_zoom():
    """Test that simple zoom in/out works"""
    pygame.init()
    grid = Grid(cell_size=64, map_file="map_1.txt")
    
    initial_zoom = grid.zoom
    print(f"Initial zoom: {initial_zoom}")
    
    # Simulate zoom in (mouse wheel up)
    zoom_in_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 4, 'pos': (640, 360)})
    grid.handle_event(zoom_in_event, 1280, 720)
    
    assert grid.zoom > initial_zoom, f"Zoom should increase, was {initial_zoom}, now {grid.zoom}"
    print(f"✓ Zoom in works: {initial_zoom} -> {grid.zoom}")
    
    mid_zoom = grid.zoom
    
    # Simulate zoom out (mouse wheel down)
    zoom_out_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 5, 'pos': (640, 360)})
    grid.handle_event(zoom_out_event, 1280, 720)
    
    assert grid.zoom < mid_zoom, f"Zoom should decrease, was {mid_zoom}, now {grid.zoom}"
    print(f"✓ Zoom out works: {mid_zoom} -> {grid.zoom}")
    
    # Test zoom limits
    for i in range(100):
        zoom_in_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 4, 'pos': (640, 360)})
        grid.handle_event(zoom_in_event, 1280, 720)
    
    assert grid.zoom <= grid.max_zoom, f"Zoom should not exceed max ({grid.max_zoom}), got {grid.zoom}"
    print(f"✓ Max zoom limit enforced: {grid.zoom} <= {grid.max_zoom}")
    
    for i in range(100):
        zoom_out_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 5, 'pos': (640, 360)})
        grid.handle_event(zoom_out_event, 1280, 720)
    
    assert grid.zoom >= grid.min_zoom, f"Zoom should not go below min ({grid.min_zoom}), got {grid.zoom}"
    print(f"✓ Min zoom limit enforced: {grid.zoom} >= {grid.min_zoom}")
    
    pygame.quit()


if __name__ == "__main__":
    print("Testing simple center zoom...\n")
    test_simple_zoom()
    print("\n✅ Simple zoom works correctly!")
