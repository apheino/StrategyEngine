#!/usr/bin/env python3
"""Test script for player unit movement system"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scenario import Scenario
from grid import PASSABLE_EASY, PASSABLE_SLOW, PASSABLE_BLOCKED

print("Testing Player Unit Movement System\n")
print("=" * 60)

# Load scenario
print("\nLoading Scenario 1:")
print("-" * 60)
scenario = Scenario(scenario_number=1)

# Test team identification
print("\nTesting team identification:")
print("-" * 60)
player_units = scenario.get_units_by_team(0)
enemy_units = scenario.get_units_by_team(1)
print(f"Player units (team 0): {len(player_units)}")
print(f"Enemy units (team 1): {len(enemy_units)}")

for unit in player_units[:2]:
    print(f"  {unit.unit_type} is_player: {unit.is_player_unit()}, is_enemy: {unit.is_enemy_unit()}")

for unit in enemy_units[:2]:
    print(f"  {unit.unit_type} is_player: {unit.is_player_unit()}, is_enemy: {unit.is_enemy_unit()}")

# Test passability checking
print("\nTesting passability at various positions:")
print("-" * 60)
test_positions = [(0, 0), (1, 1), (5, 5), (9, 9)]
for row, col in test_positions:
    passability = scenario.get_passability_at(row, col)
    pass_name = "EASY" if passability == PASSABLE_EASY else ("SLOW" if passability == PASSABLE_SLOW else "BLOCKED")
    print(f"  Position ({row},{col}): {pass_name}")

# Test unit selection
print("\nTesting unit selection:")
print("-" * 60)
print(f"Current turn: {'Player' if scenario.current_turn == 0 else 'Enemy'}")

# Try to select a player unit
player_unit = player_units[0]
row, col = player_unit.position
print(f"\nAttempting to select player {player_unit.unit_type} at {row},{col}")
success = scenario.select_unit(row, col)
print(f"  Selection successful: {success}")
print(f"  Selected unit: {scenario.selected_unit}")
print(f"  Valid moves: {len(scenario.valid_moves)}")

# Show some valid moves
if scenario.valid_moves:
    print(f"  First 5 valid moves: {scenario.valid_moves[:5]}")

# Test movement calculation
print("\nTesting movement calculation:")
print("-" * 60)
for unit in player_units[:2]:
    valid_moves = scenario.calculate_valid_moves(unit)
    print(f"  {unit.unit_type} at {unit.position}: {len(valid_moves)} valid moves (mobility: {unit.mobility})")

# Test movement attempt
print("\nTesting movement:")
print("-" * 60)
if scenario.selected_unit and scenario.valid_moves:
    original_pos = scenario.selected_unit.position
    destination = scenario.valid_moves[0]
    
    print(f"Moving {scenario.selected_unit.unit_type} from {original_pos} to {destination}")
    success = scenario.attempt_move_unit(*destination)
    print(f"  Move successful: {success}")
    
    if success:
        # Check unit moved
        unit_at_dest = scenario.get_unit_at(*destination)
        print(f"  Unit at destination: {unit_at_dest.unit_type if unit_at_dest else 'None'}")
        print(f"  Unit is_active after move: {player_units[0].is_active}")

# Test turn system
print("\nTesting turn system:")
print("-" * 60)
print(f"Current turn before end: {'Player' if scenario.current_turn == 0 else 'Enemy'}")
print("Ending turn...")
scenario.end_turn()
print(f"Current turn after end: {'Player' if scenario.current_turn == 0 else 'Enemy'}")

# Check units were reset
print(f"\nPlayer units active status after turn:")
for unit in player_units[:2]:
    print(f"  {unit.unit_type}: is_active={unit.is_active}, mobility={unit.mobility}")

print("\n" + "=" * 60)
print("All movement system tests completed!")
