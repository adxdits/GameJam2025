import arcade
from casts import Cast

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
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


class GameView(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.message = "Appuie sur une touche..."
        self.cast = Cast()
        self.QTE_PHASE = False
        self.LVL = 3

    def on_draw(self):
        self.clear()
        arcade.draw_text(self.message, 100, 200, arcade.color.WHITE, 20)
        
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
                else:
                    print("QTE continue..")
                
    def on_update(self, delta_time):
        if not self.QTE_PHASE:
            self.set_combo_data(combinations, words)
        # return super().on_update(delta_time)
                

    # def on_key_release(self, key, modifiers):
    #     self.message = f"Touche {key} relâchée"

if __name__ == "__main__":
    GameView()
    arcade.run()
