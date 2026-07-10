"""Test unit attribute loading from files"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unit import Unit


def test_soldier_attributes():
    """Test that soldier attributes load correctly from soldier.txt"""
    soldier = Unit("soldier", team=0, position=(0, 0))
    
    assert soldier.max_health == 100, f"Expected max_health=100, got {soldier.max_health}"
    assert soldier.attack_power == 20, f"Expected attack_power=20, got {soldier.attack_power}"
    assert soldier.defense == 5, f"Expected defense=5, got {soldier.defense}"
    assert soldier.attack_range == 1, f"Expected attack_range=1, got {soldier.attack_range}"
    assert soldier.max_mobility == 3, f"Expected max_mobility=3, got {soldier.max_mobility}"
    assert soldier.speed == 2.0, f"Expected speed=2.0, got {soldier.speed}"
    
    print("✓ Soldier attributes loaded correctly")


def test_archer_attributes():
    """Test that archer attributes load correctly from archer.txt"""
    archer = Unit("archer", team=0, position=(0, 0))
    
    assert archer.max_health == 80, f"Expected max_health=80, got {archer.max_health}"
    assert archer.attack_power == 25, f"Expected attack_power=25, got {archer.attack_power}"
    assert archer.defense == 3, f"Expected defense=3, got {archer.defense}"
    assert archer.attack_range == 3, f"Expected attack_range=3, got {archer.attack_range}"
    assert archer.max_mobility == 4, f"Expected max_mobility=4, got {archer.max_mobility}"
    assert archer.speed == 2.5, f"Expected speed=2.5, got {archer.speed}"
    
    print("✓ Archer attributes loaded correctly")


def test_knight_attributes():
    """Test that knight attributes load correctly from knight.txt"""
    knight = Unit("knight", team=0, position=(0, 0))
    
    assert knight.max_health == 150, f"Expected max_health=150, got {knight.max_health}"
    assert knight.attack_power == 35, f"Expected attack_power=35, got {knight.attack_power}"
    assert knight.defense == 12, f"Expected defense=12, got {knight.defense}"
    assert knight.attack_range == 1, f"Expected attack_range=1, got {knight.attack_range}"
    assert knight.max_mobility == 2, f"Expected max_mobility=2, got {knight.max_mobility}"
    assert knight.speed == 1.8, f"Expected speed=1.8, got {knight.speed}"
    
    print("✓ Knight attributes loaded correctly")


def test_health_initialized():
    """Test that current health is set to max_health"""
    soldier = Unit("soldier", team=0, position=(0, 0))
    assert soldier.health == soldier.max_health, f"Expected health={soldier.max_health}, got {soldier.health}"
    
    archer = Unit("archer", team=0, position=(0, 0))
    assert archer.health == archer.max_health, f"Expected health={archer.max_health}, got {archer.health}"
    
    knight = Unit("knight", team=0, position=(0, 0))
    assert knight.health == knight.max_health, f"Expected health={knight.max_health}, got {knight.health}"
    
    print("✓ Health initialized correctly for all unit types")


def test_different_unit_stats():
    """Test that different unit types have different stats"""
    soldier = Unit("soldier", team=0, position=(0, 0))
    archer = Unit("archer", team=0, position=(0, 0))
    knight = Unit("knight", team=0, position=(0, 0))
    
    # Verify they have different stats
    assert soldier.max_health != knight.max_health, "Soldier and knight should have different health"
    assert soldier.attack_range != archer.attack_range, "Soldier and archer should have different range"
    assert knight.max_mobility != archer.max_mobility, "Knight and archer should have different mobility"
    
    print("✓ Different unit types have different stats")


if __name__ == "__main__":
    print("Testing unit attribute loading...\n")
    
    test_soldier_attributes()
    test_archer_attributes()
    test_knight_attributes()
    test_health_initialized()
    test_different_unit_stats()
    
    print("\n✅ All unit attribute tests passed!")
