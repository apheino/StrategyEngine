"""
Main game loop and entry point for the strategy game

This is the main module that initializes Pygame, sets up the game window,
and runs the main game loop. It handles:
- Event processing (mouse, keyboard)
- Game state updates
- Rendering all game elements
- FPS management

The game loop follows the standard pattern:
1. Process events (handle_events)
2. Update game state (update)
3. Render everything (draw)
"""

import pygame
import sys
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    BLACK,
    WHITE,
    GRAY,
    LIGHT_GRAY,
    BLUE
)
from scenario import Scenario


# ============================================================================
# PYGAME INITIALIZATION
# ============================================================================

# Initialize Pygame subsystems (display, sound, etc.)
pygame.init()

# Setup display window
# pygame.NOFRAME creates a window without title bar and borders
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Strategy Game")

# Clock for managing frame rate and delta time
clock = pygame.time.Clock()


# ============================================================================
# FONT SETUP
# ============================================================================

# Font for large text (turn indicator, FPS counter)
font = pygame.font.Font(None, 36)

# Font for small text (instructions, unit info)
small_font = pygame.font.Font(None, 24)


# ============================================================================
# SCENARIO SETUP
# ============================================================================

# Load scenario (combines map and unit placement)
# scenario_number: 1 = small tutorial map, 2 = medium map, 3 = large battle
# cell_size: Base size of each grid cell in pixels (64 = standard)
scenario = Scenario(scenario_number=2, cell_size=64)

# Auto-scale map to fit screen height on startup
# This ensures the map is visible without needing to zoom out manually
scenario.grid.scale_to_screen_height(SCREEN_HEIGHT)

 
# ============================================================================
# EVENT HANDLING
# ============================================================================

