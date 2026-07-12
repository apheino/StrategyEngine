"""
Main game loop and entry point for Combat Alley 2000

This is the main module that initializes Pygame, sets up the game window,
and runs the main game loop. It handles:
- Event processing (mouse, keyboard)
- Game state updates (menus, story, gameplay)
- Rendering all game elements
- FPS management
- State machine for menu/story/game flow

The game loop follows the standard pattern:
1. Process events (handle_events)
2. Update game state (update)
3. Render everything (draw)
"""

import pygame
import sys
import json
from enum import Enum
from pathlib import Path
from config import game_config
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
# GAME STATE ENUM
# ============================================================================

class GameState(Enum):
    """Enum for different game states in the state machine"""
    MAIN_MENU = 1
    STORY_SCREEN = 2
    PLAYING = 3
    VICTORY = 4
    DEFEAT = 5
    SCENARIO_SELECT = 6


# ============================================================================
# PYGAME INITIALIZATION
# ============================================================================

# Initialize Pygame subsystems (display, sound, etc.)
pygame.init()

# Setup display window
# Use configuration for window size and title
window_width, window_height = game_config.get_window_size()
screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
pygame.display.set_caption(game_config.get_game_name())

# Clock for managing frame rate and delta time
clock = pygame.time.Clock()

# Store window dimensions for easy access
SCREEN_WIDTH = window_width
SCREEN_HEIGHT = window_height


# ============================================================================
# FONT SETUP
# ============================================================================

# Font for large text (titles, turn indicator)
font = pygame.font.Font(None, game_config.get_font_size('large_size'))

# Font for medium text (menu items)
medium_font = pygame.font.Font(None, game_config.get_font_size('medium_size'))

# Font for small text (instructions, unit info)
small_font = pygame.font.Font(None, game_config.get_font_size('small_size'))


# ============================================================================
# GAME STATE MANAGEMENT
# ============================================================================

# Current game state
current_state = GameState.MAIN_MENU

# Scenario and story tracking
scenario = None
current_scenario_number = 1
current_story = None
is_campaign_mode = False  # True for campaign, False for skirmish

# Menu state
menu_buttons = []
selected_menu_item = 0


# ============================================================================
# STORY LOADING
# ============================================================================

def load_story(scenario_number):
    """
    Load story data from JSON file for a given scenario
    
    Args:
        scenario_number (int): Scenario number to load
        
    Returns:
        dict: Story data or None if file not found
    """
    story_file = Path(f"resources/stories/scenario_{scenario_number}.json")
    if story_file.exists():
        with open(story_file, 'r') as f:
            return json.load(f)
    return None


def get_victory_condition():
    """
    Check if player has won the current scenario
    
    Uses team configuration to determine which teams are player-controlled.
    Victory = all non-player teams have been eliminated.
    
    Returns:
        bool: True if all enemy units are defeated
    """
    if not scenario:
        return False
    
    # Get all non-player controlled teams
    enemy_team_ids = [t['id'] for t in game_config.get_teams() if not t.get('player_controlled', False)]
    
    # Check if all enemy teams are eliminated
    for team_id in enemy_team_ids:
        if any(u.team == team_id and u.is_alive for u in scenario.units):
            return False
    
    return True


def get_defeat_condition():
    """
    Check if player has lost the current scenario
    
    Uses team configuration to determine which teams are player-controlled.
    Defeat = all player teams have been eliminated.
    
    Returns:
        bool: True if all player units are defeated
    """
    if not scenario:
        return False
    
    # Get all player-controlled teams
    player_team_ids = [t['id'] for t in game_config.get_teams() if t.get('player_controlled', False)]
    
    # Check if all player teams are eliminated
    for team_id in player_team_ids:
        if any(u.team == team_id and u.is_alive for u in scenario.units):
            return False
    
    return True


# ============================================================================
# MENU FUNCTIONS
# ============================================================================

def init_main_menu():
    """Initialize main menu buttons"""
    global menu_buttons, selected_menu_item
    menu_buttons = [
        {"text": "New Campaign", "action": "campaign"},
        {"text": "Skirmish", "action": "skirmish"},
        {"text": "Quit", "action": "quit"}
    ]
    selected_menu_item = 0


def init_scenario_select_menu():
    """Initialize scenario selection menu"""
    global menu_buttons, selected_menu_item
    menu_buttons = [
        {"text": "Scenario 1: The First Battle", "action": "scenario_1"},
        {"text": "Scenario 2: The Narrow Valley", "action": "scenario_2"},
        {"text": "Scenario 3: The Great Plains", "action": "scenario_3"},
        {"text": "Back to Main Menu", "action": "main_menu"}
    ]
    selected_menu_item = 0


