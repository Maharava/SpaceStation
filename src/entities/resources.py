# src/entities/resources.py
import random
from src.utils.logger import logger

class Resource:
    def __init__(self, x, y, resource_type, amount):
        self.x = x
        self.y = y
        self.resource_type = resource_type
        self.amount = amount
        self.radius = 10 + amount // 10  # Size based on amount
        self.detected = False  # Whether a scanner has detected this
        
        # Visual properties based on resource type
        self.colors = {
            'metal': (150, 150, 180),
            'crystal': (200, 100, 220),
            'energy': (100, 220, 100),
            'tech': (220, 180, 100)
        }
        
        if resource_type in self.colors:
            self.color = self.colors[resource_type]
        else:
            self.color = (200, 200, 200)  # Default

class ResourceGenerator:
    def __init__(self):
        # Resource type probabilities
        self.resource_types = {
            'metal': 0.4,
            'crystal': 0.3,
            'energy': 0.2,
            'tech': 0.1
        }
        
    def generate_resources(self, map_width, map_height, count):
        """Generate a list of random resources within map bounds"""
        try:
            resources = []
            
            for _ in range(count):
                # Random position with some padding from edges
                padding = 50
                x = random.randint(padding, map_width - padding)
                y = random.randint(padding, map_height - padding)
                
                # Random type based on probabilities
                resource_type = self.get_random_type()
                
                # Random amount
                amount = random.randint(5, 30)
                
                resources.append(Resource(x, y, resource_type, amount))
            
            return resources
        except Exception as e:
            logger.error(f"Error generating resources: {str(e)}")
            return []
    
    def get_random_type(self):
        """Select a random resource type based on probabilities"""
        try:
            rand = random.random()
            cumulative = 0
            
            for resource_type, probability in self.resource_types.items():
                cumulative += probability
                if rand <= cumulative:
                    return resource_type
                    
            return 'metal'  # Default if something goes wrong
        except Exception as e:
            logger.error(f"Error selecting resource type: {str(e)}")
            return 'metal'