#!/usr/bin/env python3
"""Test script for animated movement system"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unit import Unit

print("Testing Animated Movement System\n")
print("=" * 60)

# Create a test unit
print("\nCreating soldier unit at position (5, 5):")
print("-" * 60)
soldier = Unit(unit_type="soldier", team=0, position=(5, 5))
print(f"Initial position: {soldier.position}")
print(f"Speed: {soldier.speed} cells/second")
print(f"Is moving: {soldier.is_moving}")
print(f"Current animation: {soldier.current_animation}")

# Start movement
print("\nStarting movement to (5, 8):")
print("-" * 60)
soldier.move_to((5, 8))
print(f"Target position: {soldier.movement_target_pos}")
print(f"Is moving: {soldier.is_moving}")
print(f"Current animation: {soldier.current_animation}")
print(f"Movement progress: {soldier.movement_progress}")

# Simulate animation frames
print("\nSimulating animation frames (0.1s each):")
print("-" * 60)
dt = 0.1  # 100ms per frame
total_time = 0.0

while soldier.is_moving:
    soldier.update(dt)
    total_time += dt
    current_pos = soldier.get_current_position()
    
    print(f"Time: {total_time:.2f}s | Progress: {soldier.movement_progress:.2f} | "
          f"Pos: ({current_pos[0]:.2f}, {current_pos[1]:.2f}) | "
          f"Animation: {soldier.current_animation}")
    
    # Safety check to prevent infinite loop
    if total_time > 10.0:
        print("ERROR: Movement taking too long!")
        break

# Check final state
print("\nFinal state after movement:")
print("-" * 60)
print(f"Position: {soldier.position}")
print(f"Is moving: {soldier.is_moving}")
print(f"Current animation: {soldier.current_animation}")
print(f"Movement completed successfully: {soldier.position == (5, 8)}")

# Test different distances
print("\n" + "=" * 60)
print("\nTesting movement with different distances:")
print("-" * 60)

test_cases = [
    ((0, 0), (0, 1), 1),   # 1 cell
    ((0, 0), (0, 3), 3),   # 3 cells
    ((0, 0), (2, 2), 4),   # 4 cells diagonal
]

for start, end, distance in test_cases:
    unit = Unit(unit_type="archer", team=0, position=start)
    unit.move_to(end)
    
    # Calculate expected time
    expected_time = distance / unit.speed
    
    print(f"\nMoving from {start} to {end} (distance: {distance})")
    print(f"  Expected time: {expected_time:.2f}s")
    
    # Simulate until completion
    time_taken = 0.0
    while unit.is_moving and time_taken < 10.0:
        unit.update(dt)
        time_taken += dt
    
    print(f"  Actual time: {time_taken:.2f}s")
    print(f"  Final position: {unit.position}")
    print(f"  Success: {unit.position == end}")

print("\n" + "=" * 60)
print("\nAll movement animation tests completed!")
