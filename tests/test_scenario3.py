"""Test scenario 3 loading"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scenario import Scenario


def test_scenario_3_loading():
    """Test that scenario 3 with large map loads correctly"""
    print("Testing Scenario 3 (Large Battle Map)...")
    
    scenario = Scenario(scenario_number=3)
    
    # Verify map dimensions
    assert scenario.grid.grid_width == 200, f"Expected width 200, got {scenario.grid.grid_width}"
    assert scenario.grid.grid_height == 100, f"Expected height 100, got {scenario.grid.grid_height}"
    print(f"✓ Map dimensions: {scenario.grid.grid_width}x{scenario.grid.grid_height}")
    
    # Verify units loaded
    assert len(scenario.units) > 0, "No units loaded"
    print(f"✓ Units loaded: {len(scenario.units)}")
    
    # Count units by team
    player_units = [u for u in scenario.units if u.is_player_unit()]
    enemy_units = [u for u in scenario.units if u.is_enemy_unit()]
    print(f"  - Player units: {len(player_units)}")
    print(f"  - Enemy units: {len(enemy_units)}")
    
    # Count units by type
    unit_types = {}
    for unit in scenario.units:
        unit_types[unit.unit_type] = unit_types.get(unit.unit_type, 0) + 1
    
    for unit_type, count in sorted(unit_types.items()):
        print(f"  - {unit_type.capitalize()}: {count}")
    
    # Verify terrain variety
    terrain_counts = {0: 0, 1: 0, 2: 0}  # easy, slow, blocked
    for row in range(scenario.grid.grid_height):
        for col in range(scenario.grid.grid_width):
            passability = scenario.get_passability_at(row, col)
            if passability in terrain_counts:
                terrain_counts[passability] += 1
    
    total_cells = scenario.grid.grid_width * scenario.grid.grid_height
    print(f"\n✓ Terrain variety:")
    print(f"  - Easy passable: {terrain_counts[0]} ({terrain_counts[0]/total_cells*100:.1f}%)")
    print(f"  - Slow passable: {terrain_counts[1]} ({terrain_counts[1]/total_cells*100:.1f}%)")
    print(f"  - Blocked: {terrain_counts[2]} ({terrain_counts[2]/total_cells*100:.1f}%)")
    
    # Verify icons loaded
    icon_count = len([icon for icon in scenario.grid.icons.values() if icon is not None])
    print(f"\n✓ Icons loaded: {icon_count}")
    
    assert terrain_counts[1] > 0, "No slow passable terrain found"
    assert terrain_counts[2] > 0, "No blocked terrain found"
    print(f"\n✅ Scenario 3 loaded successfully!")


if __name__ == "__main__":
    test_scenario_3_loading()
