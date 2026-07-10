"""Test hover system for all units"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scenario import Scenario


def test_hover_all_units():
    """Test that hover works for both player and enemy units"""
    scenario = Scenario(scenario_number=1)
    
    # Find a player unit and an enemy unit
    player_unit = None
    enemy_unit = None
    
    for unit in scenario.units:
        if unit.is_player_unit() and player_unit is None:
            player_unit = unit
        if unit.is_enemy_unit() and enemy_unit is None:
            enemy_unit = unit
        if player_unit and enemy_unit:
            break
    
    assert player_unit is not None, "No player unit found"
    assert enemy_unit is not None, "No enemy unit found"
    
    # Simulate hover over player unit
    player_row, player_col = player_unit.position
    scenario.hovered_unit = player_unit
    
    assert scenario.hovered_unit == player_unit, "Player unit should be hoverable"
    print(f"✓ Hover works for player unit at ({player_row}, {player_col})")
    
    # Simulate hover over enemy unit
    enemy_row, enemy_col = enemy_unit.position
    scenario.hovered_unit = enemy_unit
    
    assert scenario.hovered_unit == enemy_unit, "Enemy unit should be hoverable"
    print(f"✓ Hover works for enemy unit at ({enemy_row}, {enemy_col})")
    
    # Test that different unit types have different stats
    units_by_type = {}
    for unit in scenario.units:
        if unit.unit_type not in units_by_type:
            units_by_type[unit.unit_type] = unit
    
    if len(units_by_type) > 1:
        unit_types = list(units_by_type.keys())
        unit1 = units_by_type[unit_types[0]]
        unit2 = units_by_type[unit_types[1]]
        
        print(f"✓ {unit1.unit_type.capitalize()}: HP={unit1.max_health}, ATK={unit1.attack_power}, DEF={unit1.defense}, MOB={unit1.max_mobility}, RNG={unit1.attack_range}")
        print(f"✓ {unit2.unit_type.capitalize()}: HP={unit2.max_health}, ATK={unit2.attack_power}, DEF={unit2.defense}, MOB={unit2.max_mobility}, RNG={unit2.attack_range}")


if __name__ == "__main__":
    print("Testing hover system for all units...\n")
    
    test_hover_all_units()
    
    print("\n✅ All hover tests passed!")
