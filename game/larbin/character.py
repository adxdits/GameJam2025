import arcade
from animation.animation_utils import create_animation_from_frames
from pathlib import Path


class Character:
    def __init__(self, window):
        self.window = window
        self.state = "idle"
        self.animations = {}
        
        # Position initiale
        self.x = 1200
        self.y = 200
        self.target_v_height = 800
        
        # Pour gérer l'animation d'attaque
        self.attack_duration = 0.5  # Durée de l'animation d'attaque
        self.attack_time = 0  # Temps écoulé depuis le début de l'attaque
        self.is_attacking = False
        
        self._load_animations()
        self.current_sprite = None
        self.set_state("idle")
        
    def _load_animations(self):
        base_path = Path(__file__).resolve().parent.parent.parent / "game" / "animation" / "cropped-assets" / "Priest"
        
        # Charger différentes animations
        self.animations["idle"] = create_animation_from_frames(
            frame_paths=["Priest001.png", "Priest002.png", "Priest003.png", 
                        "Priest004.png", "Priest005.png", "Priest006.png"],
            base_path=str(base_path / "Priest-standing"),
            scale=7.0,
            flip_horizontal=True,
            position_x=0,
            position_y=0
        )
        
        self.animations["attack"] = create_animation_from_frames(
            frame_paths=["Priest047.png", "Priest048.png", "Priest049.png", 
                        "Priest050.png", "Priest051.png"],
            base_path=str(base_path / "Priest-Healing"),
            scale=7.0,
            flip_horizontal=True,
            position_x=0,
            position_y=0
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
        """Dessine avec conversion virtuel -> écran + scale UI."""
        if not self.current_sprite:
            return

        # Position (virtuel -> écran)
        cx = self.window._sx(self.x)
        cy = self.window._sy(self.y)

        # Échelle calculée pour que la texture ait target_v_height en VIRTUEL,
        # puis on applique le ui_scale pour l’écran.
        tex = self.current_sprite.texture  # frame courante
        if tex and tex.height > 0:
            scale_virtual = self.target_v_height / tex.height
        else:
            scale_virtual = 1.0

        sc = scale_virtual * self.window.ui_scale

        self.current_sprite.center_x = cx
        self.current_sprite.center_y = cy
        self.current_sprite.scale = sc

        self.current_sprite.draw()
            
    def play_attack_animation(self):
        """Lance l'animation d'attaque"""
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_time = 0
            self.set_state("attack")