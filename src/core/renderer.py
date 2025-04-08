import pygame
import os

class Renderer:
    def __init__(self, config):
        self.config = config
        self.width = config.get("screen_width")
        self.height = config.get("screen_height")
        self.fullscreen = config.get("fullscreen")
        
        pygame.init()
        self.setup_display()
        self.clock = pygame.time.Clock()
        self.fps = config.get("fps_cap")
        
        # For debugging
        self.font = pygame.font.SysFont("Arial", 18)
    
    def setup_display(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode(
                (self.width, self.height),
                pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode(
                (self.width, self.height)
            )
        pygame.display.set_caption("Starbound Exile: Derelict Awakening")
    
    def clear_screen(self):
        self.screen.fill((0, 0, 0))
    
    def draw_text(self, text, x, y, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def draw_rectangle(self, x, y, width, height, color):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
    
    def draw_circle(self, x, y, radius, color):
        pygame.draw.circle(self.screen, color, (x, y), radius)
    
    def update_display(self):
        pygame.display.flip()
        self.clock.tick(self.fps)
    
    def shutdown(self):
        pygame.quit()

    def load_image(self, path):
        """Load image with fallback to geometric shapes if file not found"""
        try:
            if os.path.exists(path):
                return pygame.image.load(path).convert_alpha()
            else:
                # Return None to indicate fallback should be used
                return None
        except Exception as e:
            logger.error(f"Error loading image {path}: {str(e)}")
            return None

    def draw_ship(self, x, y, rotation, radius=20):
        """Draw the player ship with image or fallback to shape"""
        ship_image = self.load_image("assets/images/ships/player_ship.png")
        
        if ship_image:
            # Calculate rotated image
            rotated_ship = pygame.transform.rotate(ship_image, -rotation)
            rect = rotated_ship.get_rect(center=(x, y))
            self.screen.blit(rotated_ship, rect)
        else:
            # Fallback to geometric shape
            self.draw_circle(x, y, radius, (0, 150, 200))
            
            # Direction indicator
            angle_rad = math.radians(rotation)
            indicator_x = x + math.cos(angle_rad) * radius
            indicator_y = y + math.sin(angle_rad) * radius
            self.draw_circle(indicator_x, indicator_y, 5, (200, 200, 50))

    def draw_drone(self, x, y, drone_type, radius=10):
        """Draw a drone with image or fallback to shape"""
        image_path = f"assets/images/drones/{drone_type}.png"
        drone_image = self.load_image(image_path)
        
        if drone_image:
            rect = drone_image.get_rect(center=(x, y))
            self.screen.blit(drone_image, rect)
        else:
            # Fallback colors based on drone type
            if drone_type == "combat_drone":
                color = (255, 50, 50)  # Red for combat
            elif drone_type == "scanner_drone":
                color = (50, 200, 255)  # Blue for scanner
            elif "mining" in drone_type:
                color = (180, 160, 60)  # Yellow for mining
            else:
                color = (200, 200, 200)  # Default gray
                
            self.draw_circle(x, y, radius, color)

    def draw_resource(self, x, y, resource_type, amount, detected=False):
        """Draw a resource with image or fallback to shape"""
        if not detected:
            return  # Don't draw undetected resources
            
        image_path = f"assets/images/resources/{resource_type}.png"
        resource_image = self.load_image(image_path)
        
        # Calculate size based on amount
        radius = 10 + amount // 10
        
        if resource_image:
            # Scale image based on amount
            scale = radius / 20  # Assuming base size is 20
            scaled_img = pygame.transform.scale(
                resource_image, 
                (int(resource_image.get_width() * scale), 
                 int(resource_image.get_height() * scale))
            )
            rect = scaled_img.get_rect(center=(x, y))
            self.screen.blit(scaled_img, rect)
        else:
            # Fallback colors by resource type
            colors = {
                'metal': (150, 150, 180),
                'crystal': (200, 100, 220),
                'energy': (100, 220, 100),
                'tech': (220, 180, 100)
            }
            color = colors.get(resource_type, (200, 200, 200))
            self.draw_circle(x, y, radius, color)

    def draw_obstacle(self, x, y, obstacle_type, radius):
        """Draw an obstacle with image or fallback to shape"""
        image_path = f"assets/images/environment/obstacles/{obstacle_type}.png"
        obstacle_image = self.load_image(image_path)
        
        if obstacle_image:
            # Scale image based on radius
            scale = radius / 20  # Assuming base size is 20
            scaled_img = pygame.transform.scale(
                obstacle_image, 
                (int(obstacle_image.get_width() * scale), 
                 int(obstacle_image.get_height() * scale))
            )
            rect = scaled_img.get_rect(center=(x, y))
            self.screen.blit(scaled_img, rect)
        else:
            # Fallback colors by obstacle type
            if obstacle_type == "asteroid":
                color = (100, 90, 80)  # Brown
            elif obstacle_type == "debris":
                color = (120, 120, 130)  # Gray
            elif obstacle_type == "ice":
                color = (200, 220, 255)  # Light blue
            else:
                color = (150, 150, 150)  # Default gray
                
            self.draw_circle(x, y, radius, color)

    def draw_poi(self, x, y, poi_type, radius=50):
        """Draw a point of interest with image or fallback to shape"""
        image_path = f"assets/images/environment/poi/{poi_type}.png"
        poi_image = self.load_image(image_path)
        
        if poi_image:
            # Scale image based on radius
            scale = radius / 25  # Assuming base size is 25
            scaled_img = pygame.transform.scale(
                poi_image, 
                (int(poi_image.get_width() * scale), 
                 int(poi_image.get_height() * scale))
            )
            rect = scaled_img.get_rect(center=(x, y))
            self.screen.blit(scaled_img, rect)
        else:
            # Fallback colors by POI type
            if poi_type == "derelict":
                color = (180, 120, 80)  # Orange
            elif poi_type == "station":
                color = (80, 180, 150)  # Teal
            elif poi_type == "anomaly":
                color = (200, 100, 200)  # Purple
            else:
                color = (200, 200, 100)  # Yellow-ish default
                
            self.draw_circle(x, y, radius, color)

    def draw_survivor(self, x, y, survivor_id, width=100, height=120):
        """Draw a survivor portrait with image or fallback to shape"""
        image_path = f"assets/images/survivors/{survivor_id}.png"
        survivor_image = self.load_image(image_path)
        
        if survivor_image:
            rect = survivor_image.get_rect(center=(x, y))
            self.screen.blit(survivor_image, rect)
        else:
            # Fallback to simple rectangle with different colors based on ID
            # Use ID to generate a semi-unique color
            id_num = int(''.join(filter(str.isdigit, survivor_id))) if any(c.isdigit() for c in survivor_id) else 1
            r = (id_num * 123) % 200 + 55
            g = (id_num * 45) % 200 + 55
            b = (id_num * 67) % 200 + 55
            
            self.draw_rectangle(x - width//2, y - height//2, width, height, (r, g, b))
            
            # Draw face features using circles
            self.draw_circle(x, y - 20, 15, (255, 220, 180))  # Face
            self.draw_circle(x - 5, y - 25, 3, (50, 50, 50))  # Left eye
            self.draw_circle(x + 5, y - 25, 3, (50, 50, 50))  # Right eye
            self.draw_circle(x, y - 15, 5, (200, 150, 150))  # Mouth

    def draw_button(self, x, y, width, height, text, is_hover=False):
        """Draw a UI button with image or fallback to shape"""
        state = "hover" if is_hover else "normal"
        image_path = f"assets/images/ui/buttons/{state}.png"
        button_image = self.load_image(image_path)
        
        if button_image:
            # Scale button to desired size
            scaled_img = pygame.transform.scale(button_image, (width, height))
            self.screen.blit(scaled_img, (x, y))
        else:
            # Fallback button
            if is_hover:
                color = (100, 150, 200)  # Lighter blue for hover
            else:
                color = (70, 120, 170)  # Darker blue for normal
                
            self.draw_rectangle(x, y, width, height, color)
            
            # Button border
            pygame.draw.rect(
                self.screen, 
                (200, 200, 220), 
                (x, y, width, height), 
                2  # Border width
            )
        
        # Draw button text
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(x + width//2, y + height//2))
        self.screen.blit(text_surf, text_rect)