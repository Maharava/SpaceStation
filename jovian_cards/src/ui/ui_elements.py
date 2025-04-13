# jovian_cards/src/ui/ui_elements.py

# This file contains reusable UI components and elements used across different screens.

import pygame
from utils.resource_loader import load_image

class Button:
    def __init__(self, label, position, size):
        self.label = label
        self.position = position
        self.size = size

    def draw(self, screen):
        # Code to draw the button on the screen
        pass

    def is_clicked(self, mouse_pos):
        # Code to check if the button is clicked
        pass

class Label:
    def __init__(self, text, position):
        self.text = text
        self.position = position

    def draw(self, screen):
        # Code to draw the label on the screen
        pass

class Image:
    def __init__(self, image_path, position):
        self.image_path = image_path
        self.position = position

    def draw(self, screen):
        # Code to draw the image on the screen
        pass

# Update HeroTile to handle 512x512 portraits

class HeroTile:
    def __init__(self, hero):
        self.hero = hero
        portrait_path = f"heroes/{hero['images']['portrait']}"
        self.original_image = load_image(portrait_path)
        
        # Scale portrait (512x512) to tile size (100x100)
        tile_size = 100
        self.image = pygame.transform.smoothscale(self.original_image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        
    def get_rect(self):
        return self.rect
        
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)