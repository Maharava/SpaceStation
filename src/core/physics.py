# src/core/physics.py
import math
from src.utils.logger import logger

class Physics:
    def __init__(self):
        # Physics constants
        self.max_velocity = 8.0
        self.thrust_power = 0.2
        self.rotation_speed = 4.0
        self.friction = 0.98  # Slight dampening effect
        
    def apply_thrust(self, entity, direction_x, direction_y):
        """Apply thrust to an entity in the specified direction"""
        try:
            # Normalize direction if needed
            magnitude = math.sqrt(direction_x**2 + direction_y**2)
            if magnitude > 0:
                norm_x = direction_x / magnitude
                norm_y = direction_y / magnitude
                
                # Apply force
                entity.velocity_x += norm_x * self.thrust_power
                entity.velocity_y += norm_y * self.thrust_power
                
                # Limit max velocity
                current_speed = math.sqrt(entity.velocity_x**2 + entity.velocity_y**2)
                if current_speed > self.max_velocity:
                    ratio = self.max_velocity / current_speed
                    entity.velocity_x *= ratio
                    entity.velocity_y *= ratio
        except Exception as e:
            logger.error(f"Error applying thrust: {str(e)}")
    
    def update_position(self, entity, dt=1.0):
        """Update entity position based on velocity"""
        try:
            # Apply velocity to position
            entity.x += entity.velocity_x * dt
            entity.y += entity.velocity_y * dt
            
            # Apply friction
            entity.velocity_x *= self.friction
            entity.velocity_y *= self.friction
        except Exception as e:
            logger.error(f"Error updating position: {str(e)}")
    
    def check_collision(self, entity1, entity2):
        """Simple circle collision detection"""
        try:
            dx = entity1.x - entity2.x
            dy = entity1.y - entity2.y
            distance = math.sqrt(dx**2 + dy**2)
            return distance < (entity1.radius + entity2.radius)
        except Exception as e:
            logger.error(f"Error checking collision: {str(e)}")
            return False