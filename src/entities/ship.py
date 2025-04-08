# src/entities/ship.py
import math
from src.utils.logger import logger

class Ship:
    def __init__(self, x, y):
        # Position and movement
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.rotation = 0  # in degrees
        self.radius = 20
        
        # Ship stats
        self.health = 100
        self.max_health = 100
        self.energy = 100
        self.max_energy = 100
        self.shield = 0
        self.max_shield = 0
        
        # Weapon properties
        self.weapon_cooldown = 0
        self.weapon_cooldown_max = 10
        self.weapon_damage = 10
        self.weapon_energy_cost = 5
        
        # Drone capacity
        self.max_drones = 1
        self.active_drones = []
        
        # Cargo
        self.cargo = {}
        self.max_cargo = 100
        
    def update(self, physics):
        """Update ship state"""
        try:
            physics.update_position(self)
            
            # Handle weapon cooldown
            if self.weapon_cooldown > 0:
                self.weapon_cooldown -= 1
                
            # Regenerate energy slowly
            if self.energy < self.max_energy:
                self.energy += 0.1
                if self.energy > self.max_energy:
                    self.energy = self.max_energy
        except Exception as e:
            logger.error(f"Error updating ship: {str(e)}")
    
    def fire_weapon(self):
        """Fire ship's main weapon if possible"""
        try:
            if self.weapon_cooldown <= 0 and self.energy >= self.weapon_energy_cost:
                self.weapon_cooldown = self.weapon_cooldown_max
                self.energy -= self.weapon_energy_cost
                
                # Calculate projectile direction based on ship rotation
                angle_rad = math.radians(self.rotation)
                direction_x = math.cos(angle_rad)
                direction_y = math.sin(angle_rad)
                
                # Create projectile at ship's position
                projectile = {
                    'x': self.x + direction_x * self.radius,
                    'y': self.y + direction_y * self.radius,
                    'velocity_x': direction_x * 10 + self.velocity_x,
                    'velocity_y': direction_y * 10 + self.velocity_y,
                    'damage': self.weapon_damage,
                    'lifetime': 60  # frames
                }
                
                return projectile
            return None
        except Exception as e:
            logger.error(f"Error firing weapon: {str(e)}")
            return None
    
    def collect_resource(self, resource):
        """Add resource to cargo"""
        try:
            resource_type = resource.resource_type
            amount = resource.amount
            
            # Check cargo capacity
            current_cargo = sum(self.cargo.values())
            if current_cargo + amount > self.max_cargo:
                amount = self.max_cargo - current_cargo
                if amount <= 0:
                    return False
            
            # Add to cargo
            if resource_type in self.cargo:
                self.cargo[resource_type] += amount
            else:
                self.cargo[resource_type] = amount
                
            return True
        except Exception as e:
            logger.error(f"Error collecting resource: {str(e)}")
            return False
    
    def take_damage(self, amount):
        """Apply damage to ship"""
        try:
            # Apply to shield first if available
            if self.shield > 0:
                if amount <= self.shield:
                    self.shield -= amount
                    return False  # Not destroyed
                else:
                    amount -= self.shield
                    self.shield = 0
            
            # Apply remaining damage to health
            self.health -= amount
            return self.health <= 0  # Return True if destroyed
        except Exception as e:
            logger.error(f"Error applying damage: {str(e)}")
            return False