def init_victory_menu():
    """Initialize victory screen menu"""
    global menu_buttons, selected_menu_item
    buttons = []
    
    # Check if there's a next scenario in campaign mode
    if is_campaign_mode and current_story and current_story.get('next_scenario'):
        buttons.append({"text": "Continue Campaign", "action": "next_scenario"})
    
    buttons.extend([
        {"text": "Replay Scenario", "action": "replay"},
        {"text": "Main Menu", "action": "main_menu"}
    ])
    
    menu_buttons = buttons
    selected_menu_item = 0


def init_defeat_menu():
    """Initialize defeat screen menu"""
    global menu_buttons, selected_menu_item
    menu_buttons = [
        {"text": "Retry", "action": "replay"},
        {"text": "Main Menu", "action": "main_menu"}
    ]
    selected_menu_item = 0


def start_scenario(scenario_number, campaign_mode=False):
    """
    Start a scenario
    
    Args:
        scenario_number (int): Scenario number to load
        campaign_mode (bool): True if playing campaign, False for skirmish
    """
    global scenario, current_scenario_number, current_story, is_campaign_mode, current_state
    
    current_scenario_number = scenario_number
    is_campaign_mode = campaign_mode
    
    # Load story if in campaign mode
    if campaign_mode:
        current_story = load_story(scenario_number)
        current_state = GameState.STORY_SCREEN
    else:
        current_story = None
        # Load scenario directly
        scenario = Scenario(scenario_number=scenario_number, cell_size=64)
        scenario.grid.scale_to_screen_height(SCREEN_HEIGHT)
        current_state = GameState.PLAYING


# ============================================================================
# MENU RENDERING
# ============================================================================

def get_menu_button_at_mouse(mouse_pos, buttons, button_start_y=200, button_spacing=60):
    """
    Get the index of the menu button at the mouse position
    
    Args:
        mouse_pos (tuple): (x, y) mouse position
        buttons (list): List of button dicts
        button_start_y (int): Y position of first button
        button_spacing (int): Vertical spacing between buttons
        
    Returns:
        int: Button index or -1 if no button at position
    """
    mouse_x, mouse_y = mouse_pos
    
    for i, button in enumerate(buttons):
        button_y = button_start_y + i * button_spacing
        # Create a rough hit box around the button text
        # Approximate button height and width
        button_height = 40
        button_width = len(button['text']) * 20  # Rough estimate
        
        button_left = SCREEN_WIDTH // 2 - button_width // 2
        button_right = SCREEN_WIDTH // 2 + button_width // 2
        button_top = button_y - button_height // 2
        button_bottom = button_y + button_height // 2
        
        if (button_left <= mouse_x <= button_right and 
            button_top <= mouse_y <= button_bottom):
            return i
    
    return -1


