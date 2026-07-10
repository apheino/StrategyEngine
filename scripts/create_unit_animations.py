"""Script to create placeholder unit animation files"""
import pygame
import os

# Initialize Pygame
pygame.init()

# Animation settings
UNIT_SIZE = 64
FRAME_COUNT = {
    "idle": 2,
    "move": 4,
    "attack": 3,
    "death": 4
}

# Unit types to create
UNIT_TYPES = ["soldier", "archer", "knight"]

# Ensure resources/units directory exists
os.makedirs("resources/units", exist_ok=True)

# Team colors
TEAM_COLORS = {
    "soldier": (100, 150, 255),  # Blue
    "archer": (100, 255, 150),   # Green
    "knight": (200, 100, 255)    # Purple
}

def draw_unit_base(surface, unit_type, frame, animation):
    """Draw a simple unit representation"""
    base_color = TEAM_COLORS.get(unit_type, (150, 150, 150))
    
    # Clear surface
    surface.fill((0, 0, 0, 0))  # Transparent background
    
    if animation == "idle":
        # Pulsing effect for idle
        offset = 2 if frame % 2 == 0 else 0
        pygame.draw.circle(surface, base_color, 
                         (UNIT_SIZE // 2, UNIT_SIZE // 2 + offset), 
                         UNIT_SIZE // 3)
        # Draw a simple body
        pygame.draw.rect(surface, base_color,
                        (UNIT_SIZE // 3, UNIT_SIZE // 2,
                         UNIT_SIZE // 3, UNIT_SIZE // 3))
    
    elif animation == "move":
        # Moving legs animation
        leg_offset = (frame - 2) * 3 if frame < 2 else (4 - frame) * 3
        # Head
        pygame.draw.circle(surface, base_color, 
                         (UNIT_SIZE // 2, UNIT_SIZE // 3), 
                         UNIT_SIZE // 4)
        # Body
        pygame.draw.rect(surface, base_color,
                        (UNIT_SIZE // 3, UNIT_SIZE // 3,
                         UNIT_SIZE // 3, UNIT_SIZE // 2))
        # Legs (animated)
        pygame.draw.line(surface, base_color,
                        (UNIT_SIZE // 2, UNIT_SIZE - 10),
                        (UNIT_SIZE // 2 - leg_offset, UNIT_SIZE), 5)
        pygame.draw.line(surface, base_color,
                        (UNIT_SIZE // 2, UNIT_SIZE - 10),
                        (UNIT_SIZE // 2 + leg_offset, UNIT_SIZE), 5)
    
    elif animation == "attack":
        # Attack swing animation
        arm_angle = frame * 30
        # Head
        pygame.draw.circle(surface, base_color, 
                         (UNIT_SIZE // 2, UNIT_SIZE // 3), 
                         UNIT_SIZE // 4)
        # Body
        pygame.draw.rect(surface, base_color,
                        (UNIT_SIZE // 3, UNIT_SIZE // 3,
                         UNIT_SIZE // 3, UNIT_SIZE // 2))
        # Weapon (sword-like)
        weapon_color = (200, 200, 200)
        start_x = UNIT_SIZE // 2
        start_y = UNIT_SIZE // 2
        end_x = start_x + int(20 * (1 + frame * 0.5))
        end_y = start_y - int(10 * frame)
        pygame.draw.line(surface, weapon_color, (start_x, start_y), (end_x, end_y), 4)
    
    elif animation == "death":
        # Falling/fading animation
        alpha = 255 - (frame * 60)
        if alpha < 0:
            alpha = 0
        
        # Create surface with alpha
        temp_surface = pygame.Surface((UNIT_SIZE, UNIT_SIZE), pygame.SRCALPHA)
        
        # Falling/rotating
        rotation = frame * 22.5
        size = UNIT_SIZE // 3 - (frame * 3)
        if size > 0:
            pygame.draw.circle(temp_surface, (*base_color, alpha), 
                             (UNIT_SIZE // 2, UNIT_SIZE // 2 + frame * 5), 
                             size)
        
        surface.blit(temp_surface, (0, 0))
    
    # Add border for visibility
    pygame.draw.rect(surface, (50, 50, 50), (0, 0, UNIT_SIZE, UNIT_SIZE), 1)


def create_animation_frames(unit_type):
    """Create all animation frames for a unit type"""
    for animation, num_frames in FRAME_COUNT.items():
        for frame in range(num_frames):
            # Create surface with alpha channel
            surface = pygame.Surface((UNIT_SIZE, UNIT_SIZE), pygame.SRCALPHA)
            
            # Draw the unit
            draw_unit_base(surface, unit_type, frame, animation)
            
            # Add text label (for identification)
            font = pygame.font.Font(None, 12)
            text = font.render(f"{unit_type[0].upper()}", True, (255, 255, 255))
            text_rect = text.get_rect(topleft=(2, 2))
            surface.blit(text, text_rect)
            
            # Save the frame
            filename = f"resources/units/{unit_type}_{animation}_{frame}.png"
            pygame.image.save(surface, filename)
            print(f"Created {filename}")


# Create animations for all unit types
print("Creating unit animation placeholder files...\n")

for unit_type in UNIT_TYPES:
    print(f"Creating animations for {unit_type}:")
    create_animation_frames(unit_type)
    print()

print("Unit animation creation complete!")
print(f"\nCreated animations for: {', '.join(UNIT_TYPES)}")
print(f"Animation types: {', '.join(FRAME_COUNT.keys())}")
