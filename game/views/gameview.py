import arcade
import random
from larbin import Character
from casts import Cast
from entities import Monster
from views.dialog_manager import DialogManager
from endgame import EndGame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Détection des touches"
parchment_texture = arcade.load_texture("../assets/sprites/parchemin.png")
CUSTOM_FONT = "../assets/fonts/DigitalDisco.ttf"
arcade.load_font(CUSTOM_FONT)

# =========================
# Données
# =========================

TYPES = {
    "Massage":       [arcade.key.LEFT,  arcade.key.RIGHT, arcade.key.LEFT,  arcade.key.RIGHT],   # va-et-vient
    "Lissage":       [arcade.key.RIGHT, arcade.key.RIGHT, arcade.key.RIGHT, arcade.key.RIGHT],   # gestes rectilignes
    "Polissage":     [arcade.key.UP,    arcade.key.RIGHT, arcade.key.DOWN,  arcade.key.LEFT],    # mouvement circulaire
    "Hydratation":   [arcade.key.UP,    arcade.key.UP,    arcade.key.DOWN,  arcade.key.DOWN],    # vagues
    "Réchauffage":   [arcade.key.UP,    arcade.key.RIGHT, arcade.key.UP,    arcade.key.RIGHT],   # friction qui monte
    "Rafraîchissement":[arcade.key.DOWN,arcade.key.LEFT,  arcade.key.DOWN,  arcade.key.LEFT],    # souffle frais
    "Peignage":      [arcade.key.UP,    arcade.key.DOWN,  arcade.key.UP,    arcade.key.DOWN],    # peigne haut-bas
    "Brillance":     [arcade.key.UP,    arcade.key.LEFT,  arcade.key.UP,    arcade.key.LEFT],    # éclats en zig
    "Démêlage":      [arcade.key.DOWN,  arcade.key.UP,    arcade.key.DOWN,  arcade.key.UP],      # contre-peigne
}

QUALIFICATIFS = {
    "exquis":        [arcade.key.RIGHT, arcade.key.UP,    arcade.key.RIGHT, arcade.key.UP],
    "délicat":       [arcade.key.LEFT,  arcade.key.UP,    arcade.key.LEFT,  arcade.key.UP],
    "parfumé":       [arcade.key.RIGHT, arcade.key.DOWN,  arcade.key.RIGHT, arcade.key.DOWN],
    "divin":         [arcade.key.UP,    arcade.key.RIGHT, arcade.key.RIGHT, arcade.key.UP],
    "soyeux":        [arcade.key.DOWN,  arcade.key.RIGHT, arcade.key.RIGHT, arcade.key.DOWN],
    "scintillant":   [arcade.key.UP,    arcade.key.LEFT,  arcade.key.LEFT,  arcade.key.UP],
    "inutile":       [arcade.key.LEFT,  arcade.key.DOWN,  arcade.key.LEFT,  arcade.key.DOWN],
    "urgent":        [arcade.key.UP,    arcade.key.UP,    arcade.key.RIGHT, arcade.key.RIGHT],
    "cosmétique":    [arcade.key.RIGHT, arcade.key.RIGHT, arcade.key.UP,    arcade.key.UP],
}

CIBLES = {
    "des cheveux":     [arcade.key.UP,    arcade.key.LEFT,  arcade.key.DOWN,  arcade.key.RIGHT],
    "de la moustache": [arcade.key.LEFT,  arcade.key.DOWN,  arcade.key.RIGHT, arcade.key.UP],
    "des bottes":      [arcade.key.DOWN,  arcade.key.DOWN,  arcade.key.RIGHT, arcade.key.LEFT],
    "du plastron":     [arcade.key.RIGHT, arcade.key.LEFT,  arcade.key.UP,    arcade.key.DOWN],
    "des gants":       [arcade.key.LEFT,  arcade.key.RIGHT, arcade.key.DOWN,  arcade.key.UP],
    "de l’armure":     [arcade.key.RIGHT, arcade.key.UP,    arcade.key.LEFT,  arcade.key.DOWN],
    "des sourcils":    [arcade.key.UP,    arcade.key.DOWN,  arcade.key.LEFT,  arcade.key.RIGHT],
    "du casque":       [arcade.key.UP,    arcade.key.UP,    arcade.key.LEFT,  arcade.key.RIGHT],
    "des ongles":      [arcade.key.DOWN,  arcade.key.LEFT,  arcade.key.UP,    arcade.key.RIGHT],
}

