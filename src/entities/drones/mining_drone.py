# src/entities/drones/mining_drone.py
import math
import pygame
from src.entities.drones.drone_base import DroneBase
from src.utils.logger import logger

class MiningDrone(DroneBase):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # Mining properties
        self.mining_range = 100
        self.mining_rate = 0.5
        self.current_cargo = 0
        self.cargo_capacity = 30
        self.target_resource = None
        
        # Visual properties
        self.color = (150, 150, 50)  # Yellow for mining
        self.drone_type = "mining_drone"  # Used for asset loading
        self.animation_frame = 0
        self.max_frames = 4
        self.animation_speed = 0.1
        self.animation_counter = 0
        self.mining_active = False
        
    def update(self, physics, ship, resources=None):
        """Update mining drone behavior"""
        try:
            # Base behavior first
            super().update(physics, ship)
            
            # Update animation
            self.animation_counter += self.animation_speed
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.animation_frame = (self.animation_frame + 1) % self.max_frames
            
            # Mining behavior
            if resources:
                self.mine_resources(resources)
                
            # Return to ship if cargo full
            if self.current_cargo >= self.cargo_capacity:
                # Extra force toward ship for return
                self.follow_distance = 20  # Get closer to ship to transfer
            else:
                self.follow_distance = 100  # Normal follow distance
                
            # Try to transfer cargo if close to ship
            if self.current_cargo > 0:
                dx = ship.x - self.x
                dy = ship.y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance < 30:
                    self.transfer_cargo_to_ship(ship)
            
            return None
        except Exception as e:
            logger.error(f"Error updating mining drone: {str(e)}")
            return None
    
    def mine_resources(self, resources):
        """Find and mine resources"""
        try:
            # Reset mining status
            self.mining_active = False
            
            # If we have a target resource, check if it's still valid
            if self.target_resource:
                # Check if target still exists
                if self.target_resource not in resources or self.target_resource.amount <= 0:
                    self.target_resource = None
            
            # Find a resource to mine if we don't have one
            if not self.target_resource and self.current_cargo < self.cargo_capacity:
                # Find closest valid resource
                closest_dist = float('inf')
                for resource in resources:
                    if resource.amount <= 0 or not resource.detected:
                        continue
                        
                    dx = resource.x - self.x
                    dy = resource.y - self.y
                    distance = math.sqrt(dx**2 + dy**2)
                    
                    if distance < closest_dist:
                        closest_dist = distance
                        self.target_resource = resource
            
            # If we have a target, mine it
            if self.target_resource and self.current_cargo < self.cargo_capacity:
                dx = self.target_resource.x - self.x
                dy = self.target_resource.y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                
                # Move toward resource if not close enough
                if distance > 20:
                    norm_dx = dx / distance
                    norm_dy = dy / distance
                    self.velocity_x = norm_dx * self.speed
                    self.velocity_y = norm_dy * self.speed
                else:
                    # Mine the resource
                    self.mining_active = True
                    mine_amount = min(
                        self.mining_rate,
                        self.target_resource.amount,
                        self.cargo_capacity - self.current_cargo
                    )
                    
                    if mine_amount > 0:
                        self.target_resource.amount -= mine_amount
                        self.current_cargo += mine_amount
                        
                        # If resource is depleted, clear target
                        if self.target_resource.amount <= 0:
                            self.target_resource = None
        except Exception as e:
            logger.error(f"Error mining resources: {str(e)}")
    
    def transfer_cargo_to_ship(self, ship):
        """Transfer mined resources to the ship"""
        try:
            # Add to ship cargo
            # For simplicity, assume all mined resources are "metal"
            resource_type = "metal"
            
            # Check ship cargo capacity
            current_ship_cargo = sum(ship.cargo.values())
            transfer_amount = min(self.current_cargo, ship.max_cargo - current_ship_cargo)
            
            if transfer_amount > 0:
                if resource_type in ship.cargo:
                    ship.cargo[resource_type] += transfer_amount
                else:
                    ship.cargo[resource_type] = transfer_amount
                    
                self.current_cargo -= transfer_amount
        except Exception as e:
            logger.error(f"Error transferring cargo: {str(e)}")
    
    def render(self, renderer, camera_x, camera_y):
        """Custom rendering method for mining drone"""
        try:
            screen_x = self.x - camera_x
            screen_y = self.y - camera_y
            
            # Only render if on screen
            if (-self.radius <= screen_x <= renderer.width + self.radius and
                -self.radius <= screen_y <= renderer.height + self.radius):
                
                # Use the new renderer method for drones
                renderer.draw_drone(screen_x, screen_y, self.drone_type, self.radius)
                
                # Draw line to target resource if mining
                if self.target_resource:
                    resource_screen_x = self.target_resource.x - camera_x
                    resource_screen_y = self.target_resource.y - camera_y
                    
                    # Draw dotted line to target
                    if self.mining_active:
                        # Solid line when actively mining
                        pygame.draw.line(
                            renderer.screen,
                            (180, 180, 60),  # Yellow
                            (int(screen_x), int(screen_y)),
                            (int(resource_screen_x), int(resource_screen_y)),
                            2  # Width
                        )
                    else:
                        # Dotted line when moving to resource
                        dash_length = 5
                        space_length = 5
                        total_length = dash_length + space_length
                        
                        dx = resource_screen_x - screen_x
                        dy = resource_screen_y - screen_y
                        distance = math.sqrt(dx**2 + dy**2)
                        
                        if distance > 0:
                            dx /= distance
                            dy /= distance
                            
                            # Draw dashed line
                            current_pos = (screen_x, screen_y)
                            remaining = distance
                            drawing = True
                            
                            while remaining > 0:
                                segment = min(dash_length if drawing else space_length, remaining)
                                next_pos = (
                                    current_pos[0] + dx * segment,
                                    current_pos[1] + dy * segment
                                )
                                
                                if drawing:
                                    pygame.draw.line(
                                        renderer.screen,
                                        (180, 180, 60),  # Yellow
                                        (int(current_pos[0]), int(current_pos[1])),
                                        (int(next_pos[0]), int(next_pos[1])),
                                        1  # Width
                                    )
                                
                                current_pos = next_pos
                                remaining -= segment
                                drawing = not drawing
                
                # Draw cargo indicator
                if self.current_cargo > 0:
                    # Draw cargo fill level
                    fill_percent = self.current_cargo / self.cargo_capacity
                    bar_width = 20
                    bar_height = 4
                    
                    # Background
                    renderer.draw_rectangle(
                        screen_x - bar_width/2,
                        screen_y + self.radius + 2,
                        bar_width,
                        bar_height,
                        (50, 50, 50)
                    )
                    
                    # Fill
                    renderer.draw_rectangle(
                        screen_x - bar_width/2,
                        screen_y + self.radius + 2,
                        bar_width * fill_percent,
                        bar_height,
                        (200, 180, 50)
                    )
        except Exception as e:
            logger.error(f"Error rendering mining drone: {str(e)}")
            # Fallback to simple circle if rendering fails
            renderer.draw_circle(screen_x, screen_y, self.radius, self.color)