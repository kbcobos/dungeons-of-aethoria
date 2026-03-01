import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from game import start_game

if __name__ == "__main__":
    try:
        start_game()
    except KeyboardInterrupt:
        print("\n\n  [Juego interrumpido. Hasta pronto, aventurero.]\n")
        sys.exit(0)
