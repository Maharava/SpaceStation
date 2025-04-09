# src/entities/drones/scanner_drone.py
import math
import pygame
from src.entities.drones.drone_base import DroneBase
from src.utils.logger import logger

class ScannerDrone(DroneBase):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # Scanner properties
        self.scan_radius = 250
        self.scan_cooldown = 0
        self.scan_cooldown_max = 60
        self.scan_active = False
        self.scan_duration = 20
        self.scan_timer = 0
        
        # Visual properties
        self.color = (50, 200, 255)  # Blue for scanner
        self.drone_type = "scanner_drone"  # Used for asset loading
        self.animation_frame = 0
        self.max_frames = 4
        self.animation_speed = 0.1
        self.animation_counter = 0
        self.pulse_size = 0  # For scan pulse effect
        
    def update(self, physics, ship):
        """Update scanner drone behavior"""
        try:
            # First perform base drone update
            super().update(physics, ship)
            
            # Handle scanning cooldown
            if self.scan_cooldown > 0:
                self.scan_cooldown -= 1
                
            # Update scan animation if active
            if self.scan_active:
                self.scan_timer -= 1
                self.pulse_size = (self.scan_duration - self.scan_timer) * (self.scan_radius / self.scan_duration)
                if self.scan_timer <= 0:
                    self.scan_active = False
                    self.pulse_size = 0
            
            # Update animation
            self.animation_counter += self.animation_speed
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.animation_frame = (self.animation_frame + 1) % self.max_frames
            
            return {
                'scan_active': self.scan_active,
                'scan_radius': self.scan_radius,
                'x': self.x,
                'y': self.y
            }
        except Exception as e:
            logger.error(f"Error updating scanner drone: {str(e)}")
            return None
    
    def perform_scan(self):
        """Initiate a scan if cooldown allows"""
        try:
            if self.scan_cooldown <= 0 and not self.scan_active:
                self.scan_active = True
                self.scan_timer = self.scan_duration
                self.scan_cooldown = self.scan_cooldown_max
                self.pulse_size = 0  # Reset pulse
                return True
            return False
        except Exception as e:
            logger.error(f"Error performing scan: {str(e)}")
            return False
    
    def detect_resources(self, resources):
        """Return resources within scan radius"""
        try:
            detected = []
            
            for resource in resources:
                dx = resource.x - self.x
                dy = resource.y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance <= self.scan_radius:
                    resource.detected = True
                    detected.append(resource)
            
            return detected
        except Exception as e:
            logger.error(f"Error detecting resources: {str(e)}")
            return []
    
    def render(self, renderer, camera_x, camera_y):
        """Custom rendering method for scanner drone"""
        try:
            screen_x = self.x - camera_x
            screen_y = self.y - camera_y
            
            # Only render if on screen
            if (-self.radius <= screen_x <= renderer.width + self.radius and
                -self.radius <= screen_y <= renderer.height + self.radius):
                
                # Use the new renderer method for drones
                renderer.draw_drone(screen_x, screen_y, self.drone_type, self.radius)
                
                # Draw scan pulse if active
                if self.scan_active and self.pulse_size > 0:
                    # Calculating alpha (transparency) based on pulse size
                    # Fade out as the pulse expands
                    alpha = max(0, 255 - int(255 * (self.pulse_size / self.scan_radius)))
                    
                    # Create a surface for the transparent circle
                    surf = pygame.Surface((self.pulse_size * 2, self.pulse_size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(
                        surf,
                        (50, 200, 255, alpha),  # Blue with alpha
                        (self.pulse_size, self.pulse_size),
                        self.pulse_size,
                        2  # Width of the circle line
                    )
                    
                    # Blit the surface onto the screen
                    renderer.screen.blit(
                        surf,
                        (screen_x - self.pulse_size, screen_y - self.pulse_size)
                    )
                
                # Draw scan radius indicator when cooldown is ready
                if self.scan_cooldown <= 0 and not self.scan_active:
                    # Draw dotted circle to show scan radius
                    points = []
                    num_points = 36
                    for i in range(num_points):
                        angle = 2 * math.pi * i / num_points
                        px = screen_x + math.cos(angle) * self.scan_radius
                        py = screen_y + math.sin(angle) * self.scan_radius
                        if i % 2 == 0:  # Only draw every other point for dotted effect
                            points.append((px, py))
                    
                    # Draw points
                    for point in points:
                        pygame.draw.circle(
                            renderer.screen,
                            (50, 200, 255),  # Blue
                            (int(point[0]), int(point[1])),
                            2
                        )
        except Exception as e:
            logger.error(f"Error rendering scanner drone: {str(e)}")
            # Fallback to simple circle if rendering fails
            renderer.draw_circle(screen_x, screen_y, self.radius, self.color)