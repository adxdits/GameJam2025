import arcade
from casts import Cast
from views.dialog_manager import DialogManager


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Détection des touches"

combinations = {
    "TYPE": {
        "soin": [arcade.key.UP, arcade.key.DOWN, arcade.key.RIGHT, arcade.key.LEFT],
        "feu": [arcade.key.LEFT, arcade.key.RIGHT],
        "dégâts": [arcade.key.UP, arcade.key.RIGHT]
    },
    "QUALIFIER": {
        "mineur": [arcade.key.SPACE],
        "majeur": [arcade.key.DOWN, arcade.key.UP, arcade.key.UP, arcade.key.UP],
        "critique": [arcade.key.LEFT, arcade.key.LEFT]
    },
    "TARGET": {
        "héros": [arcade.key.UP, arcade.key.LEFT, arcade.key.RIGHT, arcade.key.LEFT],
        "ennemi": [arcade.key.DOWN],
        "tous": [arcade.key.RIGHT, arcade.key.RIGHT]
    }
}

words = ["soin", "majeur", "héros"]


class GameView(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
        self.message = "Appuie sur une touche..."
        self.cast = Cast()
        self.QTE_PHASE = False
        self.LVL = 3
        self.qte_active_timer = 0  # Timer pour la durée du QTE
        self.dialog_manager = DialogManager()
        self.hero_mood = 2  # Exemple : humeur initiale

        # Timer for random dialogues
        self.dialog_timer = 10  # Time between dialogues (10 seconds)
        self.dialog_active = False  # Is a dialogue currently active?
   

    def on_draw(self):
        self.clear()
        arcade.draw_text(self.message, 100, 200, arcade.color.WHITE, 20)
        self.dialog_manager.draw()
        
    def set_combo_data(self, combinations: dict, words: list):
        self.qte_active_timer = 3 * (2+self.LVL-1)  # 3 / 5 / 7 secondes pour faire le QTE
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
                    self.QTE_PHASE = False
                    if self.hero_mood < 3:
                        self.hero_mood += 1
                    self.dialog_manager.get_dialog(self.hero_mood)
                    print("QTE réussi ! Sort lancé !")
                elif val == -1:
                    self.QTE_PHASE = False
                    if self.hero_mood > 0:
                        self.hero_mood -= 1 
                    self.dialog_manager.get_dialog(self.hero_mood)
                    print("QTE échoué !")
                else:
                    print("QTE continue..")
                
    def on_update(self, delta_time):
        if not self.QTE_PHASE:
            self.set_combo_data(combinations, words)
        if self.QTE_PHASE:
            self.qte_active_timer -= delta_time
            if self.qte_active_timer <= 0:
                self.QTE_PHASE = False
                print("Temps écoulé ! QTE échoué !")


        # Update the dialogue manager
        self.dialog_manager.update(delta_time)

if __name__ == "__main__":
    GameView()
    arcade.run()
