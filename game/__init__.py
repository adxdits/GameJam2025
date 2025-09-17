# __init__.py dans le dossier "jeu"

# Importation des classes
from .cast import Cast
from .endgame import EndGame
from .gameview import GameView
from .character import Character
from .main_character import MainCharacter


# Visibilité des "from jeu import *"
__all__ = ["Cast","Character", "MainCharacter", "Endgame", "GameView"]

# Variable de version du package
__version__ = "0.1.0"
