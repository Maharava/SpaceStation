# jovian_cards/src/ui/character_screen.py

import pygame
# Fix imports - remove src. prefix
from ui.ui_elements import HeroTile
from utils.resource_loader import load_heroes
from utils.currency import get_currencies
from utils.resource_loader import load_image
from utils.hero_progression import can_level_up

class CharacterScreen:
    def __init__(self, screen):
        self.screen = screen
        self.heroes = load_heroes()
        self.selected_hero = None
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Load background
        try:
            self.background = load_image("ui/backgrounds/roster.png")
            # Scale to match screen size
            self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))
        except Exception as e:
            print(f"Could not load background: {e}")
            self.background = None
        
        # Home button (non-functional)
        self.home_button = pygame.Rect(700, 50, 80, 30)  # Changed Y from 20 to 50

        # Load essence icon
        try:
            self.essence_icon = load_image("ui/essence.png")
            self.essence_icon = pygame.transform.scale(self.essence_icon, (24, 24))
        except Exception as e:
            print(f"Could not load essence icon: {e}")
            self.essence_icon = None

    def display_heroes(self):
        for index, hero in enumerate(self.heroes):
            tile = HeroTile(hero)
            tile_rect = tile.get_rect()
            tile_rect.x = 50 + (index % 3) * (tile_rect.width + 20)
            tile_rect.y = 50 + (index // 3) * (tile_rect.height + 20)
            
            # Draw the tile first
            self.screen.blit(tile.image, tile_rect)
            
            # THEN draw border on top so it's visible
            pygame.draw.rect(self.screen, (0, 0, 0), tile_rect, 3)  # 3px thick black border
            
            # Add level-up indicator if hero can level up
            if can_level_up(hero):
                # Draw green up arrow in top right
                arrow_pos = (tile_rect.right - 15, tile_rect.top + 15)
                arrow_points = [
                    (arrow_pos[0], arrow_pos[1] + 10),  # Bottom middle
                    (arrow_pos[0] - 8, arrow_pos[1] + 2),  # Bottom left
                    (arrow_pos[0] + 8, arrow_pos[1] + 2),  # Bottom right
                ]
                pygame.draw.polygon(self.screen, (0, 200, 0), arrow_points)  # Green arrow

    def select_hero(self, hero):
        self.selected_hero = hero

    def draw(self):
        # Draw background if available, otherwise use white
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((255, 255, 255))
        
        # Add ROSTER title at the top of screen
        title_text = pygame.font.Font(None, 48).render("ROSTER", True, (0, 0, 0))
        title_rect = title_text.get_rect(centerx=self.screen.get_width() // 2, top=10)
        
        # Draw backing behind title
        backing_rect = title_rect.copy()
        backing_rect.inflate_ip(20, 10)  # Make backing slightly larger than text
        pygame.draw.rect(self.screen, (240, 240, 240, 220), backing_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), backing_rect, 1)
        
        # Draw the title text on top of backing
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
        
        # Draw essence amount in top right
        currencies = get_currencies()
        essence_text = self.small_font.render(str(currencies["essence"]), True, (0, 0, 0))
        essence_rect = essence_text.get_rect(right=self.screen.get_width() - 10, top=10)

        # Draw background for essence counter
        bg_rect = essence_rect.copy()
        if self.essence_icon:
            bg_rect.width += 30  # Make room for icon
        bg_rect.inflate_ip(10, 6)  # Add padding
        bg_rect.right = self.screen.get_width() - 5
        pygame.draw.rect(self.screen, (240, 240, 240, 220), bg_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), bg_rect, 1)

        # Draw essence icon
        if self.essence_icon:
            icon_rect = self.essence_icon.get_rect(right=essence_rect.left - 5, centery=essence_rect.centery)
            self.screen.blit(self.essence_icon, icon_rect)

        self.screen.blit(essence_text, essence_rect)

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
        from utils.stats_calculator import calculate_combined_stats
        if "combined_stats" in hero:
            stats = hero["combined_stats"]
        else:
            stats = calculate_combined_stats(hero.get('level_1_stats', {}), hero.get('equipment', {}))
        stats_font = pygame.font.Font(None, 28)
        y_pos = panel_rect.y + 60
        
        for stat, value in stats.items():
            stat_text = stats_font.render(f"{stat}: {value}", True, (0, 0, 0))
            self.screen.blit(stat_text, (panel_rect.x + 10, y_pos))
            y_pos += 30
        
        # Equipment section
        y_pos += 20
        equip_text = self.font.render("Equipment", True, (0, 0, 0))
        self.screen.blit(equip_text, (panel_rect.x + 10, y_pos))
        
        # Add small equipment slots (40x40)
        small_slot_size = 40
        slot_y = y_pos + 35
        slot_x = panel_rect.x + 20
        slot_gap = 10
        
        # Create slots for augment, gear, stim
        for i, slot_type in enumerate(["augment", "gear", "stim"]):
            slot_rect = pygame.Rect(slot_x + i * (small_slot_size + slot_gap), slot_y, 
                                    small_slot_size, small_slot_size)
            
            # Draw slot background
            pygame.draw.rect(self.screen, (240, 240, 240), slot_rect)
            pygame.draw.rect(self.screen, (100, 100, 100), slot_rect, 1)
            
            # Draw equipped item if any
            if isinstance(hero.get('equipment'), dict) and hero['equipment'].get(slot_type):
                try:
                    item = hero['equipment'][slot_type]
                    img_path = f"items/{slot_type}/{item['image']}"  # Changed from gear/
                    img = load_image(img_path)
                    img = pygame.transform.scale(img, (small_slot_size-6, small_slot_size-6))
                    self.screen.blit(img, (slot_rect.x+3, slot_rect.y+3))
                except:
                    pass  # Skip if image loading fails
            
            # Draw slot labels below
            if slot_type == "augment":
                label = "Aug"
            else:
                label = slot_type.capitalize()
            
            label_text = self.small_font.render(label, True, (0, 0, 0))
            label_rect = label_text.get_rect(centerx=slot_rect.centerx, top=slot_rect.bottom + 2)
            self.screen.blit(label_text, label_rect)
        
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