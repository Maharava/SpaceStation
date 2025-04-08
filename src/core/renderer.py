import pygame
import os

class Renderer:
    def __init__(self, config):
        self.config = config
        self.width = config.get("screen_width")
        self.height = config.get("screen_height")
        self.fullscreen = config.get("fullscreen")
        
        pygame.init()
        self.setup_display()
        self.clock = pygame.time.Clock()
        self.fps = config.get("fps_cap")
        
        # For debugging
        self.font = pygame.font.SysFont("Arial", 18)
    
    def setup_display(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode(
                (self.width, self.height),
                pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode(
                (self.width, self.height)
            )
        pygame.display.set_caption("Starbound Exile: Derelict Awakening")
    
    def clear_screen(self):
        self.screen.fill((0, 0, 0))
    
    def draw_text(self, text, x, y, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def draw_rectangle(self, x, y, width, height, color):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
    
    def draw_circle(self, x, y, radius, color):
        pygame.draw.circle(self.screen, color, (x, y), radius)
    
    def update_display(self):
        pygame.display.flip()
        self.clock.tick(self.fps)
    
    def shutdown(self):
        pygame.quit()