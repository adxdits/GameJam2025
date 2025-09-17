import arcade

class EndGame(arcade.Window):
    def __init__(self, width: int, height: int, victory: bool = True):
        """
        Initialise l'écran de fin de jeu
        :param width: Largeur de la fenêtre
        :param height: Hauteur de la fenêtre
        :param victory: True pour une victoire, False pour une défaite
        """
        super().__init__(width, height, "Fin du Jeu")
        self.victory = victory
        
        # Chargement de l'image en fonction du résultat
        image_path = "assets/Arrow(Projectile)/Arrow01(32x32).png" if victory else "assets/Arrow(Projectile)/Arrow02(32x32).png"
        self.image = arcade.Sprite(image_path, scale=2.0)
        
        # Initialiser la position de l'image au centre
        self.image.center_x = width // 2
        self.image.center_y = height // 2

    def on_draw(self):
        arcade.start_render()
        self.image.draw()

    def on_update(self, delta_time):
        # Cette méthode est appelée à chaque frame pour mettre à jour la logique du jeu
        pass

    def show_end_screen(self):
        """
        Affiche l'écran de fin et lance la boucle de jeu
        """
        arcade.run()