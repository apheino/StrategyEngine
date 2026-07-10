#!/usr/bin/env python3
"""Test script for Unit class functionality"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unit import Unit

print("Testing Unit class:\n")

# Create a soldier unit
print("Creating a soldier unit:")
soldier = Unit(unit_type="soldier", team=0, position=(2, 3))
print(f"  {soldier}")
print(f"  Max Health: {soldier.max_health}")
print(f"  Attack Power: {soldier.attack_power}")
print(f"  Defense: {soldier.defense}")
print(f"  Mobility: {soldier.mobility}/{soldier.max_mobility}")
print(f"  Attack Range: {soldier.attack_range}")
print(f"  Animations loaded: {list(soldier.animations.keys())}")
print()

# Create an archer unit
print("Creating an archer unit:")
archer = Unit(unit_type="archer", team=1, position=(5, 5))
print(f"  {archer}")
print(f"  Animations loaded: {list(archer.animations.keys())}")
print()

# Test combat
print("Testing combat:")
print(f"  Archer health before: {archer.health}/{archer.max_health}")
damage = soldier.attack(archer)
print(f"  Soldier attacks archer for {damage} damage")
print(f"  Archer health after: {archer.health}/{archer.max_health}")
print(f"  Archer still alive: {archer.is_alive}")
print()

# Test movement
print("Testing movement:")
print(f"  Soldier position before: {soldier.position}")
soldier.move_to((3, 4))
print(f"  Soldier position after: {soldier.position}")
print(f"  Current animation: {soldier.current_animation}")
print()

# Test healing
print("Testing healing:")
print(f"  Archer health before heal: {archer.health}/{archer.max_health}")
archer.heal(30)
print(f"  Archer health after heal: {archer.health}/{archer.max_health}")
print()

# Test death
print("Testing death scenario:")
knight = Unit(unit_type="knight", team=0, position=(1, 1))
print(f"  Created knight: {knight}")
print(f"  Knight health: {knight.health}")
print(f"  Dealing lethal damage...")
for i in range(6):
    damage = knight.take_damage(20)
    print(f"    Took {damage} damage, health now: {knight.health}")
print(f"  Knight alive: {knight.is_alive}")
print(f"  Current animation: {knight.current_animation}")
print()

# Animation frame counts
print("Animation frame counts:")
for unit_type in ["soldier", "archer", "knight"]:
    test_unit = Unit(unit_type=unit_type, team=0, position=(0, 0))
    for anim_name, frames in test_unit.animations.items():
        print(f"  {unit_type} {anim_name}: {len(frames)} frames")
print()

print("All tests completed successfully!")
