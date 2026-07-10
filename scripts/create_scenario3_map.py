"""Generate large scenario 3 map with varied terrain"""
import random

# Map dimensions
WIDTH = 200
HEIGHT = 100

def generate_map():
    """Generate a 200x100 map with varied terrain"""
    map_data = []
    
    # Header comment
    map_data.append("# Scenario 3 - Large Battle Map (200x100)")
    map_data.append("# Icon 1 = Sand/Shoreline (easy passing)")
    map_data.append("# Icon 2 = Grassland (easy passing)")
    map_data.append("# Icon 3 = Swamp/Rough Terrain (slow passing)")
    map_data.append("# Icon 4 = Mountain/Water (blocked)")
    map_data.append("")
    
    # Generate terrain
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            # Create some terrain patterns
            
            # Border mountains (20% of the time on edges)
            if (x == 0 or x == WIDTH-1 or y == 0 or y == HEIGHT-1) and random.random() < 0.2:
                cell = "4,2"  # Mountain, blocked
            
            # Scattered mountain ranges (create clusters)
            elif ((x // 20) + (y // 15)) % 7 == 0 and random.random() < 0.4:
                cell = "4,2"  # Mountain, blocked
            
            # Swamp/rough areas (create zones)
            elif ((x // 15) + (y // 10)) % 5 == 0 and random.random() < 0.5:
                cell = "3,1"  # Swamp, slow
            
            # Rivers (horizontal and vertical lines)
            elif (y % 25 == 10 or y % 25 == 11) and x % 3 != 0:
                cell = "4,2"  # Water, blocked
            elif (x % 40 == 20 or x % 40 == 21) and y % 3 != 0:
                cell = "4,2"  # Water, blocked
            
            # Random scattered obstacles
            elif random.random() < 0.05:
                if random.random() < 0.5:
                    cell = "3,1"  # Swamp, slow
                else:
                    cell = "4,2"  # Mountain, blocked
            
            # Sandy/beach areas near borders
            elif x < 10 or x >= WIDTH-10 or y < 10 or y >= HEIGHT-10:
                cell = "1,0"  # Sand, easy
            
            # Default grassland
            else:
                cell = "2,0"  # Grass, easy
            
            row.append(cell)
        
        map_data.append(" ".join(row))
    
    return "\n".join(map_data)

if __name__ == "__main__":
    print("Generating large map for scenario 3...")
    map_content = generate_map()
    
    with open("resources/maps/map_3.txt", "w") as f:
        f.write(map_content)
    
    print(f"✓ Generated map_3.txt: 200x100 grid")
    print(f"  - Total cells: {200*100}")
    print(f"  - Terrain types: Sand, Grass, Swamp, Mountain/Water")
    print(f"  - File size: {len(map_content)} bytes")
