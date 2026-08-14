"""
Caribbean Naval Warfare - Pirate-Themed Start Menu
8-bit pixel art style with animated water and ships
"""

import pygame
import sys
import math
from pathlib import Path


class StartMenu:
    def __init__(self, screen_width=1024, screen_height=768):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Caribbean Naval Warfare - Rise of the Pirate King")
        
        self.width = screen_width
        self.height = screen_height
        self.clock = pygame.time.Clock()
        
        # Colors - 8-bit pirate theme
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GOLD = (255, 215, 0)
        self.DARK_GOLD = (184, 134, 11)
        self.RED = (200, 40, 40)
        self.DARK_RED = (120, 20, 20)
        self.BLUE_WATER = (30, 80, 120)
        self.BLUE_WATER_LIGHT = (50, 110, 170)
        self.BLUE_WATER_DARK = (20, 60, 90)
        self.BROWN = (100, 70, 40)
        self.CREAM = (240, 220, 180)
        
        # Animation state
        self.time = 0
        
        # Menu options
        self.menu_items = [
            "NEW CAMPAIGN",
            "CONTINUE",
            "QUICK BATTLE",
            "MAP EDITOR",
            "OPTIONS",
            "QUIT"
        ]
        self.selected_index = 0
        
        # Create fonts
        self.title_font = pygame.font.Font(None, 96)
        self.subtitle_font = pygame.font.Font(None, 48)
        self.menu_font = pygame.font.Font(None, 42)
        self.small_font = pygame.font.Font(None, 24)
        
    def draw_static_water(self):
        """Draw static water background with subtle gradient"""
        # Create gradient effect from dark to mid blue
        for y in range(0, self.height):
            # Gradient calculation
            ratio = y / self.height
            r = int(self.BLUE_WATER_DARK[0] + (self.BLUE_WATER[0] - self.BLUE_WATER_DARK[0]) * ratio)
            g = int(self.BLUE_WATER_DARK[1] + (self.BLUE_WATER[1] - self.BLUE_WATER_DARK[1]) * ratio)
            b = int(self.BLUE_WATER_DARK[2] + (self.BLUE_WATER[2] - self.BLUE_WATER_DARK[2]) * ratio)
            color = (r, g, b)
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))
    
    def draw_ship_silhouette(self, x, y, scale=1.0):
        """Draw a simple pirate ship silhouette"""
        # Scale all coordinates
        def s(val):
            return int(val * scale)
        
        # Hull
        hull_points = [
            (x - s(20), y + s(10)),
            (x - s(20), y),
            (x + s(20), y),
            (x + s(20), y + s(10)),
            (x + s(15), y + s(15)),
            (x - s(15), y + s(15))
        ]
        pygame.draw.polygon(self.screen, self.BLACK, hull_points)
        
        # Masts
        pygame.draw.rect(self.screen, self.BLACK, (x - s(10), y - s(25), s(3), s(25)))
        pygame.draw.rect(self.screen, self.BLACK, (x + s(5), y - s(22), s(3), s(22)))
        
        # Sails
        sail1 = [(x - s(20), y - s(20)), (x - s(20), y - s(5)), (x, y - s(5)), (x, y - s(20))]
        sail2 = [(x, y - s(18)), (x, y - s(5)), (x + s(15), y - s(5)), (x + s(15), y - s(18))]
        pygame.draw.polygon(self.screen, self.CREAM, sail1)
        pygame.draw.polygon(self.screen, self.CREAM, sail2)
        
        # Flag (pirate flag!)
        pygame.draw.rect(self.screen, self.RED, (x - s(10), y - s(28), s(8), s(5)))
    
    def draw_title(self):
        """Draw the game title with pirate theme"""
        # Main title
        title_text = "CARIBBEAN"
        title_surface = self.title_font.render(title_text, True, self.GOLD)
        title_rect = title_surface.get_rect(center=(self.width // 2, 100))
        
        # Shadow
        shadow_surface = self.title_font.render(title_text, True, self.DARK_GOLD)
        shadow_rect = shadow_surface.get_rect(center=(self.width // 2 + 3, 103))
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = "NAVAL WARFARE"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, self.WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(self.width // 2, 160))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Tagline
        tagline_text = "~ Rise of the Pirate King ~"
        tagline_surface = self.menu_font.render(tagline_text, True, self.CREAM)
        tagline_rect = tagline_surface.get_rect(center=(self.width // 2, 210))
        self.screen.blit(tagline_surface, tagline_rect)
    
    def draw_menu(self):
        """Draw menu options"""
        menu_start_y = 320
        menu_spacing = 60
        
        for i, item in enumerate(self.menu_items):
            # Highlight selected item
            if i == self.selected_index:
                color = self.GOLD
                # Draw selection indicator (skull and crossbones style!)
                indicator_x = self.width // 2 - 180
                indicator_y = menu_start_y + i * menu_spacing
                pygame.draw.circle(self.screen, self.RED, (indicator_x, indicator_y + 10), 8)
                pygame.draw.rect(self.screen, self.WHITE, (indicator_x - 10, indicator_y + 15, 5, 8))
                pygame.draw.rect(self.screen, self.WHITE, (indicator_x + 5, indicator_y + 15, 5, 8))
            else:
                color = self.WHITE
            
            # Draw menu item
            text_surface = self.menu_font.render(item, True, color)
            text_rect = text_surface.get_rect(center=(self.width // 2, menu_start_y + i * menu_spacing))
            self.screen.blit(text_surface, text_rect)
    
    def draw_decorations(self):
        """Draw decorative elements"""
        # Sailing ships in background
        ship_y = 280 + math.sin(self.time * 0.001) * 10
        self.draw_ship_silhouette(150, int(ship_y), 0.6)
        
        ship2_y = 320 + math.sin(self.time * 0.0015 + 2) * 12
        self.draw_ship_silhouette(self.width - 150, int(ship2_y), 0.8)
        
        # Treasure chest (bottom left)
        chest_x, chest_y = 80, self.height - 100
        pygame.draw.rect(self.screen, self.BROWN, (chest_x, chest_y, 50, 35))
        pygame.draw.rect(self.screen, self.DARK_GOLD, (chest_x, chest_y - 5, 50, 8))
        # Gold coins spilling out
        for i in range(5):
            coin_x = chest_x + 55 + i * 12
            coin_y = chest_y + 25 + (i % 2) * 5
            pygame.draw.circle(self.screen, self.GOLD, (coin_x, coin_y), 6)
            pygame.draw.circle(self.screen, self.DARK_GOLD, (coin_x, coin_y), 4)
        
        # Compass (bottom right)
        compass_x, compass_y = self.width - 100, self.height - 100
        pygame.draw.circle(self.screen, self.DARK_GOLD, (compass_x, compass_y), 30)
        pygame.draw.circle(self.screen, self.CREAM, (compass_x, compass_y), 25)
        # Compass needle
        angle = self.time * 0.001
        needle_x = compass_x + math.cos(angle) * 18
        needle_y = compass_y + math.sin(angle) * 18
        pygame.draw.line(self.screen, self.RED, (compass_x, compass_y), (needle_x, needle_y), 3)
        
        # Version info
        version_text = "v1.0 - 8-bit Edition"
        version_surface = self.small_font.render(version_text, True, self.CREAM)
        version_rect = version_surface.get_rect(center=(self.width // 2, self.height - 30))
        self.screen.blit(version_surface, version_rect)
    
    def draw(self):
        """Draw the complete menu"""
        self.draw_static_water()
        self.draw_decorations()
        self.draw_title()
        self.draw_menu()
    
    def handle_input(self, event):
        """Handle keyboard and mouse input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.menu_items[self.selected_index]
            elif event.key == pygame.K_ESCAPE:
                return "QUIT"
        
        elif event.type == pygame.MOUSEMOTION:
            # Highlight menu item under mouse
            mouse_y = event.pos[1]
            menu_start_y = 320
            menu_spacing = 60
            for i in range(len(self.menu_items)):
                item_y = menu_start_y + i * menu_spacing
                if abs(mouse_y - item_y) < 25:
                    self.selected_index = i
                    break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click on menu item
            if event.button == 1:  # Left click
                return self.menu_items[self.selected_index]
        
        return None
    
    def run(self):
        """Main menu loop"""
        running = True
        selected_action = None
        
        while running:
            self.time += self.clock.get_time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                action = self.handle_input(event)
                if action:
                    selected_action = action
                    running = False
            
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        return selected_action


def main():
    """Test the start menu"""
    menu = StartMenu()
    action = menu.run()
    print(f"Selected: {action}")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
