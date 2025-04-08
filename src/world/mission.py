# src/world/mission.py
import random
from src.utils.logger import logger
from src.entities.resources import ResourceGenerator
from src.entities.survivors import SurvivorGenerator

class Mission:
    def __init__(self, map_data):
        self.map_data = map_data
        self.objectives = []
        self.resources = []
        self.enemies = []
        self.survivor = None
        self.completed = False
        self.resource_generator = ResourceGenerator()
        self.survivor_generator = SurvivorGenerator()
        
    def generate_mission(self, mission_type="exploration", difficulty=1):
        """Generate mission content based on type and difficulty"""
        try:
            # Generate mission resources
            resource_count = 10 + difficulty * 5
            self.resources = self.resource_generator.generate_resources(
                self.map_data['width'], 
                self.map_data['height'], 
                resource_count
            )
            
            # Set mission objectives based on type
            if mission_type == "exploration":
                self.generate_exploration_mission()
            elif mission_type == "rescue":
                self.generate_rescue_mission()
            elif mission_type == "collection":
                self.generate_collection_mission()
            else:
                # Default to exploration
                self.generate_exploration_mission()
                
            return {
                'type': mission_type,
                'difficulty': difficulty,
                'objectives': self.objectives
            }
        except Exception as e:
            logger.error(f"Error generating mission: {str(e)}")
            # Default mission if error occurs
            self.objectives = [{'type': 'explore', 'target': 'sector', 'completed': False}]
            return {'type': 'exploration', 'difficulty': difficulty, 'objectives': self.objectives}
    
    def generate_exploration_mission(self):
        """Generate objectives for exploration mission"""
        try:
            # Simple exploration mission
            self.objectives = [
                {'type': 'explore', 'target': 'sector', 'completed': False, 
                 'description': 'Scan the sector for valuable data'}
            ]
            
            # Add a point of interest to visit if available
            if self.map_data['points_of_interest']:
                poi = random.choice(self.map_data['points_of_interest'])
                self.objectives.append({
                    'type': 'visit', 
                    'target': poi, 
                    'completed': False,
                    'description': f'Visit the {poi["type"]} at coordinates ({poi["x"]}, {poi["y"]})'
                })
        except Exception as e:
            logger.error(f"Error generating exploration mission: {str(e)}")
            self.objectives = [{'type': 'explore', 'target': 'sector', 'completed': False}]
    
    def generate_rescue_mission(self):
        """Generate objectives for rescue mission"""
        try:
            # Generate a survivor
            self.survivor = self.survivor_generator.generate_survivor()
            
            # Create a rescue point if there are points of interest
            rescue_point = None
            if self.map_data['points_of_interest']:
                rescue_point = random.choice(self.map_data['points_of_interest'])
            else:
                # Create a random rescue location
                x = random.randint(100, self.map_data['width'] - 100)
                y = random.randint(100, self.map_data['height'] - 100)
                rescue_point = {'x': x, 'y': y, 'radius': 50, 'type': 'escape_pod'}
            
            self.objectives = [
                {'type': 'rescue', 
                 'target': rescue_point, 
                 'completed': False, 
                 'survivor': self.survivor,
                 'description': f'Rescue {self.survivor.name} from the {rescue_point["type"]}'}
            ]
        except Exception as e:
            logger.error(f"Error generating rescue mission: {str(e)}")
            self.objectives = [{'type': 'explore', 'target': 'sector', 'completed': False}]
    
    def generate_collection_mission(self):
        """Generate objectives for resource collection mission"""
        try:
            # Target specific resource type
            resource_types = ['metal', 'crystal', 'energy', 'tech']
            target_type = random.choice(resource_types)
            target_amount = random.randint(10, 30)
            
            self.objectives = [
                {'type': 'collect', 
                 'resource_type': target_type, 
                 'amount': target_amount, 
                 'collected': 0, 
                 'completed': False,
                 'description': f'Collect {target_amount} units of {target_type}'}
            ]
        except Exception as e:
            logger.error(f"Error generating collection mission: {str(e)}")
            self.objectives = [{'type': 'explore', 'target': 'sector', 'completed': False}]
    
    def check_objective_completion(self, ship, visit_radius=100):
        """Check if objectives are completed"""
        try:
            for objective in self.objectives:
                if objective['completed']:
                    continue
                    
                # Handle different objective types
                if objective['type'] == 'explore':
                    # For simplicity, exploration is completed after collecting some resources
                    collected_count = sum(1 for resource in self.resources if resource not in self.resources)
                    if collected_count >= len(self.resources) * 0.5:  # 50% of resources collected
                        objective['completed'] = True
                
                elif objective['type'] == 'visit':
                    target = objective['target']
                    dx = ship.x - target['x']
                    dy = ship.y - target['y']
                    distance = (dx**2 + dy**2)**0.5
                    
                    if distance < visit_radius:
                        objective['completed'] = True
                
                elif objective['type'] == 'rescue':
                    target = objective['target']
                    dx = ship.x - target['x']
                    dy = ship.y - target['y']
                    distance = (dx**2 + dy**2)**0.5
                    
                    if distance < visit_radius:
                        objective['completed'] = True
                        objective['survivor'].rescued = True
                
                elif objective['type'] == 'collect':
                    # Check cargo for required resources
                    if objective['resource_type'] in ship.cargo:
                        objective['collected'] = ship.cargo[objective['resource_type']]
                        if objective['collected'] >= objective['amount']:
                            objective['completed'] = True
            
            # Check if all objectives are completed
            all_completed = all(obj['completed'] for obj in self.objectives)
            self.completed = all_completed
            
            return self.completed
        except Exception as e:
            logger.error(f"Error checking objective completion: {str(e)}")
            return False