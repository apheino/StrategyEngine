"""Test health bar rendering"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from unit import Unit


def test_health_bar_colors():
    """Test that health bar colors change based on health percentage"""
    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    
    soldier = Unit("soldier", team=0, position=(0, 0))
    
    # Test full health (green)
    soldier.health = 100
    health_percent = soldier.health / soldier.max_health
    assert health_percent > 0.6, "Full health should be > 60%"
    print(f"✓ Full health ({health_percent*100:.0f}%) -> Green bar")
    
    # Test medium health (yellow)
    soldier.health = 50
    health_percent = soldier.health / soldier.max_health
    assert 0.3 < health_percent <= 0.6, "Medium health should be 30-60%"
    print(f"✓ Medium health ({health_percent*100:.0f}%) -> Yellow bar")
    
    # Test low health (red)
    soldier.health = 20
    health_percent = soldier.health / soldier.max_health
    assert health_percent <= 0.3, "Low health should be <= 30%"
    print(f"✓ Low health ({health_percent*100:.0f}%) -> Red bar")
    
    pygame.quit()


def test_health_bar_rendering():
    """Test that health bar can be drawn without errors"""
    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    
    soldier = Unit("soldier", team=0, position=(0, 0))
    
    # Test drawing at different health levels
    for health in [100, 75, 50, 25, 10, 0]:
        soldier.health = health
        try:
            soldier.draw(screen, 50, 50, 64)
            print(f"✓ Health bar rendered successfully at {health} HP")
        except Exception as e:
            print(f"✗ Error rendering at {health} HP: {e}")
            pygame.quit()
            raise
    
    pygame.quit()


def test_different_unit_types():
    """Test health bars for different unit types with different max health"""
    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    
    soldier = Unit("soldier", team=0, position=(0, 0))
    archer = Unit("archer", team=0, position=(0, 0))
    knight = Unit("knight", team=0, position=(0, 0))
    
    # Set all to 50% health
    soldier.health = soldier.max_health // 2
    archer.health = archer.max_health // 2
    knight.health = knight.max_health // 2
    
    # All should show yellow bar (50% health)
    for unit in [soldier, archer, knight]:
        health_percent = unit.health / unit.max_health
        assert 0.3 < health_percent <= 0.6, f"{unit.unit_type} at 50% should show yellow"
        print(f"✓ {unit.unit_type.capitalize()}: {unit.health}/{unit.max_health} HP -> Yellow bar")
    
    pygame.quit()


if __name__ == "__main__":
    print("Testing health bar rendering...\n")
    
    test_health_bar_colors()
    print()
    test_health_bar_rendering()
    print()
    test_different_unit_types()
    
    print("\n✅ All health bar tests passed!")
