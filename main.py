import sys
import os
sys.path.append(os.path.abspath("src"))

from src.core.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()