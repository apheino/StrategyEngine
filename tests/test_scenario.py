#!/usr/bin/env python3
"""Test script for Scenario loading system"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scenario import Scenario

print("Testing Scenario Loading System\n")
print("=" * 60)

# Test Scenario 1
print("\nLoading Scenario 1:")
print("-" * 60)
scenario1 = Scenario(scenario_number=1)
print(f"Map size: {scenario1.grid.grid_height}x{scenario1.grid.grid_width}")
print(f"Total units: {len(scenario1.units)}")

# Count units by team
team0_units = scenario1.get_units_by_team(0)
team1_units = scenario1.get_units_by_team(1)
print(f"Team 0 (Blue) units: {len(team0_units)}")
print(f"Team 1 (Red) units: {len(team1_units)}")

# List all units
print("\nUnit positions:")
for unit in scenario1.units:
    print(f"  {unit}")

# Test unit lookup
print("\nTesting unit lookup at specific positions:")
test_positions = [(7, 3), (1, 4), (5, 5)]
for row, col in test_positions:
    unit = scenario1.get_unit_at(row, col)
    if unit:
        print(f"  Position ({row},{col}): {unit.unit_type} (Team {unit.team})")
    else:
        print(f"  Position ({row},{col}): Empty")

print("\n" + "=" * 60)

# Test Scenario 2
print("\nLoading Scenario 2:")
print("-" * 60)
scenario2 = Scenario(scenario_number=2)
print(f"Map size: {scenario2.grid.grid_height}x{scenario2.grid.grid_width}")
print(f"Total units: {len(scenario2.units)}")

# Count units by team
team0_units = scenario2.get_units_by_team(0)
team1_units = scenario2.get_units_by_team(1)
print(f"Team 0 (Blue) units: {len(team0_units)}")
print(f"Team 1 (Red) units: {len(team1_units)}")

# List all units
print("\nUnit positions:")
for unit in scenario2.units:
    print(f"  {unit}")

print("\n" + "=" * 60)

# Test non-existent scenario
print("\nLoading non-existent Scenario 99:")
print("-" * 60)
scenario99 = Scenario(scenario_number=99)
print(f"Units loaded: {len(scenario99.units)}")

print("\n" + "=" * 60)
print("\nAll scenario loading tests completed!")
