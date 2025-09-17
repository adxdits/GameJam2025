# __init__.py dans le dossier "jeu"

# Importation des classes
from .cast import Cast
from .gameview import GameView

# Visibilité des "from jeu import *"
__all__ = ["Cast", "GameView"]

# Variable de version du package
__version__ = "0.1.0"
