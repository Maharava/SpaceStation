# src/entities/drones/combat_drone.py
import math
from src.entities.drones.drone_base import DroneBase
from src.utils.logger import logger

class CombatDrone(DroneBase):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # Combat stats
        self.weapon_cooldown = 0
        self.weapon_cooldown_max = 30
        self.weapon_damage = 5
        self.attack_range = 200
        
        # Visual
        self.color = (255, 50, 50)  # Red for combat
        
    def update(self, physics, ship, enemies=None):
        """Update combat drone behavior"""
        try:
            # First perform base drone update
            super().update(physics, ship)
            
            # Handle weapon cooldown
            if self.weapon_cooldown > 0:
                self.weapon_cooldown -= 1
            
            # If enemies are provided, find closest and attack
            if enemies and len(enemies) > 0:
                target = self.find_closest_enemy(enemies)
                if target:
                    return self.attack_enemy(target)
            
            return None  # No projectile created
        except Exception as e:
            logger.error(f"Error updating combat drone: {str(e)}")
            return None
    
    def find_closest_enemy(self, enemies):
        """Find the closest enemy in range"""
        try:
            closest_enemy = None
            min_distance = self.attack_range
            
            for enemy in enemies:
                dx = enemy.x - self.x
                dy = enemy.y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
            
            return closest_enemy
        except Exception as e:
            logger.error(f"Error finding closest enemy: {str(e)}")
            return None
    
    def attack_enemy(self, enemy):
        """Attack the target enemy if cooldown allows"""
        try:
            if self.weapon_cooldown <= 0:
                self.weapon_cooldown = self.weapon_cooldown_max
                
                # Calculate direction to enemy
                dx = enemy.x - self.x
                dy = enemy.y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance > 0:
                    dx /= distance
                    dy /= distance
                
                # Create projectile
                projectile = {
                    'x': self.x + dx * self.radius,
                    'y': self.y + dy * self.radius,
                    'velocity_x': dx * 8,
                    'velocity_y': dy * 8,
                    'damage': self.weapon_damage,
                    'lifetime': 40
                }
                
                return projectile
            
            return None
        except Exception as e:
            logger.error(f"Error attacking enemy: {str(e)}")
            return None