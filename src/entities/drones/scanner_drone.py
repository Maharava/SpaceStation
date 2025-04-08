# src/entities/drones/scanner_drone.py
import math
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
        
        # Visual
        self.color = (50, 200, 255)  # Blue for scanner
        
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
                if self.scan_timer <= 0:
                    self.scan_active = False
            
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