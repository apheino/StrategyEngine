# Scripts

This directory contains utility and setup scripts for the strategy game project.

## Files

### Asset Creation
- **create_icons.py** - Generate placeholder terrain icon files
- **create_unit_animations.py** - Generate placeholder unit animation frames

### Demo Scripts
- **demo_scenario_variants.py** - Demonstrate different scenario configurations
- **demo_units.py** - Demonstrate unit system features

## Usage

Run scripts from the project root:

```bash
# Generate terrain icons
python scripts/create_icons.py

# Generate unit animation frames
python scripts/create_unit_animations.py

# Run demos
python scripts/demo_units.py
python scripts/demo_scenario_variants.py
```

## Creating New Scripts

Utility scripts should:
1. Be placed in this directory
2. Include clear docstrings
3. Print progress/status messages
4. Handle errors gracefully
