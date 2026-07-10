#!/usr/bin/env python3
"""Test script to verify grid dimensions are loaded correctly from map files"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grid import Grid

print("Testing grid size detection from map files:\n")

# Test map_1.txt (10x10)
print("Loading map_1.txt:")
grid1 = Grid(cell_size=64, map_file="map_1.txt")
print(f"  Grid dimensions: {grid1.grid_height} rows x {grid1.grid_width} columns")
print(f"  Expected: 10 x 10")
print(f"  ✓ PASS" if grid1.grid_height == 10 and grid1.grid_width == 10 else "  ✗ FAIL")
print()

# Test map_2.txt (8x15)
print("Loading map_2.txt:")
grid2 = Grid(cell_size=64, map_file="map_2.txt")
print(f"  Grid dimensions: {grid2.grid_height} rows x {grid2.grid_width} columns")
print(f"  Expected: 8 x 15")
print(f"  ✓ PASS" if grid2.grid_height == 8 and grid2.grid_width == 15 else "  ✗ FAIL")
print()

# Test non-existent map (should create default 10x10)
print("Loading non_existent.txt (should create default 10x10):")
grid3 = Grid(cell_size=64, map_file="non_existent.txt")
print(f"  Grid dimensions: {grid3.grid_height} rows x {grid3.grid_width} columns")
print(f"  Expected: 10 x 10 (default)")
print(f"  ✓ PASS" if grid3.grid_height == 10 and grid3.grid_width == 10 else "  ✗ FAIL")
print()

print("All tests completed!")