def draw_menu(title, buttons, selected_index):
    """
    Draw a menu screen with title and buttons
    
    Args:
        title (str): Menu title
        buttons (list): List of button dicts with 'text' keys
        selected_index (int): Index of currently selected button
    """
    screen.fill(BLUE)
    
    # Draw title
    title_surf = font.render(title, True, WHITE)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_surf, title_rect)
    
    # Get mouse position for hover detection
    mouse_pos = pygame.mouse.get_pos()
    hovered_index = get_menu_button_at_mouse(mouse_pos, buttons)
    
    # Draw buttons
    button_start_y = 200
    button_spacing = 60
    
    for i, button in enumerate(buttons):
        # Highlight if selected by keyboard or hovered by mouse
        if i == selected_index or i == hovered_index:
            color = (255, 255, 100)  # Yellow for selected/hovered
            text = f"> {button['text']} <"
        else:
            color = WHITE
            text = button['text']
        
        button_surf = medium_font.render(text, True, color)
        button_rect = button_surf.get_rect(center=(SCREEN_WIDTH // 2, button_start_y + i * button_spacing))
        screen.blit(button_surf, button_rect)
    
    # Draw controls hint
    hint = "Arrow keys or mouse to navigate, ENTER or click to select, ESC to quit"
    hint_surf = small_font.render(hint, True, LIGHT_GRAY)
    hint_rect = hint_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    screen.blit(hint_surf, hint_rect)


def draw_story_screen():
    """Draw story/intro screen for current scenario"""
    screen.fill(BLUE)
    
    if not current_story:
        return
    
    # Draw title
    title = current_story.get('title', f'Scenario {current_scenario_number}')
    title_surf = font.render(title, True, WHITE)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title_surf, title_rect)
    
    # Draw horizontal line
    pygame.draw.line(screen, WHITE, (100, 120), (SCREEN_WIDTH - 100, 120), 2)
    
    # Draw intro text
    intro_lines = current_story.get('intro_text', [])
    y_offset = 180
    for line in intro_lines:
        if line:  # Skip empty lines but preserve spacing
            text_surf = small_font.render(line, True, WHITE)
        else:
            text_surf = small_font.render(" ", True, WHITE)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(text_surf, text_rect)
        y_offset += 30
    
    # Draw continue prompt
    prompt = "Press ENTER to begin, ESC for main menu"
    prompt_surf = medium_font.render(prompt, True, (255, 255, 100))
    prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
    screen.blit(prompt_surf, prompt_rect)


def draw_victory_screen():
    """Draw victory screen with mouse support"""
    screen.fill((20, 50, 20))  # Dark green background
    
    # Draw title
    title = "VICTORY!"
    title_surf = font.render(title, True, (100, 255, 100))
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title_surf, title_rect)
    
    # Draw line
    pygame.draw.line(screen, WHITE, (100, 130), (SCREEN_WIDTH - 100, 130), 2)
    
    # Draw victory text if available
    if current_story:
        victory_lines = current_story.get('victory_text', [])
        y_offset = 180
        for line in victory_lines:
            if line:
                text_surf = small_font.render(line, True, WHITE)
            else:
                text_surf = small_font.render(" ", True, WHITE)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text_surf, text_rect)
            y_offset += 30
    
    # Get mouse position for hover detection
    mouse_pos = pygame.mouse.get_pos()
    hovered_index = get_menu_button_at_mouse(mouse_pos, menu_buttons, button_start_y=380, button_spacing=50)
    
    # Draw menu
    y_offset = 380
    for i, button in enumerate(menu_buttons):
        # Highlight if selected by keyboard or hovered by mouse
        if i == selected_menu_item or i == hovered_index:
            color = (255, 255, 100)
            text = f"> {button['text']} <"
        else:
            color = WHITE
            text = button['text']
        
        button_surf = medium_font.render(text, True, color)
        button_rect = button_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 50))
        screen.blit(button_surf, button_rect)


def draw_defeat_screen():
    """Draw defeat screen with mouse support"""
    screen.fill((50, 20, 20))  # Dark red background
    
    # Draw title
    title = "DEFEAT"
    title_surf = font.render(title, True, (255, 100, 100))
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title_surf, title_rect)
    
    # Draw line
    pygame.draw.line(screen, WHITE, (100, 130), (SCREEN_WIDTH - 100, 130), 2)
    
    # Draw defeat text if available
    if current_story:
        defeat_lines = current_story.get('defeat_text', [])
        y_offset = 180
        for line in defeat_lines:
            if line:
                text_surf = small_font.render(line, True, WHITE)
            else:
                text_surf = small_font.render(" ", True, WHITE)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text_surf, text_rect)
            y_offset += 30
    
    # Get mouse position for hover detection
    mouse_pos = pygame.mouse.get_pos()
    hovered_index = get_menu_button_at_mouse(mouse_pos, menu_buttons, button_start_y=380, button_spacing=50)
    
    # Draw menu
    y_offset = 380
    for i, button in enumerate(menu_buttons):
        # Highlight if selected by keyboard or hovered by mouse
        if i == selected_menu_item or i == hovered_index:
            color = (255, 255, 100)
            text = f"> {button['text']} <"
        else:
            color = WHITE
            text = button['text']
        
        button_surf = medium_font.render(text, True, color)
        button_rect = button_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 50))
        screen.blit(button_surf, button_rect)

 
# ============================================================================
# EVENT HANDLING
# ============================================================================

def handle_menu_events(event):
    """
    Handle events for menu screens (keyboard and mouse)
    
    Args:
        event: Pygame event
        
    Returns:
        bool: True to continue, False to quit
    """
    global selected_menu_item, current_state, current_scenario_number
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return False
        elif event.key == pygame.K_UP:
            selected_menu_item = (selected_menu_item - 1) % len(menu_buttons)
        elif event.key == pygame.K_DOWN:
            selected_menu_item = (selected_menu_item + 1) % len(menu_buttons)
        elif event.key == pygame.K_RETURN:
            # Execute selected action
            execute_menu_action(selected_menu_item)
    
    elif event.type == pygame.MOUSEMOTION:
        # Update selected item based on mouse hover
        # Use different button positions for victory/defeat screens
        mouse_pos = pygame.mouse.get_pos()
        if current_state in [GameState.VICTORY, GameState.DEFEAT]:
            hovered_index = get_menu_button_at_mouse(mouse_pos, menu_buttons, button_start_y=380, button_spacing=50)
        else:
            hovered_index = get_menu_button_at_mouse(mouse_pos, menu_buttons)
        if hovered_index >= 0:
            selected_menu_item = hovered_index
    
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left click
            mouse_pos = event.pos
            # Use different button positions for victory/defeat screens
            if current_state in [GameState.VICTORY, GameState.DEFEAT]:
                clicked_index = get_menu_button_at_mouse(mouse_pos, menu_buttons, button_start_y=380, button_spacing=50)
            else:
                clicked_index = get_menu_button_at_mouse(mouse_pos, menu_buttons)
            if clicked_index >= 0:
                selected_menu_item = clicked_index
                execute_menu_action(clicked_index)
    
    return True


