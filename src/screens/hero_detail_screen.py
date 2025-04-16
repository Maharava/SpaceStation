# jovian_cards/src/ui/hero_detail_screen.py

# This file displays detailed information about a selected hero, including stats and equipment.

import pygame
import json
import os
from utils.resource_loader import load_image, DATA_DIR, ASSETS_DIR
from utils.stats_calculator import calculate_combined_stats
from utils.inventory_manager import inventory_add, inventory_remove, ensure_dict_format, get_items_by_slot, get_inventory
from utils.abilities import get_ability_description
from ui.tooltip import Tooltip
from utils.currency import get_currencies
from ui.item_window import show_item_window
from utils.item_manager import calculate_item_stats
from utils.hero_progression import (
    can_level_up, level_up, can_rank_up, rank_up,
    get_level_up_cost, get_rank_up_cost, get_xp_required
)

class HeroDetailScreen:
    def __init__(self, hero_data, screen_manager):
        self.screen_manager = screen_manager
        self.screen = screen_manager.screen
        self.hero_data = hero_data
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.stat_value_font = pygame.font.Font(None, 40)
        
        # Load background
        try:
            self.background = load_image("ui/backgrounds/hero_details.png")
            self.background = pygame.transform.scale(self.background, (800, 600))
        except:
            self.background = pygame.Surface((800, 600))
            self.background.fill((255, 255, 255))
        
        # Load stat icons
        self.stat_icons = {}
        self.load_stat_icons()
        
        # Load hero image
        if 'full_body' in self.hero_data.get('images', {}):
            full_filename = self.hero_data['images']['full_body']
            self.full_image = load_image(f"heroes/{full_filename}")
            full_width = 350
            full_height = int(full_width * (1024/768))
            self.full_image_scaled = pygame.transform.smoothscale(
                self.full_image, (full_width, full_height))
        else:
            self.full_image = None
        
        # Equipment slots
        self.slot_size = (80, 80)
        self.augment_slot = pygame.Rect(20, 300, *self.slot_size)
        self.gear_slot = pygame.Rect(110, 300, *self.slot_size)
        self.stim_slot = pygame.Rect(200, 300, *self.slot_size)
        
        # Back button - initial position will be updated in draw method
        self.back_button = pygame.Rect(20, 550, 100, 30)
        
        # Tooltip using the external Tooltip class
        self.tooltip = Tooltip("")
        
        # Inventory variables - Always visible in Stage 2
        self.inventory_rects = []
        self.scroll_offset = 0
        # We'll calculate the exact position in draw_inventory
        self.inventory_panel = pygame.Rect(0, 0, 0, 0)
        
        # Equipment slots in dictionary for easy access
        self.equipment_slots = {
            "augment": self.augment_slot,
            "gear": self.gear_slot,
            "stim": self.stim_slot
        }
        
        # Load equipment images
        self.equipment_images = {}
        self.load_equipment_images()
        
        # Load all inventory items immediately
        self.load_inventory_items()
        
        # Add essence icon
        try:
            self.essence_icon = load_image("ui/essence.png")
            self.essence_icon = pygame.transform.scale(self.essence_icon, (24, 24))
        except:
            self.essence_icon = None
        
        # Add active item window tracker
        self.active_item_window = None
        self.active_item = None

        # Add level up and rank up buttons (will be updated in draw)
        self.level_up_button = pygame.Rect(0, 0, 80, 25)
        self.rank_up_button = pygame.Rect(0, 0, 80, 25)
        
        # Add secretary button with selection state
        try:
            # Fix secretary button paths to match the correct filenames
            self.secretary_button_selected = load_image("ui/sec_but_selected.png")
            self.secretary_button_selected = pygame.transform.scale(self.secretary_button_selected, (40, 40))
            
            self.secretary_button_unselected = load_image("ui/sec_but_unselected.png")
            self.secretary_button_unselected = pygame.transform.scale(self.secretary_button_unselected, (40, 40))
            
            self.secretary_button = pygame.Rect(self.screen.get_width() - 50, 
                                              self.screen.get_height() - 50, 40, 40)
            
            # Check if this hero is already the secretary
            self.is_secretary = self.check_if_secretary()
        except Exception as e:
            print(f"Could not load secretary buttons: {e}")
            self.secretary_button = pygame.Rect(self.screen.get_width() - 50, 
                                              self.screen.get_height() - 50, 40, 40)
            self.secretary_button_selected = None
            self.secretary_button_unselected = None
            self.is_secretary = False
            
        # For notifications
        self.notification_text = ""
        self.notification_time = 0
    
    def load_stat_icons(self):
        icon_mapping = {
            "attack": "attack.png", 
            "armour": "armour.png", 
            "hp": "hp.png"
        }
        
        for stat, filename in icon_mapping.items():
            try:
                icon_path = os.path.join(ASSETS_DIR, "ui", filename)
                if os.path.exists(icon_path):
                    icon = pygame.image.load(icon_path)
                    self.stat_icons[stat] = pygame.transform.scale(icon, (48, 48))
                else:
                    print(f"Icon file not found: {icon_path}")
            except Exception as e:
                print(f"Could not load icon for {stat}: {e}")
    
    def load_equipment_images(self):
        self.equipment_images = {}
        
        if isinstance(self.hero_data.get('equipment'), dict):
            for slot_type, item in self.hero_data['equipment'].items():
                if item:
                    try:
                        # Use default image name if none specified
                        image_name = item.get('image', f"{item['name'].lower().replace(' ', '_')}.png")
                        image_path = f"items/{slot_type}/{image_name}"
                        image = load_image(image_path)
                        scaled_image = pygame.transform.smoothscale(image, (self.slot_size[0]-10, self.slot_size[1]-10))
                        self.equipment_images[slot_type] = scaled_image
                    except Exception as e:
                        print(f"Error loading equipment image: {e}")
    
    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw hero image on right
        if hasattr(self, 'full_image_scaled'):
            full_x = 800 - self.full_image_scaled.get_width() - 10
            full_y = 30
            self.screen.blit(self.full_image_scaled, (full_x, full_y))
        
        # Create semi-transparent panel for left side
        left_panel = pygame.Surface((full_x - 20, 550), pygame.SRCALPHA)
        left_panel.fill((255, 255, 255, 170))
        self.screen.blit(left_panel, (10, 10))
        
        # Show hero name at top
        name_text = self.font.render(f"{self.hero_data['name']} - Rank {self.hero_data.get('rank', 1)}", True, (0, 0, 0))
        self.screen.blit(name_text, (20, 20))
        
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
        
        # XP bar with correct values
        xp_bar_rect = pygame.Rect(20, 60, 300, 25)
        xp_required = get_xp_required(self.hero_data)
        current_xp = self.hero_data.get('XP', 0)
        current_level = self.hero_data.get('level', 1)
        
        # Draw XP bar background
        pygame.draw.rect(self.screen, (50, 50, 50), xp_bar_rect)
        
        # Draw XP progress if any
        if xp_required > 0:
            fill_width = int((current_xp / xp_required) * xp_bar_rect.width)
            xp_fill_rect = pygame.Rect(xp_bar_rect.x, xp_bar_rect.y, fill_width, xp_bar_rect.height)
            pygame.draw.rect(self.screen, (0, 150, 0), xp_fill_rect)
        
        # XP text
        xp_text = self.small_font.render(f"Level {current_level} - XP: {current_xp}/{xp_required}", True, (255, 255, 255))
        self.screen.blit(xp_text, (xp_bar_rect.x + 10, xp_bar_rect.y + 4))
        
        # Draw level up button if can level up
        if can_level_up(self.hero_data):
            self.level_up_button.x = xp_bar_rect.right + 10
            self.level_up_button.y = xp_bar_rect.y
            
            pygame.draw.rect(self.screen, (100, 200, 100), self.level_up_button)
            pygame.draw.rect(self.screen, (50, 150, 50), self.level_up_button, 2)
            
            level_up_text = self.small_font.render("Level Up", True, (0, 0, 0))
            level_up_rect = level_up_text.get_rect(center=self.level_up_button.center)
            self.screen.blit(level_up_text, level_up_rect)
            
            # Show cost tooltip on hover
            mouse_pos = pygame.mouse.get_pos()
            if self.level_up_button.collidepoint(mouse_pos):
                cost = get_level_up_cost(self.hero_data)
                self.tooltip.update_text(f"Cost: {cost} Essence")
                self.tooltip.show((mouse_pos[0] + 15, mouse_pos[1] + 15))
        
        # Draw rank up button if eligible
        if can_rank_up(self.hero_data):
            self.rank_up_button.x = 20
            self.rank_up_button.y = 90
            
            pygame.draw.rect(self.screen, (200, 150, 100), self.rank_up_button)
            pygame.draw.rect(self.screen, (150, 100, 50), self.rank_up_button, 2)
            
            rank_up_text = self.small_font.render("Rank Up", True, (0, 0, 0))
            rank_up_rect = rank_up_text.get_rect(center=self.rank_up_button.center)
            self.screen.blit(rank_up_text, rank_up_rect)
            
            # Show cost tooltip on hover
            mouse_pos = pygame.mouse.get_pos()
            if self.rank_up_button.collidepoint(mouse_pos):
                cost = get_rank_up_cost(self.hero_data)
                self.tooltip.update_text(f"Cost: {cost} Essence\nRequires level 10+")
                self.tooltip.show((mouse_pos[0] + 15, mouse_pos[1] + 15))
        
        # Show stats with icons
        stats_y = 100
        icon_height = 48
        x_pos = 20
        icon_spacing = 120
        
        # Calculate combined stats
        base_stats = self.hero_data['level_1_stats']
        if "combined_stats" in self.hero_data:
            stats = self.hero_data["combined_stats"]
        else:
            stats = calculate_combined_stats(base_stats, self.hero_data.get('equipment', {}))
        
        for stat, value in stats.items():
            icon_key = None
            if (stat == "Attack"): icon_key = "attack"
            elif (stat == "Armour"): icon_key = "armour"
            elif (stat == "HP"): icon_key = "hp"
            
            if icon_key and icon_key in self.stat_icons:
                self.screen.blit(self.stat_icons[icon_key], (x_pos, stats_y))
                value_text = self.stat_value_font.render(str(value), True, (0, 0, 0))
                text_y = stats_y + (icon_height - value_text.get_height()) // 2
                self.screen.blit(value_text, (x_pos + 55, text_y))
                x_pos += icon_spacing
        
        # Equipment section
        equip_y = stats_y + 70
        
        # Draw equipment slots
        self.augment_slot.y = equip_y + 40
        self.gear_slot.y = equip_y + 40
        self.stim_slot.y = equip_y + 40
        
        for slot, label, slot_type in [
            (self.augment_slot, "Augment", "augment"),
            (self.gear_slot, "Gear", "gear"),
            (self.stim_slot, "Stim", "stim")
        ]:
            # Draw slot background
            slot_color = (220, 220, 220)
            if self.hero_data.get('equipment', {}).get(slot_type):
                rarity = self.hero_data['equipment'][slot_type].get('rarity', '').lower()
                if rarity == 'common': slot_color = (192, 192, 192)  # Grey
                elif rarity == 'rare': slot_color = (100, 149, 237)  # Blue
                elif rarity == 'epic': slot_color = (147, 112, 219)  # Purple
                elif rarity == 'prototype': slot_color = (40, 40, 40)  # Black
            
            pygame.draw.rect(self.screen, slot_color, slot)
            pygame.draw.rect(self.screen, (100, 100, 100), slot, 2)
            
            # Draw equipped item image
            if slot_type in self.equipment_images:
                image = self.equipment_images[slot_type]
                image_rect = image.get_rect(center=slot.center)
                self.screen.blit(image, image_rect)
            
            # Draw slot label
            text = self.small_font.render(label, True, (0, 0, 0))
            text_rect = text.get_rect(centerx=slot.centerx, bottom=slot.top - 5)
            self.screen.blit(text, text_rect)
        
        # Draw inventory section (always visible in Stage 2)
        inventory_title = self.font.render("Inventory", True, (0, 0, 0))
        self.screen.blit(inventory_title, (20, self.augment_slot.bottom + 20))
        
        # Draw inventory items
        self.draw_inventory()
        
        # Replace back button with actual back button
        self.back_button.x = 20
        self.back_button.y = self.inventory_panel.bottom + 15
        pygame.draw.rect(self.screen, (200, 200, 200), self.back_button)
        pygame.draw.rect(self.screen, (100, 100, 100), self.back_button, 2)
        back_text = self.small_font.render("Back", True, (0, 0, 0))
        text_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, text_rect)
        
        # Draw secretary button based on current state
        pygame.draw.rect(self.screen, (200, 200, 200), self.secretary_button)
        if self.is_secretary and self.secretary_button_selected:
            self.screen.blit(self.secretary_button_selected, self.secretary_button)
        elif not self.is_secretary and self.secretary_button_unselected:
            self.screen.blit(self.secretary_button_unselected, self.secretary_button)
        else:
            sec_text = self.small_font.render("SEC", True, (0, 0, 0))
            sec_rect = sec_text.get_rect(center=self.secretary_button.center)
            self.screen.blit(sec_text, sec_rect)
        
        # Draw tooltip using the Tooltip class
        self.tooltip.draw(self.screen)
        
        pygame.display.flip()
    
    def draw_inventory(self):
        # Position inventory panel to align with main left panel
        left_panel_x = 10
        left_panel_y = 10
        left_panel_width = 800 - self.full_image_scaled.get_width() - 30 if hasattr(self, 'full_image_scaled') else 430
        left_panel_height = 550
        
        # Align inventory with left panel bottom
        self.inventory_panel.x = left_panel_x
        self.inventory_panel.y = self.augment_slot.bottom + 50
        self.inventory_panel.width = left_panel_width
        # Make the inventory panel align perfectly with the bottom of the left panel
        self.inventory_panel.height = (left_panel_y + left_panel_height) - self.inventory_panel.y
        
        # Draw only inventory panel border (no fill)
        pygame.draw.rect(self.screen, (100, 100, 100), self.inventory_panel, 2)
        
        # Draw items
        self.inventory_rects = []
        item_size = 60
        spacing = 10
        items_per_row = 5
        start_x = self.inventory_panel.x + 10
        start_y = self.inventory_panel.y + 10
        
        for i, item in enumerate(self.inventory_items):
            row = i // items_per_row
            col = i % items_per_row
            
            # Apply scroll offset to y position
            item_y = start_y + row * (item_size + spacing) - self.scroll_offset
            
            # Skip items that would be above or below the visible area
            if item_y + item_size < self.inventory_panel.y or item_y > self.inventory_panel.y + self.inventory_panel.height:
                self.inventory_rects.append(None)
                continue
            
            item_rect = pygame.Rect(start_x + col * (item_size + spacing), item_y, item_size, item_size)
            self.inventory_rects.append(item_rect)
            
            # Draw item background with rarity color
            rarity = item.get('rarity', '').lower()
            border_color = (100, 100, 100)  # Default
            if rarity == 'common': border_color = (192, 192, 192)  # Grey
            elif rarity == 'rare': border_color = (100, 149, 237)  # Blue
            elif rarity == 'epic': border_color = (147, 112, 219)  # Purple
            elif rarity == 'prototype': border_color = (40, 40, 40)  # Black
            
            pygame.draw.rect(self.screen, (220, 220, 220), item_rect)
            pygame.draw.rect(self.screen, border_color, item_rect, 3)
            
            # Draw item image
            try:
                slot_type = item.get('slot', 'gear').lower()
                # Use a default image name based on the item name if no image field exists
                image_name = item.get('image', f"{item['name'].lower().replace(' ', '_')}.png")
                image_path = f"items/{slot_type}/{image_name}"
                image = load_image(image_path)
                scaled_image = pygame.transform.scale(image, (item_size-10, item_size-10))
                self.screen.blit(scaled_image, (item_rect.x+5, item_rect.y+5))
                
                # Draw level indicator for all items
                level = item.get('level', 1)
                level_circle_pos = (item_rect.right - 12, item_rect.bottom - 12)
                pygame.draw.circle(self.screen, border_color, level_circle_pos, 10)
                level_text = self.small_font.render(str(level), True, (255, 255, 255))
                level_rect = level_text.get_rect(center=level_circle_pos)
                self.screen.blit(level_text, level_rect)
            except Exception as e:
                print(f"Error drawing inventory item: {e}")
    
    def load_inventory_items(self):
        # Load all inventory items (Stage 2 shows all items)
        inventory = get_inventory()
        self.inventory_items = inventory.get("items", [])
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEMOTION:
                # Hide tooltip first
                self.tooltip.hide()
                
                # Check equipment slots for tooltips
                for slot, slot_type in [
                    (self.augment_slot, "augment"),
                    (self.gear_slot, "gear"),
                    (self.stim_slot, "stim")
                ]:
                    if slot.collidepoint(event.pos):
                        self.show_tooltip(event.pos, slot_type)
                        break
                
                # Check inventory items for tooltips
                for i, rect in enumerate(self.inventory_rects):
                    if rect and rect.collidepoint(event.pos) and i < len(self.inventory_items):
                        item = self.inventory_items[i]
                        tooltip_text = self.generate_tooltip_text(item)
                        self.show_tooltip(event.pos, None, tooltip_text)
                        break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                # Check if item window should open
                if event.button == 1:  # Left click
                    # Check equipment slots
                    for slot_type, slot in self.equipment_slots.items():
                        if slot.collidepoint(mouse_pos) and self.hero_data.get('equipment', {}).get(slot_type):
                            # Show item window for equipped item
                            item = self.hero_data['equipment'][slot_type]
                            show_item_window(self.screen, item, self.hero_data, True)
                            self.load_inventory_items()  # Reload inventory after window closes
                            self.load_equipment_images()  # Reload equipment images
                            return True
                    
                    # Check inventory items
                    for i, rect in enumerate(self.inventory_rects):
                        if rect and rect.collidepoint(mouse_pos) and i < len(self.inventory_items):
                            # Show item window for inventory item
                            item = self.inventory_items[i]
                            show_item_window(self.screen, item)
                            self.load_inventory_items()  # Reload inventory after window closes
                            return True
                
                # Check back button
                if self.back_button.collidepoint(event.pos):
                    return False
                
                # Handle mouse wheel for scrolling inventory
                if event.button == 4:  # Scroll up
                    self.scroll_offset = max(0, self.scroll_offset - 20)
                    self.draw()
                elif event.button == 5:  # Scroll down
                    self.scroll_offset += 20
                    self.draw()
                
                # Check for equipment slot right-clicks
                if event.button == 3:  # Right click
                    for slot, slot_type in [
                        (self.augment_slot, "augment"),
                        (self.gear_slot, "gear"),
                        (self.stim_slot, "stim")
                    ]:
                        if slot.collidepoint(event.pos):
                            # If slot has an item, unequip it
                            if self.check_equipped(slot_type):
                                self.unequip_item(slot_type)
                                self.load_inventory_items()  # Reload inventory
                                self.draw()
                            break
                
                # Check inventory items for right-click to equip
                if event.button == 3:  # Right click
                    for i, rect in enumerate(self.inventory_rects):
                        if rect and rect.collidepoint(event.pos) and i < len(self.inventory_items):
                            # Equip the clicked item
                            item = self.inventory_items[i]
                            slot_type = item.get('slot', 'gear').lower()
                            self.equip_item(item, slot_type)
                            self.load_inventory_items()  # Reload inventory
                            self.draw()
                            break

                # Check level up button
                if hasattr(self, 'level_up_button') and self.level_up_button.collidepoint(mouse_pos):
                    if can_level_up(self.hero_data):
                        if level_up(self.hero_data):
                            # Refresh the display
                            self.draw()
                        return True
                
                # Check rank up button
                if hasattr(self, 'rank_up_button') and self.rank_up_button.collidepoint(mouse_pos):
                    if can_rank_up(self.hero_data):
                        if rank_up(self.hero_data):
                            # Refresh the display
                            self.draw()
                        return True
                
                # Check secretary button
                if self.secretary_button.collidepoint(mouse_pos):
                    self.set_as_secretary()

                # Check if home button clicked
                if self.home_button.collidepoint(mouse_pos):
                    self.screen_manager.set_home()
                    return True
        
        return True
    
    def show_tooltip(self, position, slot_type=None, custom_text=None):
        if custom_text:
            tooltip_text = custom_text
        elif slot_type:
            # Generate tooltip text for the slot
            if self.hero_data.get('equipment', {}).get(slot_type):
                item = self.hero_data['equipment'][slot_type]
                tooltip_text = self.generate_tooltip_text(item)
            else:
                # Default tooltips for empty slots
                if slot_type == "augment":
                    tooltip_text = "Augment: Boosts Attack"
                elif slot_type == "gear":
                    tooltip_text = "Gear: Enhances Armour"
                elif slot_type == "stim":
                    tooltip_text = "Stim: Enhances HP"
        else:
            return
        
        # Update tooltip text and show it at cursor position
        self.tooltip.update_text(tooltip_text)
        self.tooltip.show((position[0] + 15, position[1] + 15))
    
    def generate_tooltip_text(self, item):
        # Ensure we have a dictionary
        item = ensure_dict_format(item)
        if not item:
            return "No item information available"
            
        result = f"{item['name']} ({item['rarity']})\n"
        
        # Calculate stats based on level
        from utils.item_manager import calculate_item_stats
        actual_stats = calculate_item_stats(item)
        
        # Add stats
        for stat, value in actual_stats.items():
            result += f"{stat}: +{value}\n"
        
        # Add ability if present
        if item.get('ability') and item['ability'] != "None":
            result += f"\nAbility: {item['ability']}"
            desc = get_ability_description(item['ability'])
            if desc:
                result += f"\n{desc}"
        
        # Add level if present
        result += f"\nLevel: {item.get('level', 1)}"
        
        return result
    
    def check_equipped(self, slot_type):
        """Check if an item is equipped in the given slot"""
        return bool(self.hero_data.get('equipment', {}).get(slot_type))
    
    def unequip_item(self, slot_type):
        """Unequip an item from a slot"""
        if not self.hero_data['equipment'].get(slot_type):
            return
            
        # Add to inventory
        item = self.hero_data['equipment'][slot_type]
        inventory_add(item)
        
        # Remove from hero
        self.hero_data['equipment'][slot_type] = None
        
        # Update stats
        self.calculate_stats()
        
        # Update graphics
        if slot_type in self.equipment_images:
            del self.equipment_images[slot_type]
        
        # Save changes
        self.update_player()

    def equip_item(self, item, slot_type):
        """Equip an item to a slot"""
        # Ensure item is properly formatted
        item = ensure_dict_format(item)
        
        # Unequip existing item if any
        if self.hero_data['equipment'].get(slot_type):
            self.unequip_item(slot_type)
            
        # Equip the new item
        self.hero_data['equipment'][slot_type] = item
        
        # Remove from inventory
        inventory_remove(item["id"])
        
        # Update stats
        self.calculate_stats()
        
        # Update graphics
        try:
            image_path = f"items/{slot_type}/{item['image']}"
            image = load_image(image_path)
            scaled_image = pygame.transform.scale(image, (self.slot_size[0]-10, self.slot_size[1]-10))
            self.equipment_images[slot_type] = scaled_image
        except Exception as e:
            print(f"Error loading equipment image: {e}")
        
        # Save changes
        self.update_player()

    def calculate_stats(self):
        """Calculate combined stats from base stats and equipment"""
        self.hero_data['combined_stats'] = calculate_combined_stats(
            self.hero_data.get('current_stats', self.hero_data.get('level_1_stats', {})),
            self.hero_data['equipment'],
            self.hero_data
        )

    def update_player(self):
        """Save hero data to heroes.json"""
        heroes_path = os.path.join(DATA_DIR, "player", "heroes.json")
        
        try:
            with open(heroes_path, 'r') as f:
                heroes_data = json.load(f)
                
            for hero in heroes_data["heroes"]:
                if hero["name"] == self.hero_data["name"]:
                    hero["equipment"] = self.hero_data["equipment"]
                    
                    # Update abilities list from equipped items
                    hero["abilities"] = []
                    for slot, item in self.hero_data["equipment"].items():
                        if item and item.get("ability") and item["ability"] != "None":
                            hero["abilities"].append(item["ability"])
                    
                    # Calculate and store combined stats
                    base_stats = self.hero_data.get('level_1_stats', {})
                    hero["combined_stats"] = calculate_combined_stats(base_stats, self.hero_data['equipment'])
                    break
                    
            with open(heroes_path, 'w') as f:
                json.dump(heroes_data, f, indent=2)
        except Exception as e:
            print(f"Error saving hero data: {e}")
            
    def set_as_secretary(self):
        """Set or unset this hero as secretary"""
        try:
            # Create player directory if needed
            os.makedirs(os.path.join(DATA_DIR, "player"), exist_ok=True)
            secretary_path = os.path.join(DATA_DIR, "player", "secretary.json")
            
            # Make sure the hero has an ID (use name if no ID)
            hero_id = self.hero_data.get("id", self.hero_data.get("name"))
            if not hero_id:
                print("Error: Hero has no ID or name")
                return
                
            if self.check_if_secretary():
                # Unset as secretary
                if os.path.exists(secretary_path):
                    os.remove(secretary_path)
                # No notifications, just update state
                self.is_secretary = False
            else:
                # Set as secretary
                with open(secretary_path, "w") as f:
                    json.dump({"hero_id": hero_id}, f)
                # No notifications, just update state
                self.is_secretary = True
                    
        except Exception as e:
            print(f"Error setting secretary: {e}")

    def check_if_secretary(self):
        """Check if this hero is the current secretary"""
        try:
            secretary_path = os.path.join(DATA_DIR, "player", "secretary.json")
            if os.path.exists(secretary_path):
                with open(secretary_path, "r") as f:
                    data = json.load(f)
                    return data.get("hero_id") == self.hero_data.get("id")
        except Exception as e:
            print(f"Error checking secretary status: {e}")
        return False
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()