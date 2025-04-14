# jovian_cards/src/ui/character_screen.py

import pygame
# Fix imports - remove src. prefix
from ui.ui_elements import HeroTile
from utils.resource_loader import load_heroes

class CharacterScreen:
    def __init__(self, screen):
        self.screen = screen
        self.heroes = load_heroes()
        self.selected_hero = None
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Home button (non-functional)
        self.home_button = pygame.Rect(700, 20, 80, 30)

    def display_heroes(self):
        for index, hero in enumerate(self.heroes):
            tile = HeroTile(hero)
            tile_rect = tile.get_rect()
            tile_rect.x = 50 + (index % 3) * (tile_rect.width + 20)
            tile_rect.y = 50 + (index // 3) * (tile_rect.height + 20)
            self.screen.blit(tile.image, tile_rect)

    def select_hero(self, hero):
        self.selected_hero = hero

    def draw(self):
        self.screen.fill((255, 255, 255))  # Clear screen with white
        
        # Add ROSTER title at the top of screen
        title_text = pygame.font.Font(None, 48).render("ROSTER", True, (0, 0, 0))
        title_rect = title_text.get_rect(centerx=self.screen.get_width() // 2, top=10)
        self.screen.blit(title_text, title_rect)
        
        self.display_heroes()
        
        # Draw home button (non-functional)
        pygame.draw.rect(self.screen, (200, 200, 200), self.home_button)
        pygame.draw.rect(self.screen, (100, 100, 100), self.home_button, 2)
        home_text = self.small_font.render("Home", True, (0, 0, 0))
        text_rect = home_text.get_rect(center=self.home_button.center)
        self.screen.blit(home_text, text_rect)
        
        # Check if mouse is over a hero portrait to show name tooltip
        mouse_pos = pygame.mouse.get_pos()
        for index, hero in enumerate(self.heroes):
            tile_rect = pygame.Rect(
                50 + (index % 3) * (100 + 20),  # x position
                50 + (index // 3) * (100 + 20),  # y position
                100,  # width
                100   # height
            )
            if tile_rect.collidepoint(mouse_pos):
                # Draw tooltip with hero name
                name_text = self.small_font.render(hero['name'], True, (0, 0, 0))
                tooltip_bg = name_text.get_rect()
                tooltip_bg.center = (tile_rect.centerx, tile_rect.bottom + 15)
                tooltip_bg.inflate_ip(10, 6)  # Make background a bit larger than text
                
                # Draw tooltip background
                pygame.draw.rect(self.screen, (240, 240, 240), tooltip_bg)
                pygame.draw.rect(self.screen, (100, 100, 100), tooltip_bg, 1)
                
                # Draw name text
                self.screen.blit(name_text, name_text.get_rect(center=tooltip_bg.center))
        
        if self.selected_hero:
            self.show_hero_details(self.selected_hero)
        
        pygame.display.flip()

    def show_hero_details(self, hero):
        # Create a panel for hero details
        panel_rect = pygame.Rect(400, 50, 350, 500)
        pygame.draw.rect(self.screen, (220, 220, 220), panel_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), panel_rect, 2)
        
        # Display hero name, rank and stats
        name_text = self.font.render(f"{hero['name']} - Rank {hero['rank']}", True, (0, 0, 0))
        self.screen.blit(name_text, (panel_rect.x + 10, panel_rect.y + 10))
        
        # Display stats
        stats_font = pygame.font.Font(None, 28)
        stats = hero['level_1_stats']
        y_pos = panel_rect.y + 60
        
        for stat, value in stats.items():
            stat_text = stats_font.render(f"{stat}: {value}", True, (0, 0, 0))
            self.screen.blit(stat_text, (panel_rect.x + 10, y_pos))
            y_pos += 30
        
        # Equipment section
        y_pos += 20
        equip_text = self.font.render("Equipment", True, (0, 0, 0))
        self.screen.blit(equip_text, (panel_rect.x + 10, y_pos))
        
        # View details button
        self.detail_button = pygame.Rect(panel_rect.x + 10, panel_rect.y + 450, 150, 30)
        pygame.draw.rect(self.screen, (180, 180, 180), self.detail_button)
        pygame.draw.rect(self.screen, (100, 100, 100), self.detail_button, 2)
        detail_text = stats_font.render("View Details", True, (0, 0, 0))
        text_rect = detail_text.get_rect(center=self.detail_button.center)
        self.screen.blit(detail_text, text_rect)

    # Update the view details button handler to pass the full hero data
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if a hero tile was clicked
            for index, hero in enumerate(self.heroes):
                tile = HeroTile(hero)
                tile_rect = tile.get_rect()
                tile_rect.x = 50 + (index % 3) * (tile_rect.width + 20)
                tile_rect.y = 50 + (index // 3) * (tile_rect.height + 20)
                
                if tile_rect.collidepoint(mouse_pos):
                    self.select_hero(hero)
                    break
            
            # Check if "View Details" button was clicked
            if self.selected_hero and hasattr(self, 'detail_button') and self.detail_button.collidepoint(mouse_pos):
                from ui.hero_detail_screen import HeroDetailScreen
                # Pass the entire hero data object instead of just the name
                detail_screen = HeroDetailScreen(self.selected_hero)
                detail_screen.run()
                self.selected_hero = None

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_input(event)
            
            self.draw()
        
        pygame.quit()