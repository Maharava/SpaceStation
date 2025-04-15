# src/main.py
import pygame
import sys
from utils.screen_manager import ScreenManager
from screens.home_screen import HomeScreen

def main():
    pygame.init()
    pygame.display.set_caption("Card Battler RPG")
    
    # Create screen manager
    screen_manager = ScreenManager()
    
    # Start with home screen
    home_screen = HomeScreen(screen_manager)
    screen_manager.push(home_screen)
    
    # Run the game
    screen_manager.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()