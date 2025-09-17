import arcade
from animation.animation_utils import create_animation_from_frames
from pathlib import Path


class Character:
    def __init__(self, window):
        self.window = window
        self.state = "idle"
        self.animations = {}
        
        # Position initiale
        self.x = 700
        self.y = 850
        
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
            scale=9.0,
            flip_horizontal=True,
            position_x=self.x,
            position_y=self.y
        )
        
        self.animations["attack"] = create_animation_from_frames(
            frame_paths=["Priest047.png", "Priest048.png", "Priest049.png", 
                        "Priest050.png", "Priest051.png"],
            base_path=str(base_path / "Priest-Healing"),
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
            
    def draw(self):
        """Dessine le personnage"""
        if self.current_sprite:
            self.current_sprite.draw()
            
    def play_attack_animation(self):
        """Lance l'animation d'attaque"""
        self.set_state("attack")
        # Retourner à l'état idle après un délai
        arcade.schedule(lambda dt: self.set_state("idle"), 0.5)