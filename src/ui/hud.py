# src/ui/hud.py
import pygame
from src.utils.logger import logger

class HUD:
    def __init__(self, renderer):
        self.renderer = renderer
        self.font = pygame.font.SysFont("Arial", 16)
        self.header_font = pygame.font.SysFont("Arial", 20, bold=True)
    
    def render(self, ship, mission, screen_width, screen_height):
        """Render the heads-up display during gameplay"""
        try:
            # Ship stats (top left)
            self.render_ship_stats(ship, 10, 10)
            
            # Resources/cargo (top right)
            self.render_cargo(ship, screen_width - 150, 10)
            
            # Mission objectives (bottom left)
            self.render_mission_objectives(mission, 10, screen_height - 100)
            
            # Minimap could go in the bottom right but omitted for now
        except Exception as e:
            logger.error(f"Error rendering HUD: {str(e)}")
    
    def render_ship_stats(self, ship, x, y):
        """Render ship statistics"""
        try:
            # Background panel
            self.renderer.draw_rectangle(x, y, 150, 80, (0, 0, 0, 128))
            
            # Ship stats
            health_text = f"Health: {ship.health}/{ship.max_health}"
            energy_text = f"Energy: {int(ship.energy)}/{ship.max_energy}"
            shield_text = f"Shield: {ship.shield}/{ship.max_shield}"
            drone_text = f"Drones: {len(ship.active_drones)}/{ship.max_drones}"
            
            self.renderer.draw_text("SHIP STATUS", x + 5, y + 5)
            self.renderer.draw_text(health_text, x + 10, y + 25)
            self.renderer.draw_text(energy_text, x + 10, y + 40)
            self.renderer.draw_text(shield_text, x + 10, y + 55)
            self.renderer.draw_text(drone_text, x + 10, y + 70)
        except Exception as e:
            logger.error(f"Error rendering ship stats: {str(e)}")
    
    def render_cargo(self, ship, x, y):
        """Render cargo/resource information"""
        try:
            # Background panel
            panel_height = 20 + len(ship.cargo) * 15
            self.renderer.draw_rectangle(x, y, 150, panel_height, (0, 0, 0, 128))
            
            # Cargo header
            self.renderer.draw_text("CARGO", x + 5, y + 5)
            
            # List resources
            y_offset = 25
            for resource_type, amount in ship.cargo.items():
                text = f"{resource_type}: {amount}"
                self.renderer.draw_text(text, x + 10, y + y_offset)
                y_offset += 15
                
            # If empty
            if not ship.cargo:
                self.renderer.draw_text("Empty", x + 10, y + y_offset)
        except Exception as e:
            logger.error(f"Error rendering cargo: {str(e)}")
    
    def render_mission_objectives(self, mission, x, y):
        """Render mission objectives"""
        try:
            if not mission or not mission.objectives:
                return
                
            # Background panel
            panel_height = 30 + len(mission.objectives) * 20
            self.renderer.draw_rectangle(x, y, 300, panel_height, (0, 0, 0, 128))
            
            # Mission header
            self.renderer.draw_text("OBJECTIVES", x + 5, y + 5)
            
            # List objectives
            y_offset = 25
            for objective in mission.objectives:
                # Format objective text
                text = objective.get('description', 'Unknown objective')
                
                # Add status marker
                if objective['completed']:
                    status = "✓"
                    color = (100, 255, 100)  # Green for completed
                else:
                    status = "○"
                    color = (255, 255, 255)  # White for incomplete
                
                self.renderer.draw_text(f"{status} {text}", x + 10, y + y_offset, color)
                y_offset += 20
        except Exception as e:
            logger.error(f"Error rendering mission objectives: {str(e)}")