LISTES = {
    "TYPES" : TYPES,
    "QUALIFICATIFS" : QUALIFICATIFS,
    "CIBLES" : CIBLES,
}

ARROW = {
    arcade.key.UP: "↑",
    arcade.key.DOWN: "↓",
    arcade.key.LEFT: "←",
    arcade.key.RIGHT: "→",
}

# =========================

class GameView(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen = True)
        
        # --Entitées:
        # Monstres/Ennemies
        self.enemies_timer_before_spawn = None
        self.enemies_buffer = []
        self.enemies_timer_on_screen = 0
        self.enemies_on_screen = False
        self.moving_distance = 400 # Distance que doit parcourir un ennemi/monstre
        
        self.time_between_hero_attacks = None

        self.UI_W, self.UI_H = 1920, 1080  # résolution virtuelle de référence
        self.ui_scale = 1.0
        self.ui_offx = 0
        self.ui_offy = 0

        self.character = Character(self)

        self.bg_tex = arcade.load_texture("../assets/Backgrounds/Lvl1.png")
        self.bg_w, self.bg_h = self.bg_tex.width, self.bg_tex.height

        self.current_words = []
        self.seen = {"TYPES": [], "QUALIFICATIFS": [], "CIBLES": []}
        self.cast = Cast()
        self.QTE_PHASE = False
        self.TIME_BEFORE_SPAWN = 2.0
        self.DELAY_HERO_ATTACKS = 1.0
        
        
        self.cast = Cast()
        self.LVL = 3
        self.end_screen = None
        self.game_ended = False

        self.dialog_manager = DialogManager()
        self.hero_mood = 2  # Exemple : humeur initiale

        # Timer for random dialogues
        self.dialog_timer = 10  # Time between dialogues (10 seconds)
        self.dialog_active = False  # Is a dialogue currently active?
        
        # --QTE:
        self.qte_active_timer = 0  # Timer pour la durée du QTE
        self.feedback_text = ""       # "YEAH !" ou "Ohh.."
        self.feedback_timer = 0.0

    def _begin_ui(self):
        # scale uniforme (fit) pour conserver le ratio
        s = min(self.width / self.UI_W, self.height / self.UI_H)
        self.ui_scale = s
        self.ui_offx = (self.width  - self.UI_W * s) / 2
        self.ui_offy = (self.height - self.UI_H * s) / 2

    def _sx(self, x): return int(self.ui_offx + x * self.ui_scale)
    def _sy(self, y): return int(self.ui_offy + y * self.ui_scale)
    def _sw(self, w): return int(w * self.ui_scale)
    def _sh(self, h): return int(h * self.ui_scale)
    def _sf(self, size): return max(1, int(size * self.ui_scale))  # font size

    def _find_sequence_for_word(self, word: str):
        """Retourne la séquence (liste de 4 keycodes) pour un mot."""
        if word in TYPES: return TYPES[word]
        if word in QUALIFICATIFS: return QUALIFICATIFS[word]
        if word in CIBLES: return CIBLES[word]
        return None

    def _format_sequence(self, seq):
        """Transforme [UP, RIGHT, DOWN, LEFT] en '↑ → ↓ ←'."""
        if not seq:
            return "?"
        return " ".join(ARROW.get(k, "?") for k in seq)
    
    def _bucketize_words(self):
        """Retourne les mots de self.current_words répartis par catégorie en respectant l'ordre."""
        buckets = {"TYPES": [], "QUALIFICATIFS": [], "CIBLES": []}
        for w in self.current_words:
            if w in TYPES:
                buckets["TYPES"].append(w)
            elif w in QUALIFICATIFS:
                buckets["QUALIFICATIFS"].append(w)
            elif w in CIBLES:
                buckets["CIBLES"].append(w)
        return buckets

    def _draw_section(self, title, words, x_left, y_top, width, height):
        y_cursor = y_top
        title_h = 40

        font_size_word   = self._sf(23)
        font_size_arrows = self._sf(23)
        line_h = font_size_word + self._sh(12)

        # Titre
        arcade.draw_text(
            title,
            self._sx(x_left + width // 2),
            self._sy(y_cursor - title_h // 2),
            arcade.color.DARK_BROWN,
            self._sf(18),
            anchor_x="center",
            anchor_y="center",
            width=self._sw(width),
            align="center",
            font_name="DigitalDisco"
        )
        y_cursor -= (title_h + 6)

        col_word_w = int(width * 0.60)
        col_arrow_x = x_left + col_word_w + 8

        for w in words:
            seq = self._find_sequence_for_word(w)
            arrows = self._format_sequence(seq)

            y_cursor -= line_h
            if y_cursor < (y_top - height):
                break

            # Mot (font custom)
            arcade.draw_text(
                w,
                self._sx(x_left), self._sy(y_cursor),
                arcade.color.BLACK,
                font_size_word,
                width=self._sw(col_word_w),
                align="left",
                anchor_x="left",
                anchor_y="baseline",
                font_name="DigitalDisco",
            )

            # Flèches (font par défaut)
            arcade.draw_text(
                arrows,
                self._sx(col_arrow_x), self._sy(y_cursor),
                arcade.color.BLACK,
                font_size_arrows,
                width=self._sw(width - col_word_w - 8),
                align="left",
                anchor_x="left",
                anchor_y="baseline",
            )



    def _add_seen_words(self, words: list):
        for w in words:
            if w in TYPES and w not in self.seen["TYPES"]:
                self.seen["TYPES"].append(w)
            elif w in QUALIFICATIFS and w not in self.seen["QUALIFICATIFS"]:
                self.seen["QUALIFICATIFS"].append(w)
            elif w in CIBLES and w not in self.seen["CIBLES"]:
                self.seen["CIBLES"].append(w)

    def on_draw(self):
        self.clear()
        self._begin_ui()

        virt_cover = max(self.UI_W / self.bg_w, self.UI_H / self.bg_h)
        final_scale = virt_cover * self.ui_scale  # important: * ui_scale

        arcade.draw_scaled_texture_rectangle(
            self._sx(self.UI_W // 2),
            self._sy(self.UI_H // 2),
            self.bg_tex,
            final_scale,
        )

        parchment_width = max(1, int(self.UI_W * 0.45))  # 1/3 de la largeur de l’écran
        parchment_height = max(1, int(self.UI_H + 400))

        x = self.UI_W - parchment_width // 3 + 50  # centré à droite
        y = self.UI_H // 2                   # centré verticalement

        arcade.draw_texture_rectangle(
            self._sx(x), 
            self._sy(y),
            self._sw(parchment_width), 
            self._sh(parchment_height),
            parchment_texture
        )

        # Zone texte "safe" dans le parchemin
        margin_left = int(parchment_width * 0.26)
        margin_right = int(parchment_width * 0.25)
        margin_top = int(parchment_height * 0.19)
        margin_bottom = int(parchment_height * 0.17)

        box_left = x - parchment_width // 2 + margin_left
        box_right = x + parchment_width // 2 - margin_right
        box_bottom = y - parchment_height // 2 + margin_bottom
        box_top = y + parchment_height // 2 - margin_top
        box_width = max(1, int(box_right - box_left))

        # Si QTE actif : afficher la phrase + les enchaînements
        if self.QTE_PHASE and self.current_words:
            # 1) Phrase centrée sur la partie gauche (hors parchemin)
            phrase_width = max(1, int(self.UI_W - parchment_width - 80))
            left_area_center_x = (self.UI_W - parchment_width) // 2
            phrase = " ".join(self.current_words)
            arcade.draw_text(
                phrase,
                self._sx(left_area_center_x),
                self._sy(self.UI_H // 2),
                arcade.color.WHITE,
                self._sf(36),
                anchor_x="center",
                anchor_y="center",
                align="center",
                width=self._sw(phrase_width),
            )
            # Afficher la phrase QTE dans la bulle si aucun dialogue héros n'est actif
            if self.dialog_manager.timer <= 0:
                phrase = " ".join(self.current_words)
                self.dialog_manager.draw_bubble(phrase, is_qte=True)

            # 2) Sur le parchemin : "mot : enchainement"
            buckets = self.seen

            total_h = int(box_top - box_bottom)
            h_types = int(total_h * 0.32)
            h_quals = int(total_h * 0.32)
            h_cibles = total_h - h_types - h_quals  # pour absorber l'arrondi

            # Rectangles (de haut en bas)
            types_top = box_top
            quals_top = types_top - h_types
            cibles_top = quals_top - h_quals

            # Dessin des trois sections
            self._draw_section("Types", buckets["TYPES"], box_left, types_top, box_width, h_types)
            self._draw_section("Qualificatifs", buckets["QUALIFICATIFS"], box_left, quals_top, box_width, h_quals)
            self._draw_section("Cibles", buckets["CIBLES"], box_left, cibles_top, box_width, h_cibles)

        if self.feedback_timer > 0 and self.feedback_text:
            arcade.draw_text(
                self.feedback_text,
                self.UI_W // 2,
                int(self.UI_H * 0.75),
                arcade.color.GO_GREEN if self.feedback_text.startswith("Réussi") else arcade.color.RED_ORANGE,
                64,
                anchor_x="center",
                anchor_y="center",
                bold=True,
                align="center",
                width=int(self.UI_W * 0.8),
            )
            
        for m in self.enemies_buffer:
            m.on_draw()
    
        # Dessiner le personnage
        self.character.draw()
        # Dessiner le dialogue
        self.dialog_manager.draw()
        
        # Dessiner l'écran de fin si le jeu est terminé
        if self.end_screen:
            self.clear()
            self.end_screen.draw()

    def est_coherent(self, type_mot: str, cible: str) -> bool:
        """Vérifie si la combinaison type + cible a du sens."""
        # Exemple d'incohérences à éviter :
        if type_mot in ["Peignage", "Démêlage", "Lissage"] and cible not in ["des cheveux", "de la moustache", "des sourcils"]:
            return False
        if type_mot in ["Massage"] and cible not in ["des cheveux", "de la moustache", "des sourcils", "des ongles"]:
            return False
        return True
    
    def generer_phrase(self, niveau):
        type_mot = random.choice(list(TYPES.keys()))
        qualitatif = random.choice(list(QUALIFICATIFS.keys()))
        cible = random.choice(list(CIBLES.keys()))

        # Réessayer si incohérent
        while not self.est_coherent(type_mot, cible):
            type_mot = random.choice(list(TYPES.keys()))
            cible = random.choice(list(CIBLES.keys()))

        if niveau == 1:
            return [type_mot]
        elif niveau == 2:
            return [type_mot, qualitatif]
        elif niveau == 3:
            return [type_mot, qualitatif, cible]
        else:
            raise ValueError("Le niveau doit être 1, 2 ou 3.")
        
    def set_combo_data(self, combinations: dict, words: list):
        self.current_words = words[:]
        self._add_seen_words(words)
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
                    self.character.play_attack_animation()
                    if self.hero_mood < 3:
                        self.hero_mood += 1
                    self.dialog_manager.get_dialog(self.hero_mood)
                    print("QTE réussi ! Sort lancé !")
                    # Lancer l'animation d'attaque
                elif val == -1:
                    self.QTE_PHASE = False
                    if self.hero_mood > 0:
                        self.hero_mood -= 1 
                    self.dialog_manager.get_dialog(self.hero_mood)
                    print("QTE échoué !")
                    self.show_end_screen()  # Défaite
                else:
                    print("QTE continue..")
                    
    def show_end_screen(self):
        self.game_ended = True
        # self.end_screen = EndGame(self, game_results)
                
    def on_update(self, delta_time):
        if not self.QTE_PHASE:
             self.set_combo_data(LISTES, self.generer_phrase(self.LVL))
        if self.QTE_PHASE:
            self.qte_active_timer -= delta_time
            if self.qte_active_timer <= 0:
                self.QTE_PHASE = False
                print("Temps écoulé ! QTE échoué !")
                
        # Mettre à jour l'animation du personnage
        self.character.update(delta_time)


        # Update the dialogue manager
        self.dialog_manager.update(delta_time)

        if self.feedback_timer > 0:
            self.feedback_timer -= delta_time

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
            
        if self.game_ended and self.end_screen:
            self.end_screen.update(delta_time)
            
        
if __name__ == "__main__":
    GameView()
    arcade.run()
