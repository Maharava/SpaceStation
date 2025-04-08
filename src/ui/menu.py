# src/ui/menu.py
import pygame
from src.utils.logger import logger

class MenuItem:
    def __init__(self, text, action, x, y, width, height):
        self.text = text
        self.action = action
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hover = False
    
    def is_mouse_over(self, mouse_pos):
        mx, my = mouse_pos
        return (self.x <= mx <= self.x + self.width and
                self.y <= my <= self.y + self.height)

class Menu:
    def __init__(self, renderer):
        self.renderer = renderer
        self.items = []
        self.title = ""
        self.background_color = (20, 20, 50)
        self.title_font = pygame.font.SysFont("Arial", 36)
        self.font = pygame.font.SysFont("Arial", 24)
    
    def add_item(self, text, action, width=200, height=40):
        """Add a menu item"""
        try:
            # Calculate position (center-aligned)
            screen_width = self.renderer.width
            x = (screen_width - width) // 2
            
            # Position below previous items
            y = 150 + len(self.items) * (height + 20)
            
            self.items.append(MenuItem(text, action, x, y, width, height))
        except Exception as e:
            logger.error(f"Error adding menu item: {str(e)}")
    
    def set_title(self, title):
        """Set the menu title"""
        self.title = title
    
    def handle_event(self, event):
        """Process menu input events"""
        try:
            if event.type == pygame.MOUSEMOTION:
                # Update hover state
                for item in self.items:
                    item.hover = item.is_mouse_over(event.pos)
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    for item in self.items:
                        if item.is_mouse_over(event.pos):
                            return item.action
            
            return None
        except Exception as e:
            logger.error(f"Error handling menu event: {str(e)}")
            return None
    
    def render(self):
        """Render the menu"""
        try:
            # Clear the screen
            self.renderer.clear_screen()
            
            # Draw background
            screen_width = self.renderer.width
            screen_height = self.renderer.height
            
            # Draw title
            if self.title:
                title_surface = self.title_font.render(self.title, True, (255, 255, 255))
                title_rect = title_surface.get_rect(center=(screen_width // 2, 80))
                self.renderer.screen.blit(title_surface, title_rect)
            
            # Draw menu items
            for item in self.items:
                # Item background (different if hovered)
                if item.hover:
                    bg_color = (80, 80, 120)
                else:
                    bg_color = (50, 50, 80)
                
                # Draw button background
                self.renderer.draw_rectangle(item.x, item.y, item.width, item.height, bg_color)
                
                # Draw text
                text_surface = self.font.render(item.text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(item.x + item.width // 2, item.y + item.height // 2))
                self.renderer.screen.blit(text_surface, text_rect)
            
            # Update display
            self.renderer.update_display()
        except Exception as e:
            logger.error(f"Error rendering menu: {str(e)}")