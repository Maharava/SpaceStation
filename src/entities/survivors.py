# src/entities/survivors.py
from src.utils.logger import logger

class Survivor:
    def __init__(self, name, specialty, portrait_id=1):
        self.name = name
        self.specialty = specialty
        self.portrait_id = portrait_id
        self.rescued = False
        self.assigned_module = None
        self.relationship = 0  # 0-100 scale
        
        # Specialty bonuses
        self.bonuses = {
            'engineer': {'ship_repair_efficiency': 0.2},
            'pilot': {'ship_speed': 0.15},
            'scientist': {'research_speed': 0.25},
            'medic': {'healing_efficiency': 0.2},
            'security': {'combat_efficiency': 0.15}
        }
    
    def get_dialog(self, context):
        """Return appropriate dialog based on context"""
        try:
            # Very simple dialog system for MVP
            dialogs = {
                'greeting': f"Hello, I'm {self.name}. I specialize in {self.specialty}.",
                'rescued': "Thank you for rescuing me. I'll help however I can.",
                'station': f"I can boost {self.specialty} operations if you assign me to the right module."
            }
            
            return dialogs.get(context, dialogs['greeting'])
        except Exception as e:
            logger.error(f"Error getting survivor dialog: {str(e)}")
            return f"Hello, I'm {self.name}."
    
    def get_bonuses(self):
        """Return bonuses based on specialty"""
        return self.bonuses.get(self.specialty, {})

class SurvivorGenerator:
    def __init__(self):
        # Sample data for survivors
        self.names = ["Alex", "Morgan", "Taylor", "Jordan", "Casey"]
        self.specialties = ["engineer", "pilot", "scientist", "medic", "security"]
        
    def generate_survivor(self):
        """Generate a random survivor for missions"""
        try:
            import random
            name = random.choice(self.names)
            specialty = random.choice(self.specialties)
            portrait_id = random.randint(1, 5)
            
            return Survivor(name, specialty, portrait_id)
        except Exception as e:
            logger.error(f"Error generating survivor: {str(e)}")
            return Survivor("Unknown", "engineer", 1)