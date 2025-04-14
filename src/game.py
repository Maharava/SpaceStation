# jovian_cards/src/game.py

# Main game logic for Jovian Cards

import pygame
from ui.character_screen import CharacterScreen

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Jovian Cards")
        self.heroes = []
        self.current_room = 0

    def start(self):
        self.load_heroes()
        self.game_loop()

    def load_heroes(self):
        # Load heroes from data
        pass

    def game_loop(self):
        while True:
            self.handle_input()
            self.update_game_state()
            self.render()

    def handle_input(self):
        # Handle user input
        pass

    def update_game_state(self):
        # Update game state based on actions
        pass

    def render(self):
        # Render the game state to the screen
        pass

    def run(self):
        try:
            character_screen = CharacterScreen(self.screen)
            character_screen.run()
        finally:
            pygame.quit()  # Only quit pygame at the end of the main game loop

if __name__ == "__main__":
    game = Game()
    game.start()