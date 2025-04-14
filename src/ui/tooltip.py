# jovian_cards/src/ui/tooltip.py

import pygame

class Tooltip:
    def __init__(self, text):
        self.text = text
        self.visible = False
        self.font = pygame.font.Font(None, 24)
        self.padding = 5
        self.bg_color = (240, 240, 240)
        self.text_color = (0, 0, 0)
        self.border_color = (100, 100, 100)

    def show(self, position):
        self.visible = True
        self.position = position

    def hide(self):
        self.visible = False

    def draw(self, surface):
        if self.visible:
            # Render text
            text_surf = self.font.render(self.text, True, self.text_color)
            # Create background rect
            bg_rect = text_surf.get_rect()
            bg_rect.topleft = self.position
            bg_rect.inflate_ip(self.padding * 2, self.padding * 2)
            
            # Draw background and border
            pygame.draw.rect(surface, self.bg_color, bg_rect)
            pygame.draw.rect(surface, self.border_color, bg_rect, 1)
            
            # Draw text
            text_pos = (self.position[0] + self.padding, self.position[1] + self.padding)
            surface.blit(text_surf, text_pos)

    def update_text(self, new_text):
        self.text = new_text