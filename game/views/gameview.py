import arcade
from casts import Cast
from endgame import EndGame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Détection des touches"

combinations = {
    "TYPE": {
        "soin": [arcade.key.UP, arcade.key.DOWN],
        "feu": [arcade.key.LEFT, arcade.key.RIGHT],
        "dégâts": [arcade.key.UP, arcade.key.RIGHT]
    },
    "QUALIFIER": {
        "mineur": [arcade.key.SPACE],
        "majeur": [arcade.key.DOWN, arcade.key.UP],
        "critique": [arcade.key.LEFT, arcade.key.LEFT]
    },
    "TARGET": {
        "héros": [arcade.key.UP],
        "ennemi": [arcade.key.DOWN],
        "tous": [arcade.key.RIGHT, arcade.key.RIGHT]
    }
}

words = ["soin", "majeur", "héros"]

game_results = True  # True pour victoire, False pour défaite

class GameView(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
        self.message = "Appuie sur une touche..."
        self.cast = Cast()
        self.QTE_PHASE = False
        self.LVL = 3
        self.end_screen = None
        self.game_ended = False

    def on_draw(self):
        self.clear()
        if not self.game_ended:
            arcade.draw_text(self.message, 100, 200, arcade.color.WHITE, 20)
        if self.end_screen:
            self.end_screen.draw()
        
    def set_combo_data(self, combinations: dict, words: list):
        self.cast.set_data_combo(combinations, words, self.LVL)
        self.QTE_PHASE = True  # On entre en phase de QTE
        print("Phase de QTE commencée !" + str(self.QTE_PHASE))

    def on_key_press(self, key, modifiers):
        # Si on est en phase de QTE
        if self.QTE_PHASE:
            # On traite le cas où une flèche directionnelle est pressée
            if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.RIGHT, arcade.key.LEFT):
                val = self.cast.check_qte(key)
                # Si QTE terminé avec succès
                if val == 1:
                    print("QTE réussi ! Sort lancé !")
                elif val == -1:
                    self.QTE_PHASE = False
                    print("QTE échoué !")
                    self.show_end_screen()  # Défaite
                else:
                    print("QTE continue..")
                
    def on_update(self, delta_time):
        if not self.QTE_PHASE:
            self.set_combo_data(combinations, words)
        if self.game_ended and self.end_screen:
            self.end_screen.update(delta_time)
        # return super().on_update(delta_time)
                
    def show_end_screen(self):
        self.game_ended = True
        self.end_screen = EndGame(self, game_results)

    # def on_key_release(self, key, modifiers):
    #     self.message = f"Touche {key} relâchée"

if __name__ == "__main__":
    GameView()
    arcade.run()
