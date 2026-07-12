# Tests

This directory contains all test files for Combat Alley 2000.

## Running Tests

To run tests from the project root:

```bash
# Run individual tests
python tests/test_unit.py
python tests/test_scenario.py
python tests/test_movement.py

# Run all unit tests
python -m pytest tests/  # If pytest is installed

# Visual tests (requires display)
python tests/test_health_bar_visual.py
```

## Test Files

### Unit Tests
- **test_unit.py** - Unit class functionality
- **test_unit_attributes.py** - Unit attribute loading from files
- **test_health_bars.py** - Health bar rendering

### System Tests
- **test_scenario.py** - Scenario loading and management
- **test_grid_size.py** - Dynamic grid sizing
- **test_movement.py** - Movement validation system
- **test_animation_movement.py** - Animated movement system
- **test_hover_system.py** - Unit hover tooltip system

### Visual Tests
- **test_health_bar_visual.py** - Visual verification of health bars at different levels

## Adding New Tests

Test files should:
1. Import required modules using the correct parent path
2. Follow the naming convention `test_*.py`
3. Include docstrings describing what is being tested
4. Print clear success/failure messages
