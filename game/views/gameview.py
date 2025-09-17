import arcade
import random
from casts import Cast
from entities import Monster

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
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
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=False)
        
        self.background = arcade.load_texture("../assets/Backgrounds/Lvl1.png")
        
        self.QTE_PHASE = False
        self.TIME_BEFORE_SPAWN = 2.0
        self.DELAY_HERO_ATTACKS = 1.0
        
        
        self.cast = Cast()
        self.LVL = 3
        
        # --QTE:
        self.qte_active_timer = 0  # Timer pour la durée du QTE
        
        # --Entitées:
        # Monstres/Ennemies
        self.enemies_timer_before_spawn = None
        self.enemies_buffer = []
        self.enemies_timer_on_screen = 0
        self.enemies_on_screen = False
        self.moving_distance = 400 # Distance que doit parcourir un ennemi/monstre
        
        self.time_between_hero_attacks = None

    def on_draw(self):
        self.clear()
        # On dessine l’image sur toute la fenêtre
        arcade.draw_lrwh_rectangle_textured(
            0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background
        )
        
        for m in self.enemies_buffer:
            m.on_draw()
        
    def set_combo_data(self, combinations: dict, words: list):
        self.qte_active_timer = 3 * (2+self.LVL-1)  # 3 / 5 / 7 secondes pour faire le QTE
        self.cast.set_data_combo(combinations, words, self.LVL)
        self.QTE_PHASE = True  # On entre en phase de QTE
        print("Phase de QTE commencée !" + str(self.QTE_PHASE))
        
    def set_timer_spawn_enemies(self):
        self.enemies_timer_before_spawn = 5
    
    def spawn_enemies(self):
        # FAIRE UN SYSTEM ALEATOIRE POUR LES SPRITES DES ENEMIES
        nb_enemies = random.randint(1, 3)
        for i in range(nb_enemies):
            self.enemies_buffer.append(Monster(3, -50 * (i+1), 170, 60))

    def on_key_press(self, key, modifiers):
        # Si on est en phase de QTE
        if self.QTE_PHASE:
            # On traite le cas où une flèche directionnelle est pressée
            if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.RIGHT, arcade.key.LEFT):
                val = self.cast.check_qte(key)
                # Si QTE terminé avec succès
                if val == 1:
                    self.QTE_PHASE = False
                    print("QTE réussi ! Sort lancé !")
                elif val == -1:
                    self.QTE_PHASE = False
                    print("QTE échoué !")
                else:
                    print("QTE continue..")
                
    def on_update(self, delta_time):
        # --QTE:
        # if not self.QTE_PHASE:
        #     self.set_combo_data(combinations, words)
        if self.QTE_PHASE:
            self.qte_active_timer -= delta_time
            if self.qte_active_timer <= 0:
                self.QTE_PHASE = False
                print("Temps écoulé ! QTE échoué !")        

        # --Entités:
        # Fin de vague d'ennemis → relance un timer
        if len(self.enemies_buffer) == 0 and self.enemies_timer_before_spawn is None:
            self.enemies_on_screen = False
            self.enemies_timer_before_spawn = self.TIME_BEFORE_SPAWN  # relance une nouvelle vague

        # Décrémentation du timer avant spawn
        if not self.enemies_on_screen and self.enemies_timer_before_spawn is not None:
            self.enemies_timer_before_spawn -= delta_time

            # Quand le timer atteint zéro ou moins --> spawn ennemis
            if self.enemies_timer_before_spawn <= 0:
                self.spawn_enemies()
                self.enemies_timer_before_spawn = None  # désactive le timer

        # Déplacement des ennemis dans la carte
        if not self.enemies_on_screen and len(self.enemies_buffer) > 0:
            for m in list(self.enemies_buffer):
                m.update_coordinates(m.get_speed() * delta_time, 0)
                if m.get_distance_moved() >= self.moving_distance:
                    self.enemies_on_screen = True
                    self.time_between_hero_attacks = self.DELAY_HERO_ATTACKS
                    
        # Cooldown attaque héros
        if self.enemies_on_screen and len(self.enemies_buffer) > 0 and self.time_between_hero_attacks > 0:
            self.time_between_hero_attacks -= delta_time
        # Attaque héros sur ennemis
        elif self.enemies_on_screen and len(self.enemies_buffer) > 0 and self.time_between_hero_attacks <= 0:
            self.enemies_buffer[0].take_damage(1, self.enemies_buffer)
            self.time_between_hero_attacks = self.DELAY_HERO_ATTACKS  # reset le timer
            
        
if __name__ == "__main__":
    GameView()
    arcade.run()
