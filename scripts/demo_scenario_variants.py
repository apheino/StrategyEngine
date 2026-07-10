#!/usr/bin/env python3
"""Demo showing how to load different unit configurations for the same map"""
import sys
sys.path.insert(0, '.')

from scenario import Scenario

print("Demonstrating Scenario Variants\n")
print("=" * 60)

# Load map 1 with default units
print("\nScenario 1 - Standard Configuration:")
print("-" * 60)
scenario_standard = Scenario(scenario_number=1)
print(f"Total units: {len(scenario_standard.units)}")
print(f"Team 0: {len(scenario_standard.get_units_by_team(0))} units")
print(f"Team 1: {len(scenario_standard.get_units_by_team(1))} units")

print("\n" + "=" * 60)

# Load map 1 with tutorial units
print("\nScenario 1 - Tutorial Configuration:")
print("-" * 60)
scenario_tutorial = Scenario(scenario_number=1, units_file="units_1_tutorial.txt")
print(f"Total units: {len(scenario_tutorial.units)}")
print(f"Team 0: {len(scenario_tutorial.get_units_by_team(0))} units")
print(f"Team 1: {len(scenario_tutorial.get_units_by_team(1))} units")

print("\nUnit positions in tutorial:")
for unit in scenario_tutorial.units:
    print(f"  {unit}")

print("\n" + "=" * 60)
print("\nThis demonstrates how the same map can have different")
print("unit configurations for different difficulty levels,")
print("game modes, or scenarios!")
print("=" * 60)
