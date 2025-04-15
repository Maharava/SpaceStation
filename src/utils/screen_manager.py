# src/utils/screen_manager.py
import pygame

class ScreenManager:
    def __init__(self):
        pygame.init()
        self.screen_stack = []
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Card Battler RPG")
        self.clock = pygame.time.Clock()
        self.fps = 60
        
    def push(self, screen):
        # Add screen to stack
        screen.manager = self
        screen.screen = self.screen
        self.screen_stack.append(screen)
        
    def pop(self):
        # Remove top screen and return to previous
        if len(self.screen_stack) > 1:
            self.screen_stack.pop()
            return True
        return False
        
    def set_home(self):
        # Reset to home screen
        if self.screen_stack:
            home = self.screen_stack[0]
            self.screen_stack = [home]
    
    def get_current(self):
        # Get current active screen
        if self.screen_stack:
            return self.screen_stack[-1]
        return None
    
    def create_tooltip(self, text, position):
        # Create a "Coming Soon" tooltip
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(text, True, (255, 255, 255))
        box_width = text_surface.get_width() + 20
        box_height = text_surface.get_height() + 10
        
        # Create semi-transparent background
        box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        box.fill((50, 50, 50, 180))
        box.blit(text_surface, (10, 5))
        
        return box, (position[0] - box_width//2, position[1] - box_height - 5)
        
    def create_dialogue_box(self, text, width=400, height=100):
        # Create semi-transparent dialogue box for secretary
        box = pygame.Surface((width, height), pygame.SRCALPHA)
        box.fill((100, 100, 100, 160))
        
        # Render text with wrapping
        font = pygame.font.SysFont(None, 24)
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] < width - 20:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
            
        # Draw text on box
        y_offset = 10
        for line in lines:
            text_surface = font.render(line, True, (255, 255, 255))
            box.blit(text_surface, (10, y_offset))
            y_offset += font.get_linesize()
            
        return box
        
    def run(self):
        # Main loop to run current screen
        running = True
        while running and self.screen_stack:
            # Run current screen - let screens handle their own events
            current = self.get_current()
            if current:
                result = current.run()
                if result is False:
                    if not self.pop():
                        running = False
            else:
                running = False
                
            # Update display and maintain framerate
            pygame.display.flip()
            self.clock.tick(self.fps)
            
        pygame.quit()
        return running