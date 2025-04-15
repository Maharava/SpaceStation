# src/ui/tooltip.py
import pygame

class Tooltip:
    def __init__(self, text, font_size=20):
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.padding = 5
        self.bg_color = (240, 240, 240)
        self.text_color = (0, 0, 0)
        self.border_color = (100, 100, 100)
        self.visible = False
        self.position = (0, 0)
        
    def show(self, position):
        self.visible = True
        self.position = position
        
    def hide(self):
        self.visible = False
        
    def update_text(self, text):
        self.text = text
        
    def draw(self, surface):
        if not self.visible:
            return
            
        lines = self.text.split("\n")
        max_width = max([self.font.size(line)[0] for line in lines])
        line_height = self.font.get_linesize()
        
        # Create background rect
        bg_rect = pygame.Rect(
            self.position[0],
            self.position[1],
            max_width + (self.padding * 2),
            line_height * len(lines) + (self.padding * 2)
        )
        
        # Keep tooltip on screen
        screen_w, screen_h = surface.get_size()
        if bg_rect.right > screen_w:
            bg_rect.right = screen_w - 5
        if bg_rect.bottom > screen_h:
            bg_rect.bottom = screen_h - 5
            
        # Draw background and border
        pygame.draw.rect(surface, self.bg_color, bg_rect)
        pygame.draw.rect(surface, self.border_color, bg_rect, 1)
        
        # Draw text lines
        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, self.text_color)
            surface.blit(text_surf, (
                bg_rect.x + self.padding,
                bg_rect.y + self.padding + i * line_height
             ))