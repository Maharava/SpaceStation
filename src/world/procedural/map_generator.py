# src/world/procedural/map_generator.py
import random
import math
from src.utils.logger import logger

class MapGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map_data = {}
        
    def generate_map(self, difficulty=1):
        """Generate a procedural map with obstacles and points of interest"""
        try:
            self.map_data = {
                'width': self.width,
                'height': self.height,
                'obstacles': self.generate_obstacles(difficulty),
                'points_of_interest': self.generate_points_of_interest(difficulty),
                'background_objects': self.generate_background_objects(difficulty)
            }
            
            return self.map_data
        except Exception as e:
            logger.error(f"Error generating map: {str(e)}")
            return self.create_default_map()
    
    def generate_obstacles(self, difficulty):
        """Generate obstacles (asteroids, debris) based on difficulty"""
        try:
            obstacles = []
            count = 20 + difficulty * 10  # More obstacles at higher difficulty
            
            for _ in range(count):
                x = random.randint(50, self.width - 50)
                y = random.randint(50, self.height - 50)
                size = random.randint(15, 40)
                
                # Different types of obstacles
                obstacle_type = random.choice(['asteroid', 'debris', 'ice'])
                
                obstacles.append({
                    'x': x,
                    'y': y,
                    'radius': size,
                    'type': obstacle_type,
                    'rotation': random.random() * 360,
                    'rotation_speed': (random.random() - 0.5) * 2
                })
            
            return obstacles
        except Exception as e:
            logger.error(f"Error generating obstacles: {str(e)}")
            return []
    
    def generate_points_of_interest(self, difficulty):
        """Generate mission-relevant points"""
        try:
            points = []
            count = 2 + difficulty  # More POIs at higher difficulty
            
            # Ensure points are spaced out
            for _ in range(count):
                valid_position = False
                attempts = 0
                
                while not valid_position and attempts < 20:
                    x = random.randint(100, self.width - 100)
                    y = random.randint(100, self.height - 100)
                    
                    # Check distance from other points
                    min_distance = float('inf')
                    for point in points:
                        dist = math.sqrt((x - point['x'])**2 + (y - point['y'])**2)
                        min_distance = min(min_distance, dist)
                    
                    if min_distance > 200 or len(points) == 0:
                        valid_position = True
                    
                    attempts += 1
                
                if valid_position:
                    point_type = random.choice(['derelict', 'station', 'anomaly'])
                    points.append({
                        'x': x,
                        'y': y,
                        'radius': 50,
                        'type': point_type
                    })
            
            return points
        except Exception as e:
            logger.error(f"Error generating points of interest: {str(e)}")
            return []
    
    def generate_background_objects(self, difficulty):
        """Generate non-collidable background elements"""
        try:
            objects = []
            count = 30 + difficulty * 5
            
            for _ in range(count):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                size = random.randint(2, 8)
                
                object_type = random.choice(['star', 'dust', 'nebula'])
                brightness = random.random() * 0.5 + 0.5  # 0.5 to 1.0
                
                objects.append({
                    'x': x,
                    'y': y,
                    'size': size,
                    'type': object_type,
                    'brightness': brightness
                })
            
            return objects
        except Exception as e:
            logger.error(f"Error generating background objects: {str(e)}")
            return []
    
    def create_default_map(self):
        """Create a simple default map in case of errors"""
        return {
            'width': self.width,
            'height': self.height,
            'obstacles': [],
            'points_of_interest': [],
            'background_objects': []
        }