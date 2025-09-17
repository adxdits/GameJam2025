from endgame import EndGame

# Dimensions de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    """
    Point d'entrée principal du jeu
    """
    # Simulation du résultat du jeu (à remplacer par ta logique de jeu)
    game_result = False  # True pour victoire, False pour défaite
    
    # Création et affichage de l'écran de fin
    end_screen = EndGame(SCREEN_WIDTH, SCREEN_HEIGHT, game_result)
    end_screen.show_end_screen()

if __name__ == "__main__":
    main()