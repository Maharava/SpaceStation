# src/ui/station_interface.py
import pygame
from src.utils.logger import logger

class StationInterface:
    def __init__(self, renderer):
        self.renderer = renderer
        self.font = pygame.font.SysFont("Arial", 18)
        self.header_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.current_screen = "main"  # Current screen: main, shipyard, drone_bay, etc.
        
        # Define sections/modules of the station
        self.modules = {
            "shipyard": {"name": "Shipyard", "available": True},
            "drone_bay": {"name": "Drone Bay", "available": True},
            "quarters": {"name": "Quarters", "available": True},
            "mission_control": {"name": "Mission Control", "available": True}
        }
        
        # Ship upgrade options
        self.ship_upgrades = {
            "engine": {"name": "Engine Boost", "cost": {"metal": 20}, "effect": "Speed +10%"},
            "shield": {"name": "Shield Generator", "cost": {"crystal": 15}, "effect": "Shield +20"},
            "cargo": {"name": "Cargo Hold", "cost": {"metal": 15}, "effect": "Cargo +20"},
            "weapon": {"name": "Weapon System", "cost": {"tech": 10}, "effect": "Damage +15%"}
        }
    
    def handle_event(self, event, ship, drones, survivor):
        """Process station interface input events"""
        try:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mx, my = event.pos
                    
                    # Handle module selection on main screen
                    if self.current_screen == "main":
                        y_pos = 150
                        for module_id, module in self.modules.items():
                            if module["available"] and 150 <= mx <= 650 and y_pos <= my <= y_pos + 60:
                                self.current_screen = module_id
                                return None
                            y_pos += 80
                        
                        # Back to mission button
                        if 300 <= mx <= 500 and 550 <= my <= 590:
                            return "start_mission"
                    
                    # Handle back button for submenus
                    elif 50 <= mx <= 150 and 50 <= my <= 80:
                        self.current_screen = "main"
                    
                    # Handle shipyard upgrades
                    elif self.current_screen == "shipyard":
                        y_pos = 150
                        for upgrade_id, upgrade in self.ship_upgrades.items():
                            if 150 <= mx <= 650 and y_pos <= my <= y_pos + 60:
                                # Check if player can afford the upgrade
                                can_afford = True
                                for resource, amount in upgrade["cost"].items():
                                    if resource not in ship.cargo or ship.cargo[resource] < amount:
                                        can_afford = False
                                        break
                                
                                if can_afford:
                                    # Apply upgrade
                                    if upgrade_id == "engine":
                                        ship.speed *= 1.1
                                    elif upgrade_id == "shield":
                                        ship.max_shield += 20
                                        ship.shield = ship.max_shield
                                    elif upgrade_id == "cargo":
                                        ship.max_cargo += 20
                                    elif upgrade_id == "weapon":
                                        ship.weapon_damage *= 1.15
                                    
                                    # Deduct resources
                                    for resource, amount in upgrade["cost"].items():
                                        ship.cargo[resource] -= amount
                                
                            y_pos += 80
            
            return None
        except Exception as e:
            logger.error(f"Error handling station interface event: {str(e)}")
            return None
    
    def render(self, ship, drones, survivor):
        """Render the station interface"""
        try:
            # Clear the screen
            self.renderer.clear_screen()
            
            # Render current screen
            if self.current_screen == "main":
                self.render_main_screen()
            elif self.current_screen == "shipyard":
                self.render_shipyard(ship)
            elif self.current_screen == "drone_bay":
                self.render_drone_bay(drones)
            elif self.current_screen == "quarters":
                self.render_quarters(survivor)
            elif self.current_screen == "mission_control":
                self.render_mission_control()
            
            # Update display
            self.renderer.update_display()
        except Exception as e:
            logger.error(f"Error rendering station interface: {str(e)}")
    
    def render_main_screen(self):
        """Render the main station screen"""
        try:
            # Title
            self.renderer.draw_text("STATION COMMAND", 400, 80, center=True, font=self.header_font)
            
            # Module selection
            y_pos = 150
            for module_id, module in self.modules.items():
                bg_color = (50, 50, 80) if module["available"] else (30, 30, 50)
                self.renderer.draw_rectangle(150, y_pos, 500, 60, bg_color)
                
                # Module name
                text_color = (255, 255, 255) if module["available"] else (150, 150, 150)
                self.renderer.draw_text(module["name"], 400, y_pos + 30, center=True, color=text_color)
                
                y_pos += 80
            
            # Start mission button
            self.renderer.draw_rectangle(300, 550, 200, 40, (80, 80, 120))
            self.renderer.draw_text("START MISSION", 400, 570, center=True)
        except Exception as e:
            logger.error(f"Error rendering main station screen: {str(e)}")
    
    def render_shipyard(self, ship):
        """Render the shipyard upgrade screen"""
        try:
            # Back button
            self.renderer.draw_rectangle(50, 50, 100, 30, (50, 50, 80))
            self.renderer.draw_text("< Back", 100, 65, center=True)
            
            # Title
            self.renderer.draw_text("SHIPYARD", 400, 80, center=True, font=self.header_font)
            
            # Ship status
            self.renderer.draw_text(f"Health: {ship.health}/{ship.max_health}", 150, 120)
            self.renderer.draw_text(f"Shield: {ship.shield}/{ship.max_shield}", 350, 120)
            self.renderer.draw_text(f"Cargo: {sum(ship.cargo.values())}/{ship.max_cargo}", 550, 120)
            
            # Available upgrades
            y_pos = 150
            for upgrade_id, upgrade in self.ship_upgrades.items():
                # Check if player can afford
                can_afford = True
                for resource, amount in upgrade["cost"].items():
                    if resource not in ship.cargo or ship.cargo[resource] < amount:
                        can_afford = False
                        break
                
                # Button color based on affordability
                bg_color = (50, 80, 50) if can_afford else (80, 50, 50)
                self.renderer.draw_rectangle(150, y_pos, 500, 60, bg_color)
                
                # Upgrade name and effect
                self.renderer.draw_text(upgrade["name"], 170, y_pos + 15)
                self.renderer.draw_text(upgrade["effect"], 170, y_pos + 35)
                
                # Cost
                cost_text = "Cost: "
                for resource, amount in upgrade["cost"].items():
                    cost_text += f"{amount} {resource}, "
                cost_text = cost_text[:-2]  # Remove trailing comma
                
                self.renderer.draw_text(cost_text, 400, y_pos + 25)
                
                y_pos += 80
        except Exception as e:
            logger.error(f"Error rendering shipyard: {str(e)}")
    
    def render_drone_bay(self, drones):
        """Render the drone management screen"""
        try:
            # Back button
            self.renderer.draw_rectangle(50, 50, 100, 30, (50, 50, 80))
            self.renderer.draw_text("< Back", 100, 65, center=True)
            
            # Title
            self.renderer.draw_text("DRONE BAY", 400, 80, center=True, font=self.header_font)
            
            # Display available drones
            y_pos = 150
            if drones:
                for i, drone in enumerate(drones):
                    bg_color = (50, 50, 80)
                    self.renderer.draw_rectangle(150, y_pos, 500, 60, bg_color)
                    
                    # Drone type and status
                    drone_type = "Scanner Drone" if isinstance(drone, ScannerDrone) else "Combat Drone"
                    self.renderer.draw_text(f"{drone_type} {i+1}", 170, y_pos + 15)
                    self.renderer.draw_text(f"Health: {drone.health}/{drone.max_health}", 170, y_pos + 35)
                    
                    y_pos += 80
            else:
                self.renderer.draw_text("No drones available", 400, 200, center=True)
        except Exception as e:
            logger.error(f"Error rendering drone bay: {str(e)}")
    
    def render_quarters(self, survivor):
        """Render the survivor quarters screen"""
        try:
            # Back button
            self.renderer.draw_rectangle(50, 50, 100, 30, (50, 50, 80))
            self.renderer.draw_text("< Back", 100, 65, center=True)
            
            # Title
            self.renderer.draw_text("CREW QUARTERS", 400, 80, center=True, font=self.header_font)
            
            # Display survivor information if available
            if survivor and survivor.rescued:
                # Survivor portrait placeholder
                self.renderer.draw_rectangle(150, 150, 100, 100, (60, 60, 90))
                
                # Survivor info
                self.renderer.draw_text(f"Name: {survivor.name}", 280, 160)
                self.renderer.draw_text(f"Specialty: {survivor.specialty}", 280, 185)
                
                # Dialog box
                self.renderer.draw_rectangle(150, 270, 500, 100, (40, 40, 60))
                self.renderer.draw_text(survivor.get_dialog('station'), 160, 285)
                
                # Bonuses
                self.renderer.draw_text("Bonuses:", 150, 390)
                y_pos = 415
                for bonus_type, value in survivor.get_bonuses().items():
                    self.renderer.draw_text(f"{bonus_type}: +{int(value * 100)}%", 170, y_pos)
                    y_pos += 25
            else:
                self.renderer.draw_text("No survivors rescued yet", 400, 200, center=True)
        except Exception as e:
            logger.error(f"Error rendering quarters: {str(e)}")
    
    def render_mission_control(self):
        """Render the mission control screen"""
        try:
            # Back button
            self.renderer.draw_rectangle(50, 50, 100, 30, (50, 50, 80))
            self.renderer.draw_text("< Back", 100, 65, center=True)
            
            # Title
            self.renderer.draw_text("MISSION CONTROL", 400, 80, center=True, font=self.header_font)
            
            # Simple mission selection
            mission_types = [
                {"name": "Exploration", "description": "Explore a new sector for resources"},
                {"name": "Rescue", "description": "Find and rescue a stranded survivor"},
                {"name": "Collection", "description": "Collect specific resources"}
            ]
            
            y_pos = 150
            for mission in mission_types:
                self.renderer.draw_rectangle(150, y_pos, 500, 60, (50, 50, 80))
                self.renderer.draw_text(mission["name"], 170, y_pos + 15)
                self.renderer.draw_text(mission["description"], 170, y_pos + 35)
                y_pos += 80
        except Exception as e:
            logger.error(f"Error rendering mission control: {str(e)}")