def handle_events():
    """
    Process all input events from mouse and keyboard
    
    This function handles:
    - Window close events (X button)
    - Keyboard input (ESC to quit, SPACE to end turn, G to toggle grid)
    - Mouse events (click to select/move, drag to pan, wheel to zoom)
    
    The function distinguishes between clicks (for unit selection) and drags
    (for panning) using a threshold system. Grid handles pan/zoom internally.
    
    Returns:
        bool: True to continue running, False to quit the game
    """
    for event in pygame.event.get():
        # Window close button clicked
        if event.type == pygame.QUIT:
            return False
        
        # Keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # ESC key - quit game
                return False
            elif event.key == pygame.K_SPACE:
                # SPACE key - end current player's turn
                scenario.end_turn()
            elif event.key == pygame.K_h:
                # H key - toggle damage numbers display
                scenario.show_combat_messages = not scenario.show_combat_messages
                status = "ON" if scenario.show_combat_messages else "OFF"
                print(f"Damage numbers display: {status}")
            elif event.key == pygame.K_s:
                # S key - toggle fog of war
                scenario.fog_of_war_enabled = not scenario.fog_of_war_enabled
                status = "ON" if scenario.fog_of_war_enabled else "OFF"
                print(f"Fog of war: {status}")
        
        # Pass ALL events to grid for pan/zoom tracking
        # Grid needs to track mouse down/move/up for drag detection
        scenario.grid.handle_event(event, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Handle unit selection and movement
        # Only process on mouse button RELEASE (not press) to avoid
        # triggering selection during drag operations
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button released
                # Check if this was a click or a drag
                # is_dragging() returns True if mouse moved > threshold
                if not scenario.grid.is_dragging():
                    # This was a click, not a drag - handle unit interaction
                    mouse_x, mouse_y = event.pos
                    
                    # Convert screen coordinates to grid coordinates
                    grid_pos = scenario.screen_to_grid(mouse_x, mouse_y, SCREEN_WIDTH, SCREEN_HEIGHT)
                    
                    if grid_pos:
                        row, col = grid_pos
                        # Let scenario handle the click (select unit, move, or attack)
                        scenario.handle_click(row, col)
    
    return True


# ============================================================================
# GAME LOGIC UPDATE
# ============================================================================

def update(dt):
    """
    Update game state for one frame
    
    Updates all game logic including:
    - Unit animations and movement
    - Projectile movement
    - Hover detection for tooltips
    
    Args:
        dt (float): Delta time in seconds since last frame
    """
    # Update all units, projectiles, and game logic
    scenario.update(dt)
    
    # Update which unit (if any) the mouse is hovering over
    # This is needed for displaying unit tooltips
    mouse_x, mouse_y = pygame.mouse.get_pos()
    scenario.update_hover(mouse_x, mouse_y, SCREEN_WIDTH, SCREEN_HEIGHT)


# ============================================================================
# RENDERING
# ============================================================================

def draw(fps):
    """
    Render all game elements to the screen
    
    Drawing order (back to front):
    1. Background color
    2. Map terrain
    3. Selection highlights (valid moves and attacks)
    4. Units with health bars
    5. Projectiles
    6. UI overlays (turn indicator, instructions, hover info, FPS)
    
    Args:
        fps (float): Current frames per second for FPS counter display
    """
    # Clear screen with background color (deep blue like ocean)
    screen.fill(BLUE)
    
    # ========================================
    # GAME WORLD RENDERING
    # ========================================
    
    # Draw terrain tiles
    scenario.draw_map(screen)
    
    # Draw fog of war overlay on unseen cells
    scenario.draw_fog_of_war(screen)
    
    # Draw selection highlights (green for valid moves, red for valid attacks)
    scenario.draw_selection_highlights(screen)
    
    # Draw all units with their animations and health bars
    scenario.draw_units(screen)
    
    # Draw projectiles in flight
    scenario.draw_projectiles(screen)
    
    # Draw combat messages (damage numbers)
    scenario.draw_combat_messages(screen, small_font, scenario.grid.cell_size, scenario.grid.zoom, 
                                  scenario.grid.offset_x, scenario.grid.offset_y)
    
    # ========================================
    # UI OVERLAY RENDERING
    # ========================================
    
    # Turn indicator in top-left corner
    # Shows whose turn it is with color coding
    turn_name = "Player Turn" if scenario.current_turn == 0 else "Enemy Turn"
    turn_color = (100, 255, 100) if scenario.current_turn == 0 else (255, 100, 100)
    turn_text = font.render(turn_name, True, turn_color)
    screen.blit(turn_text, (10, 10))
    
    # Instructions panel (below turn indicator)
    # Lists all available controls
    instructions = [
        "Click unit to select",
        "Click green cell to move",
        "Drag to pan map",
        "Hover for unit info",
        "SPACE: End turn",
        "H: Toggle damage #s",
        "S: Toggle fog of war",
        "G: Toggle grid"
    ]
    for i, text in enumerate(instructions):
        inst_text = small_font.render(text, True, LIGHT_GRAY)
        screen.blit(inst_text, (10, 50 + i * 25))
    
    # Selected unit info bar (bottom of screen)
    # Shows stats for currently selected player unit
    if scenario.selected_unit:
        unit = scenario.selected_unit
        effective_attack = unit.get_effective_attack_power()
        effective_mobility = unit.get_effective_mobility()
        effective_projectiles = unit.get_effective_projectile_count()
        
        # Show total damage for multi-projectile units
        if effective_projectiles > 1:
            total_damage = effective_attack * effective_projectiles
            attack_display = f"{effective_attack}x{effective_projectiles}={total_damage}"
        else:
            attack_display = str(effective_attack)
        
        info_text = small_font.render(
            f"Selected: {unit.unit_type} | HP: {unit.health}/{unit.max_health} | ATK: {attack_display} | MOB: {unit.mobility}/{effective_mobility}",
            True, (255, 255, 100)  # Yellow text
        )
        screen.blit(info_text, (10, SCREEN_HEIGHT - 30))
    
    # Hover tooltip (shows when mouse is over any unit)
    # Displays unit stats with team-colored border
    scenario.draw_hover_info(screen, small_font)
    
    # FPS counter in upper-right corner
    # Useful for performance monitoring
    fps_text = font.render(f"FPS: {int(fps)}", True, LIGHT_GRAY)
    fps_rect = fps_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    screen.blit(fps_text, fps_rect)
    
    # Update display (flip buffers)
    pygame.display.flip()


# ============================================================================
# MAIN GAME LOOP
# ============================================================================

def main():
    """
    Main game loop
    
    Implements the standard game loop pattern:
    1. Calculate delta time (time since last frame)
    2. Handle events (input processing)
    3. Update game state (physics, animations, logic)
    4. Render everything (draw to screen)
    
    The loop runs at the target FPS (60) until the user quits.
    Delta time is used to make updates frame-rate independent.
    """
    running = True
    
    while running:
        # Calculate delta time in seconds
        # clock.tick(FPS) limits frame rate and returns milliseconds elapsed
        dt = clock.tick(FPS) / 1000.0
        
        # Get actual FPS for display
        # This may differ from target FPS if game is running slow
        actual_fps = clock.get_fps()
        
        # Process input events
        # Returns False if user wants to quit
        running = handle_events()
        
        # Update game state with delta time
        update(dt)
        
        # Render everything to screen
        draw(actual_fps)
    
    # Cleanup: shutdown Pygame and exit
    pygame.quit()
    sys.exit()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Start the game when script is run directly
    main()
