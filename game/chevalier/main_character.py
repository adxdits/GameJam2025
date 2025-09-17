import arcade
from animation.animation_utils import create_animation_from_frames
from pathlib import Path


class MainCharacter:
    def __init__(self, window):
        self.window = window
        self.state = "idle"
        self.animations = {}
        
        # Position initiale
        self.x = 900
        self.y = 200
        
        # Pour gérer l'animation d'attaque
        self.attack_duration = 0.5  # Durée de l'animation d'attaque
        self.attack_time = 0  # Temps écoulé depuis le début de l'attaque
        self.is_attacking = False
        
        self._load_animations()
        self.current_sprite = None
        self.set_state("idle")
        
    def _load_animations(self):
        base_path = Path(__file__).resolve().parent.parent.parent / "game" / "animation" / "cropped-assets" / "Lancer"
        
        # Charger différentes animations
        self.animations["idle"] = create_animation_from_frames(
            frame_paths=["standing001.png", "standing002.png", "standing003.png", "standing004.png", 
                        "standing005.png", "standing006.png"],
            base_path=str(base_path / "Lancer-standing"),
            scale=9.0,
            flip_horizontal=True,
            position_x=self.x,
            position_y=self.y
        )

        self.animations["attack"] = create_animation_from_frames(
            frame_paths=["Lancer-attack001.png", "Lancer-attack002.png", "Lancer-attack003.png", 
                        "Lancer-attack004.png", "Lancer-attack005.png", "Lancer-attack006.png"],
            base_path=str(base_path / "Lancer-attack"),
            scale=9.0,
            flip_horizontal=True,
            position_x=self.x,
            position_y=self.y
        )
            
    def set_state(self, new_state):
        """Change l'état et l'animation du personnage"""
        if new_state in self.animations:
            self.state = new_state
            self.current_sprite = self.animations[new_state]
            
    def update(self, delta_time):
        """Met à jour l'animation"""
        if self.current_sprite:
            self.current_sprite.update_animation(delta_time)
            
            # Gérer la fin de l'animation d'attaque
            if self.is_attacking:
                self.attack_time += delta_time
                if self.attack_time >= self.attack_duration:
                    self.is_attacking = False
                    self.attack_time = 0
                    self.set_state("idle")
            
    def draw(self):
        """Dessine le personnage"""
        if self.current_sprite:
            self.current_sprite.draw()
            
    def play_attack_animation(self):
        """Lance l'animation d'attaque"""
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_time = 0
            self.set_state("attack")