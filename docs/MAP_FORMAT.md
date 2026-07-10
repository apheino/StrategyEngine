# Map Definition Format

## File Organization

Maps are stored in `resources/maps/` as `map_n.txt` where `n` is the map number (e.g., `map_1.txt`, `map_2.txt`).

Icons are stored in `resources/icons/` as `icon_n.png` or `icon_n.bmp` files.

**Note**: Unit placement is handled separately in `units_n.txt` files. See [UNITS_FORMAT.md](UNITS_FORMAT.md) for details.

## Format Specification

Each line in the map file represents one row of the grid.
Each cell is defined as: `icon_id,passability`

The grid size is automatically determined from the map file:
- Number of rows = number of non-empty, non-comment lines
- Number of columns = number of cells in the first row
- Grid does not need to be square (can be rectangular)

### Cell Definition
- **icon_id**: Integer identifying which icon to use (references `icon_n.png` or `icon_n.bmp`)
- **passability**: Integer defining movement type:
  - `0` = Easy passing (normal movement speed)
  - `1` = Slow passing (reduced movement speed)
  - `2` = Not passable (blocked, cannot enter)

### Format Rules
- Cells within a row are separated by spaces
- Rows are separated by newlines
- Lines starting with `#` are comments and are ignored
- Empty lines are ignored
- If passability is omitted, defaults to 0 (easy passing)

## Example

```
# Example 3x3 map
# Icon 1 = Water (not passable)
# Icon 2 = Grass (easy passing)
# Icon 3 = Mud (slow passing)

1,2 1,2 1,2
1,2 2,0 3,1
1,2 2,0 2,0
```

This creates a 3x3 map where:
- Top row and left column are water (blocked)
- Center and bottom-right are grass (easy)
- Middle-right is mud (slow)

## Icon Files

Icons are loaded from `resources/icons/` directory:
- Tries `icon_n.png` first
- Falls back to `icon_n.bmp` if PNG not found
- Icons should be 64x64 pixels
- If icon file not found, a gray placeholder is displayed

## Current Map 1

`resources/maps/map_1.txt` defines a 10x10 grid:
- Icon 1 (Shoreline/Sand): Used for edge cells - all easy passing
- Icon 2 (Grassland/Green): Used for interior cells - all easy passing
