# src/entities/drones/drone_base.py
from src.utils.logger import logger

class DroneBase:
    def __init__(self, x, y):
        # Position and movement
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.radius = 10
        
        # Drone stats
        self.health = 30
        self.max_health = 30
        self.active = True
        
        # Drone behavior
        self.target_x = x
        self.target_y = y
        self.follow_distance = 100  # Distance to keep from the ship
        self.speed = 3.0
        
    def update(self, physics, ship):
        """Update drone position and behavior"""
        try:
            # Basic following behavior
            self.follow_ship(ship)
            physics.update_position(self)
        except Exception as e:
            logger.error(f"Error updating drone: {str(e)}")
    
    def follow_ship(self, ship):
        """Simple behavior to follow the ship at a distance"""
        try:
            # Calculate vector to ship
            dx = ship.x - self.x
            dy = ship.y - self.y
            distance = (dx**2 + dy**2)**0.5
            
            # If too far, move toward ship
            if distance > self.follow_distance:
                # Normalize direction
                if distance > 0:
                    dx /= distance
                    dy /= distance
                
                # Set velocity toward ship
                self.velocity_x = dx * self.speed
                self.velocity_y = dy * self.speed
            else:
                # Slow down when close enough
                self.velocity_x *= 0.9
                self.velocity_y *= 0.9
        except Exception as e:
            logger.error(f"Error in drone following behavior: {str(e)}")
    
    def take_damage(self, amount):
        """Apply damage to drone"""
        try:
            self.health -= amount
            if self.health <= 0:
                self.active = False
                return True  # Destroyed
            return False
        except Exception as e:
            logger.error(f"Error applying damage to drone: {str(e)}")
            return False