def execute_menu_action(button_index):
    """
    Execute the action for a menu button
    
    Args:
        button_index (int): Index of the button to execute
    """
    global current_state, current_scenario_number
    
    if button_index < 0 or button_index >= len(menu_buttons):
        return
    
    action = menu_buttons[button_index]['action']
    
    if action == "campaign":
        start_scenario(1, campaign_mode=True)
    elif action == "skirmish":
        init_scenario_select_menu()
        current_state = GameState.SCENARIO_SELECT
    elif action == "scenario_1":
        start_scenario(1, campaign_mode=False)
    elif action == "scenario_2":
        start_scenario(2, campaign_mode=False)
    elif action == "scenario_3":
        start_scenario(3, campaign_mode=False)
    elif action == "main_menu":
        init_main_menu()
        current_state = GameState.MAIN_MENU
    elif action == "next_scenario":
        next_num = current_story.get('next_scenario')
        if next_num:
            start_scenario(next_num, campaign_mode=True)
    elif action == "replay":
        start_scenario(current_scenario_number, campaign_mode=is_campaign_mode)
    elif action == "quit":
        pygame.quit()
        sys.exit()


def handle_story_events(event):
    """
    Handle events for story screen
    
    Args:
        event: Pygame event
        
    Returns:
        bool: True to continue, False to quit
    """
    global current_state, scenario
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            init_main_menu()
            current_state = GameState.MAIN_MENU
        elif event.key == pygame.K_RETURN:
            # Start the scenario
            scenario = Scenario(scenario_number=current_scenario_number, cell_size=64)
            scenario.grid.scale_to_screen_height(SCREEN_HEIGHT)
            current_state = GameState.PLAYING
    
    return True


