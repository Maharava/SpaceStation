# src/screens/home_screen.py
import pygame
import os
import json
import random
import time
from utils.resource_loader import load_image, DATA_DIR
from utils.currency import get_currencies
from screens.character_screen import CharacterScreen

class HomeScreen:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.screen = screen_manager.screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Load background
        try:
            self.background = load_image("ui/backgrounds/home_screen.png")
            self.background = pygame.transform.scale(self.background, (800, 600))
        except:
            self.background = pygame.Surface((800, 600))
            self.background.fill((220, 220, 220))
        
        # Load button image
        try:
            self.button_img = load_image("ui/button.png")
            self.button_width = 150
            self.button_height = 50
            self.button_img = pygame.transform.scale(self.button_img, (self.button_width, self.button_height))
        except Exception as e:
            print(f"Error loading button image: {e}")
            self.button_img = None
        
        # Navigation buttons
        self.roster_button = pygame.Rect(150, 500, self.button_width, self.button_height)
        self.run_button = pygame.Rect(325, 500, self.button_width, self.button_height)
        self.develop_button = pygame.Rect(500, 500, self.button_width, self.button_height)
        
        # Load currency icons
        self.currency_icons = {}
        try:
            self.currency_icons["essence"] = load_image("ui/essence.png")
            self.currency_icons["tokens"] = load_image("ui/gear_token.png")
            self.currency_icons["patterns"] = load_image("ui/aug_token.png")
            
            # Scale icons
            for key in self.currency_icons:
                self.currency_icons[key] = pygame.transform.scale(self.currency_icons[key], (24, 24))
        except Exception as e:
            print(f"Error loading currency icons: {e}")
        
        # Secretary system
        self.secretary = self.load_secretary()
        self.dialogue_active = False
        self.dialogue_text = ""
        self.dialogue_start_time = 0
        self.last_dialogue_time = 0
        
        # Tooltip tracking
        self.tooltip_active = False
        self.tooltip_text = ""
        self.tooltip_position = (0, 0)
    
    def load_secretary(self):
        try:
            # Check if secretary is set
            secretary_path = os.path.join(DATA_DIR, "player", "secretary.json")
            if not os.path.exists(secretary_path):
                return None
                
            with open(secretary_path, "r") as f:
                secretary_data = json.load(f)
                hero_id = secretary_data.get("hero_id")
            
            # Load all heroes and find the one set as secretary
            heroes_path = os.path.join(DATA_DIR, "heroes")
            for filename in os.listdir(heroes_path):
                if filename.endswith(".json") and filename != "abilities.json":
                    with open(os.path.join(heroes_path, filename), "r") as f:
                        hero_data = json.load(f)
                        if hero_data.get("id") == hero_id:
                            # Load full body image
                            image = load_image(f"heroes/{hero_data['images']['full_body']}")
                            
                            # Scale image appropriately
                            height = 400
                            width = int(image.get_width() * (height / image.get_height()))
                            scaled_image = pygame.transform.scale(image, (width, height))
                            
                            return {
                                "data": hero_data,
                                "image": scaled_image,
                                "rect": pygame.Rect(50, 150, width, height)
                            }
        except Exception as e:
            print(f"Error loading secretary: {e}")
        return None
    
    def show_dialogue(self):
        if not self.secretary:
            return
            
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_dialogue_time < 5:
            return
            
        # Get dialogue based on rank
        rank = self.secretary["data"].get("rank", 1)
        rank_key = f"rank{rank}"
        
        # Get dialogue options
        dialogue_options = self.secretary["data"].get("dialogue", {}).get(rank_key, [])
        if not dialogue_options:
            dialogue_options = ["Hello, Commander!"]
            
        # Select random dialogue
        self.dialogue_text = random.choice(dialogue_options)
        self.dialogue_active = True
        self.dialogue_start_time = current_time
        self.last_dialogue_time = current_time
    
    def draw(self):
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((220, 220, 220))
        
        # Draw navigation buttons
        buttons = [
            (self.roster_button, "Roster"),  # Changed from Heroes to Roster
            (self.run_button, "Start Run"),
            (self.develop_button, "Develop")
        ]
        
        for button, text in buttons:
            # Draw button image instead of rect
            if self.button_img:
                self.screen.blit(self.button_img, button)
            else:
                pygame.draw.rect(self.screen, (200, 200, 200), button)
                pygame.draw.rect(self.screen, (100, 100, 100), button, 2)
            
            text_surf = self.font.render(text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=button.center)
            self.screen.blit(text_surf, text_rect)
        
        # Draw currencies at top
        currencies = get_currencies()
        currency_types = ["essence", "tokens", "patterns"]
        
        start_x = 250
        for i, c_type in enumerate(currency_types):
            amount = currencies.get(c_type, 0)
            
            # Create background with light grey color
            bg_rect = pygame.Rect(start_x + i*100, 20, 90, 30)
            pygame.draw.rect(self.screen, (200, 200, 200, 200), bg_rect)  # Darker grey
            pygame.draw.rect(self.screen, (100, 100, 100), bg_rect, 1)
            
            # Draw icon if available
            if c_type in self.currency_icons:
                self.screen.blit(self.currency_icons[c_type], (bg_rect.x + 5, bg_rect.y + 3))
            
            # Draw amount
            amount_text = self.small_font.render(str(amount), True, (0, 0, 0))
            self.screen.blit(amount_text, (bg_rect.x + 35, bg_rect.y + 5))
        
        # Draw secretary if available
        if self.secretary:
            self.screen.blit(self.secretary["image"], (self.secretary["rect"].x, self.secretary["rect"].y))
            
            # Draw dialogue if active
            if self.dialogue_active:
                # Check if dialogue should fade
                current_time = time.time()
                if current_time - self.dialogue_start_time > 5:
                    self.dialogue_active = False
                else:
                    # Draw dialogue box
                    dialogue_box = self.screen_manager.create_dialogue_box(self.dialogue_text)
                    self.screen.blit(dialogue_box, (350, 250))
        
        # Draw tooltip if active
        if self.tooltip_active:
            tooltip_box, pos = self.screen_manager.create_tooltip(self.tooltip_text, self.tooltip_position)
            self.screen.blit(tooltip_box, pos)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.MOUSEMOTION:
                # Reset tooltip when mouse moves
                self.tooltip_active = False
                
                # Check if hovering over Coming Soon buttons
                mouse_pos = event.pos
                if self.run_button.collidepoint(mouse_pos) or self.develop_button.collidepoint(mouse_pos):
                    self.tooltip_active = True
                    self.tooltip_text = "Coming Soon"
                    self.tooltip_position = mouse_pos
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                # Check button clicks
                if self.roster_button.collidepoint(mouse_pos):
                    # Import here to avoid circular import
                    from screens.character_screen import CharacterScreen
                    character_screen = CharacterScreen(self.screen_manager)
                    self.screen_manager.push(character_screen)
                    # Don't return True here, let processing continue
                
                # Coming soon buttons
                elif self.run_button.collidepoint(mouse_pos) or self.develop_button.collidepoint(mouse_pos):
                    self.tooltip_active = True
                    self.tooltip_text = "Coming Soon"
                    self.tooltip_position = mouse_pos
                
                # Check secretary click
                elif self.secretary and self.secretary["rect"].collidepoint(mouse_pos):
                    self.show_dialogue()
        
        return True
    
    def run(self):
        # Add this line to reload secretary data every time we return to home screen
        self.secretary = self.load_secretary()
        
        if not self.handle_events():
            return False
            
        self.draw()
        return True