# src/ui/item_window.py
import pygame
import random
from utils.currency import get_currencies, remove_currency
from utils.item_manager import (
    upgrade_item, scrap_item, merge_items, can_upgrade_item, 
    get_token_cost, get_essence_cost, MAX_LEVELS, find_mergeable_items
)
from utils.inventory_manager import inventory_remove, inventory_add, ensure_dict_format
from utils.resource_loader import load_image

class ItemWindow:
    def __init__(self, screen, item, hero_data=None, is_equipped=False):
        self.screen = screen
        self.item = item
        self.hero_data = hero_data
        self.is_equipped = is_equipped
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Window configuration
        self.width = 250
        self.height = 200
        
        # Calculate position to center on screen
        screen_w, screen_h = screen.get_size()
        self.x = (screen_w - self.width) // 2
        self.y = (screen_h - self.height) // 2
        
        # Create rect for window
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Define button rects
        button_width = 100
        button_height = 30
        button_spacing = 10
        button_y = self.y + self.height - button_height - 10
        
        self.upgrade_button = pygame.Rect(
            self.x + 10, 
            button_y,
            button_width,
            button_height
        )
        
        self.scrap_button = pygame.Rect(
            self.x + self.width - button_width - 10,
            button_y,
            button_width,
            button_height
        )
        
        # Check if we should show merge button
        self.mergeable_items = None
        self.merge_button = None
        self.show_merge = False
        
        # Only check for merging if item is in inventory
        if not is_equipped:
            mergeable_sets = find_mergeable_items()
            for key, items in mergeable_sets.items():
                if item["id"] in [i["id"] for i in items]:
                    self.mergeable_items = items
                    self.show_merge = True
                    self.merge_button = pygame.Rect(
                        self.x + (self.width - button_width) // 2,
                        button_y - button_height - 5,
                        button_width,
                        button_height
                    )
                    break
        
        # Scrap confirmation variables
        self.scrap_confirm = False
        self.scrap_rewards = None
        
        # Try to load essence icon
        try:
            self.essence_icon = load_image("ui/essence.png")
            self.essence_icon = pygame.transform.scale(self.essence_icon, (16, 16))
        except:
            self.essence_icon = None
            
        # Try to load token icons
        self.token_icons = {}
        for token_type in ["gear", "augment", "stim"]:
            try:
                icon = load_image(f"ui/{token_type}_token.png")
                self.token_icons[token_type] = pygame.transform.scale(icon, (16, 16))
            except:
                pass
        
        # Try to load neural pattern icon
        try:
            self.neural_icon = load_image("ui/neural_pattern.png")
            self.neural_icon = pygame.transform.scale(self.neural_icon, (16, 16))
        except:
            self.neural_icon = None
    
    def draw(self):
        # Draw window background
        pygame.draw.rect(self.screen, (240, 240, 240), self.rect)
        pygame.draw.rect(self.screen, (100, 100, 100), self.rect, 2)
        
        # Draw item name and level at top
        name_text = self.font.render(
            f"{self.item['name']} ({self.item['rarity'].capitalize()}) - Level {self.item.get('level', 1)}", 
            True, 
            (0, 0, 0)
        )
        self.screen.blit(name_text, (self.x + 10, self.y + 10))
        
        # Draw divider line
        pygame.draw.line(
            self.screen, 
            (200, 200, 200), 
            (self.x + 10, self.y + 40),
            (self.x + self.width - 10, self.y + 40),
            2
        )
        
        if self.scrap_confirm:
            self._draw_scrap_confirmation()
        else:
            # Draw upgrade info
            self._draw_upgrade_info()
            
            # Draw buttons
            self._draw_buttons()
    
    def _draw_upgrade_info(self):
        level = self.item.get("level", 1)
        rarity = self.item.get("rarity", "common")
        slot = self.item.get("slot", "gear")
        max_level = MAX_LEVELS.get(rarity, 5)
        
        y_pos = self.y + 50
        
        if level >= max_level:
            # Item is at max level
            max_text = self.font.render("Maximum Level Reached", True, (0, 0, 0))
            text_rect = max_text.get_rect(centerx=self.rect.centerx, top=y_pos)
            self.screen.blit(max_text, text_rect)
            return
        
        # Get costs
        essence_cost = get_essence_cost(rarity, level + 1)
        token_cost = get_token_cost(rarity, level + 1)
        currencies = get_currencies()
        
        # Check if player has enough
        has_essence = currencies["essence"] >= essence_cost
        has_tokens = currencies["upgrade_tokens"][slot] >= token_cost
        
        # Draw essence cost
        essence_text = self.font.render(
            f"Cost: {essence_cost} Essence", 
            True, 
            (0, 0, 0) if has_essence else (255, 0, 0)
        )
        self.screen.blit(essence_text, (self.x + 10, y_pos))
        y_pos += 30
        
        # Draw token cost
        token_text = self.font.render(
            f"Tokens: {currencies['upgrade_tokens'][slot]}/{token_cost} {slot.capitalize()}", 
            True, 
            (0, 0, 0) if has_tokens else (255, 0, 0)
        )
        self.screen.blit(token_text, (self.x + 10, y_pos))
        y_pos += 40
        
        # Draw stat improvement info
        improvement_text = self.font.render("Stat Improvement:", True, (0, 0, 0))
        self.screen.blit(improvement_text, (self.x + 10, y_pos))
        y_pos += 25
        
        # Show what stats will improve
        if slot == "stim":
            stat_text = self.font.render("HP: +5", True, (0, 150, 0))
        else:  # gear or augment
            stat_name = "Armour" if slot == "gear" else "Attack"
            stat_text = self.font.render(f"{stat_name}: +2", True, (0, 150, 0))
        
        self.screen.blit(stat_text, (self.x + 20, y_pos))
    
    def _draw_scrap_confirmation(self):
        if not self.scrap_rewards:
            # Calculate rewards for display
            self.scrap_rewards = {
                "essence": 20 * {"common": 1, "rare": 2, "epic": 3, "prototype": 4}.get(self.item.get("rarity", "common"), 1),
                "tokens": 0 if self.item.get("rarity") == "common" else (1 if self.item.get("rarity") in ["rare", "epic"] else 2),
                "neural_chance": {"common": 10, "rare": 20, "epic": 35, "prototype": 55}.get(self.item.get("rarity", "common"), 0)
            }
        
        y_pos = self.y + 50
        
        # Draw scrap confirmation header
        confirm_text = self.font.render("Confirm Scrapping?", True, (0, 0, 0))
        text_rect = confirm_text.get_rect(centerx=self.rect.centerx, top=y_pos)
        self.screen.blit(confirm_text, text_rect)
        y_pos += 40
        
        # Draw rewards
        rewards_text = self.font.render("You will receive:", True, (0, 0, 0))
        self.screen.blit(rewards_text, (self.x + 10, y_pos))
        y_pos += 30
        
        # Essence reward
        essence_text = self.font.render(f"{self.scrap_rewards['essence']} Essence", True, (0, 0, 0))
        if self.essence_icon:
            self.screen.blit(self.essence_icon, (self.x + 10, y_pos))
            self.screen.blit(essence_text, (self.x + 30, y_pos))
        else:
            self.screen.blit(essence_text, (self.x + 10, y_pos))
        y_pos += 25
        
        # Token reward if any
        if self.scrap_rewards["tokens"] > 0:
            slot = self.item.get("slot", "gear")
            token_text = self.font.render(f"{self.scrap_rewards['tokens']} {slot.capitalize()} Token", True, (0, 0, 0))
            
            if slot in self.token_icons:
                self.screen.blit(self.token_icons[slot], (self.x + 10, y_pos))
                self.screen.blit(token_text, (self.x + 30, y_pos))
            else:
                self.screen.blit(token_text, (self.x + 10, y_pos))
            y_pos += 25
        
        # Neural pattern chance
        neural_text = self.font.render(f"{self.scrap_rewards['neural_chance']}% Neural Pattern", True, (0, 0, 0))
        if self.neural_icon:
            self.screen.blit(self.neural_icon, (self.x + 10, y_pos))
            self.screen.blit(neural_text, (self.x + 30, y_pos))
        else:
            self.screen.blit(neural_text, (self.x + 10, y_pos))
        
        # Draw confirmation buttons
        confirm_btn = pygame.Rect(
            self.x + 30,
            self.y + self.height - 40,
            80,
            30
        )
        cancel_btn = pygame.Rect(
            self.x + self.width - 110,
            self.y + self.height - 40,
            80,
            30
        )
        
        pygame.draw.rect(self.screen, (150, 150, 150), confirm_btn)
        pygame.draw.rect(self.screen, (100, 100, 100), confirm_btn, 2)
        pygame.draw.rect(self.screen, (150, 150, 150), cancel_btn)
        pygame.draw.rect(self.screen, (100, 100, 100), cancel_btn, 2)
        
        confirm_text = self.small_font.render("Confirm", True, (0, 0, 0))
        cancel_text = self.small_font.render("Cancel", True, (0, 0, 0))
        
        confirm_rect = confirm_text.get_rect(center=confirm_btn.center)
        cancel_rect = cancel_text.get_rect(center=cancel_btn.center)
        
        self.screen.blit(confirm_text, confirm_rect)
        self.screen.blit(cancel_text, cancel_rect)
        
        # Store button rects for interaction
        self.confirm_btn = confirm_btn
        self.cancel_btn = cancel_btn
    
    def _draw_buttons(self):
        # Draw upgrade button
        pygame.draw.rect(self.screen, (150, 150, 150), self.upgrade_button)
        pygame.draw.rect(self.screen, (100, 100, 100), self.upgrade_button, 2)
        
        # Draw button text
        upgrade_text = self.small_font.render("Upgrade", True, (0, 0, 0))
        upgrade_rect = upgrade_text.get_rect(center=self.upgrade_button.center)
        self.screen.blit(upgrade_text, upgrade_rect)
        
        # Draw scrap button
        pygame.draw.rect(self.screen, (150, 150, 150), self.scrap_button)
        pygame.draw.rect(self.screen, (100, 100, 100), self.scrap_button, 2)
        
        # Draw button text
        scrap_text = self.small_font.render("Scrap", True, (0, 0, 0))
        scrap_rect = scrap_text.get_rect(center=self.scrap_button.center)
        self.screen.blit(scrap_text, scrap_rect)
        
        # Draw merge button if applicable
        if self.show_merge and self.merge_button:
            pygame.draw.rect(self.screen, (150, 150, 150), self.merge_button)
            pygame.draw.rect(self.screen, (100, 100, 100), self.merge_button, 2)
            
            merge_text = self.small_font.render("Merge", True, (0, 0, 0))
            merge_rect = merge_text.get_rect(center=self.merge_button.center)
            self.screen.blit(merge_text, merge_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if not self.rect.collidepoint(mouse_pos):
                # Click outside window - close it
                return False
            
            if self.scrap_confirm:
                # Handle scrap confirmation buttons
                if self.confirm_btn.collidepoint(mouse_pos):
                    # Confirm scrapping
                    scrap_item(self.item)
                    return False  # Close window
                elif self.cancel_btn.collidepoint(mouse_pos):
                    # Cancel scrapping
                    self.scrap_confirm = False
                    return True
            else:
                # Handle regular buttons
                if self.upgrade_button.collidepoint(mouse_pos):
                    # Attempt upgrade
                    success = upgrade_item(self.item, self.is_equipped, self.hero_data)
                    return True  # Keep window open
                
                elif self.scrap_button.collidepoint(mouse_pos):
                    # Show scrap confirmation
                    self.scrap_confirm = True
                    return True
                
                elif self.show_merge and self.merge_button and self.merge_button.collidepoint(mouse_pos):
                    # Perform merge
                    if self.mergeable_items:
                        merge_items(self.mergeable_items)
                    return False  # Close window
        
        return True  # Keep window open

def show_item_window(screen, item, hero_data=None, is_equipped=False):
    """Show an interactive window for an item"""
    window = ItemWindow(screen, item, hero_data, is_equipped)
    
    running = True
    while running:
        window.draw()
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Signal to exit game
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Left click
                if not window.handle_event(event):
                    running = False
    
    return True  # Signal to continue game