def handle_playing_events(event):
    """
    Handle events during gameplay
    
    Args:
        event: Pygame event
        
    Returns:
        bool: True to continue, False to quit
    """
    global current_state
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            # Go back to main menu
            init_main_menu()
            current_state = GameState.MAIN_MENU
            return True
        elif event.key == pygame.K_SPACE:
            # SPACE key - end current player's turn
            scenario.end_turn()
        elif event.key == pygame.K_TAB:
            # TAB key - cycle to next active unit
            scenario.cycle_to_next_active_unit()
        elif event.key == pygame.K_h:
            # H key - toggle damage numbers display
            scenario.show_combat_messages = not scenario.show_combat_messages
            status = "ON" if scenario.show_combat_messages else "OFF"
            print(f"Damage numbers display: {status}")
        elif event.key == pygame.K_p:
            # P key - toggle show all map (75% fog vs 100% fog)
            scenario.show_all_map = not scenario.show_all_map
            status = "ON" if scenario.show_all_map else "OFF"
            print(f"Show all map (75% fog): {status}")
    
    # Pass ALL events to grid for pan/zoom tracking
    scenario.grid.handle_event(event, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Handle unit selection and movement
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:  # Left mouse button released
            if not scenario.grid.is_dragging():
                # This was a click, not a drag
                mouse_x, mouse_y = event.pos
                grid_pos = scenario.screen_to_grid(mouse_x, mouse_y, SCREEN_WIDTH, SCREEN_HEIGHT)
                
                if grid_pos:
                    row, col = grid_pos
                    scenario.handle_click(row, col)
    
    return True


def handle_events():
    """
    Process all input events based on current game state
    
    Returns:
        bool: True to continue running, False to quit the game
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        # Route events based on game state
        if current_state == GameState.MAIN_MENU:
            if not handle_menu_events(event):
                return False
        elif current_state == GameState.STORY_SCREEN:
            if not handle_story_events(event):
                return False
        elif current_state == GameState.PLAYING:
            if not handle_playing_events(event):
                return False
        elif current_state == GameState.VICTORY:
            if not handle_menu_events(event):
                return False
        elif current_state == GameState.DEFEAT:
            if not handle_menu_events(event):
                return False
        elif current_state == GameState.SCENARIO_SELECT:
            if not handle_menu_events(event):
                return False
    
    return True


# ============================================================================
# GAME LOGIC UPDATE
# ============================================================================

def update(dt):
    """
    Update game state for one frame based on current state
    
    Args:
        dt (float): Delta time in seconds since last frame
    """
    global current_state
    
    if current_state == GameState.PLAYING:
        # Update scenario
        scenario.update(dt)
        
        # Update hover
        mouse_x, mouse_y = pygame.mouse.get_pos()
        scenario.update_hover(mouse_x, mouse_y, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Check for victory or defeat
        if get_victory_condition():
            init_victory_menu()
            current_state = GameState.VICTORY
            print("Victory!")
        elif get_defeat_condition():
            init_defeat_menu()
            current_state = GameState.DEFEAT
            print("Defeat!")


# ============================================================================
# RENDERING
# ============================================================================

def draw_gameplay(fps):
    """
    Render gameplay screen
    
    Args:
        fps (float): Current frames per second
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
    
    # Draw unit status indicators (green/yellow/gray glows)
    scenario.draw_unit_status_indicators(screen)
    
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
    current_team = game_config.get_team_config(scenario.current_turn)
    is_player = game_config.is_player_controlled(scenario.current_turn)
    
    if current_team:
        turn_name = f"{current_team['name']} Turn"
        # Use team color with some brightness adjustment for visibility
        base_color = current_team['color']
        turn_color = tuple(min(255, c + 50) for c in base_color)
    else:
        turn_name = f"Team {scenario.current_turn} Turn"
        turn_color = (100, 255, 100) if is_player else (255, 100, 100)
    
    turn_text = medium_font.render(turn_name, True, turn_color)
    screen.blit(turn_text, (10, 10))
    
    # Instructions panel (below turn indicator)
    instructions = [
        "Click unit to select",
        "Click green to move",
        "Drag to pan map",
        "SPACE: End turn",
        "TAB: Cycle units",
        "H: Toggle damage #s",
        "P: Show all map",
        "ESC: Main menu"
    ]
    for i, text in enumerate(instructions):
        inst_text = small_font.render(text, True, LIGHT_GRAY)
        screen.blit(inst_text, (10, 50 + i * 25))
    
    # Selected unit info bar (bottom of screen)
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
            f"Selected: {unit.unit_type} | HP: {unit.health}/{unit.max_health} | ATK: {attack_display} | MOB: {unit.mobility}/{effective_mobility} | VIS: {unit.vision_range}",
            True, (255, 255, 100)
        )
        screen.blit(info_text, (10, SCREEN_HEIGHT - 30))
    
    # Hover tooltip
    scenario.draw_hover_info(screen, small_font)
    
    # Move preview tooltip
    scenario.draw_move_preview(screen, small_font)
    
    # FPS counter in upper-right corner
    fps_text = small_font.render(f"FPS: {int(fps)}", True, LIGHT_GRAY)
    fps_rect = fps_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    screen.blit(fps_text, fps_rect)


def draw(fps):
    """
    Render all game elements based on current state
    
    Args:
        fps (float): Current frames per second for FPS counter display
    """
    if current_state == GameState.MAIN_MENU:
        draw_menu("COMBAT ALLEY 2000", menu_buttons, selected_menu_item)
    elif current_state == GameState.SCENARIO_SELECT:
        draw_menu("SELECT SCENARIO", menu_buttons, selected_menu_item)
    elif current_state == GameState.STORY_SCREEN:
        draw_story_screen()
    elif current_state == GameState.PLAYING:
        draw_gameplay(fps)
    elif current_state == GameState.VICTORY:
        draw_victory_screen()
    elif current_state == GameState.DEFEAT:
        draw_defeat_screen()
    
    # Update display (flip buffers)
    pygame.display.flip()


# ============================================================================
# MAIN GAME LOOP
# ============================================================================

def main():
    """
    Main game loop with state machine
    
    Implements the standard game loop pattern:
    1. Calculate delta time (time since last frame)
    2. Handle events (input processing)
    3. Update game state (physics, animations, logic, state transitions)
    4. Render everything (draw to screen)
    
    The loop runs at the target FPS (60) until the user quits.
    State machine manages transitions between menus, story, and gameplay.
    """
    # Initialize main menu
    init_main_menu()
    
    running = True
    
    while running:
        # Calculate delta time in seconds
        dt = clock.tick(FPS) / 1000.0
        
        # Get actual FPS for display
        actual_fps = clock.get_fps()
        
        # Process input events
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
