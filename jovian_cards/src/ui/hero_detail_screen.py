# jovian_cards/src/ui/hero_detail_screen.py

# This file displays detailed information about a selected hero, including stats and equipment.

import pygame
from utils.resource_loader import load_hero_data, load_image
from ui.tooltip import Tooltip

class HeroDetailScreen:
    def __init__(self, hero_data):
        # Use provided hero data instead of loading it again
        self.hero_data = hero_data
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Load full image if available (768x1024)
        if 'full_body' in self.hero_data['images']:
            full_filename = self.hero_data['images']['full_body']
            self.full_image = load_image(f"heroes/{full_filename}")
            
            # Scale full image to fit screen while preserving aspect ratio
            full_width = 350  # Increased from 300
            full_height = int(full_width * (1024/768))  # New aspect ratio
            self.full_image_scaled = pygame.transform.smoothscale(
                self.full_image, (full_width, full_height))
        else:
            self.full_image = None
        
        # Equipment slots - positioned in row on left side
        self.slot_size = (80, 80)
        slot_y = 300
        slot_spacing = 90
        start_x = 20
        
        self.enhancement_slot = pygame.Rect(start_x, slot_y, *self.slot_size)
        self.gear_slot = pygame.Rect(start_x + slot_spacing, slot_y, *self.slot_size)
        self.stim_slot = pygame.Rect(start_x + 2 * slot_spacing, slot_y, *self.slot_size)
        
        # Back button
        self.back_button = pygame.Rect(20, 550, 100, 30)
        
        # Tooltips
        self.tooltip_enhancement = Tooltip("Enhancement: Boosts Attack")
        self.tooltip_gear = Tooltip("Gear: Enhances Armour")
        self.tooltip_stim = Tooltip("Stim: Enhances HP")
        self.active_tooltip = None

        # Load equipment images if hero has equipment
        self.equipment_images = {}
        for equip in self.hero_data.get('equipment', []):
            slot_type = self.determine_slot_type(equip)
            if slot_type:
                image_path = f"gear/{equip['image']}" 
                try:
                    image = load_image(image_path)
                    # Scale to fit slot
                    scaled_image = pygame.transform.smoothscale(image, (self.slot_size[0]-10, self.slot_size[1]-10))
                    self.equipment_images[slot_type] = scaled_image
                except FileNotFoundError:
                    pass  # Skip if image not found

        # Create equipment-specific tooltips
        self.equipment_tooltips = {}
        for equip in self.hero_data.get('equipment', []):
            slot_type = self.determine_slot_type(equip)
            if slot_type:
                tooltip_text = f"{equip['name']} ({equip['rarity']}): +{next(iter(equip['stats'].values()))} {next(iter(equip['stats'].keys()))}"
                self.equipment_tooltips[slot_type] = Tooltip(tooltip_text)

    def determine_slot_type(self, gear):
        # Simple determination based on stats
        if "Attack" in gear.get("stats", {}):
            return "enhancement"
        elif "HP" in gear.get("stats", {}):
            return "stim"
        else:
            return "gear"  # Default for armor items

    def display_hero_details(self):
        self.screen.fill((255, 255, 255))
        
        # Display full image on right
        if hasattr(self, 'full_image_scaled'):
            # Position image on right side
            full_x = 800 - self.full_image_scaled.get_width() - 10  # 10px margin
            full_y = 30  # Moved up slightly
            self.screen.blit(self.full_image_scaled, (full_x, full_y))
        
        # Display name and rank at top left
        name_text = self.font.render(f"{self.hero_data['name']} - Rank {self.hero_data['rank']}", True, (0, 0, 0))
        self.screen.blit(name_text, (20, 20))
        
        # Description below name
        description = self.hero_data['description']
        desc_words = description.split()
        desc_lines = []
        current_line = ""
        for word in desc_words:
            test_line = current_line + " " + word if current_line else word
            if self.small_font.size(test_line)[0] < 400:
                current_line = test_line
            else:
                desc_lines.append(current_line)
                current_line = word
        if current_line:
            desc_lines.append(current_line)
            
        # Draw description lines
        y_pos = 60
        for line in desc_lines:
            description_text = self.small_font.render(line, True, (0, 0, 0))
            self.screen.blit(description_text, (20, y_pos))
            y_pos += 25
        
        # Calculate left panel width to end at image
        left_panel_width = 500 if self.full_image else 780
        
        # Stats section
        stats_y = max(120, y_pos + 20)  # At least 20px below description
        stats_title = self.font.render("Stats", True, (0, 0, 0))
        self.screen.blit(stats_title, (20, stats_y))
        
        # Display stats vertically in left panel
        stats = self.hero_data['level_1_stats']
        y_pos = stats_y + 40
        for stat, value in stats.items():
            stat_text = self.font.render(f"{stat}: {value}", True, (0, 0, 0))
            self.screen.blit(stat_text, (40, y_pos))
            y_pos += 40
        
        # Equipment title
        equip_y = y_pos + 20
        equip_title = self.font.render("Equipment", True, (0, 0, 0))
        self.screen.blit(equip_title, (20, equip_y))
        
        # Equipment slots now with more vertical space (60px instead of 40px)
        slot_spacing = 110
        slot_y = equip_y + 60  # Increased from 40 to 60
        start_x = 20
        
        # Display equipment slots
        for index, (slot, label, slot_type) in enumerate([
            (self.enhancement_slot, "Enhancement", "enhancement"),
            (self.gear_slot, "Gear", "gear"),
            (self.stim_slot, "Stim", "stim")
        ]):
            # Update slot positions
            slot.x = start_x + (index * slot_spacing)
            slot.y = slot_y
            
            pygame.draw.rect(self.screen, (220, 220, 220), slot)
            pygame.draw.rect(self.screen, (100, 100, 100), slot, 2)
            
            # Draw equipment image if slot has equipment
            if slot_type in self.equipment_images:
                image = self.equipment_images[slot_type]
                image_rect = image.get_rect(center=slot.center)
                self.screen.blit(image, image_rect)
            
            text = self.small_font.render(label, True, (0, 0, 0))
            text_rect = text.get_rect(centerx=slot.centerx, bottom=slot.top - 5)
            self.screen.blit(text, text_rect)
        
        # Back button
        pygame.draw.rect(self.screen, (200, 200, 200), self.back_button)
        pygame.draw.rect(self.screen, (100, 100, 100), self.back_button, 2)
        back_text = self.small_font.render("Back", True, (0, 0, 0))
        text_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, text_rect)
        
        # Draw tooltip if active
        if self.active_tooltip:
            self.active_tooltip.draw(self.screen)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(event.pos):
                    return False
            elif event.type == pygame.MOUSEMOTION:
                # Reset active tooltip
                self.active_tooltip = None
                
                # Check equipment slots
                slots = [
                    (self.enhancement_slot, "enhancement", self.tooltip_enhancement),
                    (self.gear_slot, "gear", self.tooltip_gear),
                    (self.stim_slot, "stim", self.tooltip_stim)
                ]
                
                for slot, slot_type, default_tooltip in slots:
                    if slot.collidepoint(event.pos):
                        # Use equipment tooltip if available, otherwise use default
                        if slot_type in self.equipment_tooltips:
                            self.equipment_tooltips[slot_type].show(event.pos)
                            self.active_tooltip = self.equipment_tooltips[slot_type]
                        else:
                            default_tooltip.show(event.pos)
                            self.active_tooltip = default_tooltip
                        break
                        
        return True

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.display_hero_details()