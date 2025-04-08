import pygame

class InputHandler:
    def __init__(self, config):
        self.config = config
        self.actions = {}
        self.keys_pressed = {}
        self.setup_controls()
    
    def setup_controls(self):
        controls = self.config.get("controls")
        self.key_mapping = {
            controls["move_up"]: "move_up",
            controls["move_down"]: "move_down",
            controls["move_left"]: "move_left",
            controls["move_right"]: "move_right",
            controls["fire"]: "fire"
        }
    
    def handle_events(self):
        self.actions = {action: False for action in set(self.key_mapping.values())}
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                self.keys_pressed[key] = True
                
            if event.type == pygame.KEYUP:
                key = pygame.key.name(event.key)
                self.keys_pressed[key] = False
        
        # Process pressed keys into actions
        for key, is_pressed in self.keys_pressed.items():
            if key in self.key_mapping and is_pressed:
                self.actions[self.key_mapping[key]] = True
        
        return True
    
    def is_action_pressed(self, action):
        return self.actions.get(action, False)