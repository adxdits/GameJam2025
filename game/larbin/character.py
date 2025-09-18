import arcade
from animation.animation_utils import create_animation_from_frames
from pathlib import Path

# --- Cache global pour partager les animations entre toutes les instances ---
_ANIMATION_CACHE = {}

class Character:
    def __init__(self, window):
        self.window = window
        self.state = "idle"
        self.animations = {}
        
        # Position initiale
        self.x = 1200
        self.y = 120
        self.target_v_height = 800
        
        # Pour gérer l'animation d'attaque
        self.attack_duration = 0.5
        self.attack_time = 0
        self.is_attacking = False
        
        self._load_animations()
        self.current_sprite = None
        self.set_state("idle")
        
    def _load_animations(self):
        """Charge les animations avec cache global"""
        global _ANIMATION_CACHE
        base_path = Path(__file__).resolve().parent.parent.parent / "game" / "animation" / "cropped-assets" / "Priest"
        
        animation_defs = {
            "idle": {
                "frames": ["Priest001.png", "Priest002.png", "Priest003.png", 
                           "Priest004.png", "Priest005.png", "Priest006.png"],
                "folder": "Priest-standing"
            },
            "attack": {
                "frames": ["Priest047.png", "Priest048.png", "Priest049.png", 
                           "Priest050.png", "Priest051.png"],
                "folder": "Priest-Healing"
            }
        }

        for state, anim in animation_defs.items():
            cache_key = f"Priest-{state}"
            if cache_key not in _ANIMATION_CACHE:
                _ANIMATION_CACHE[cache_key] = create_animation_from_frames(
                    frame_paths=anim["frames"],
                    base_path=str(base_path / anim["folder"]),
                    scale=7.0,  # Scale appliqué plus tard dans draw()
                    flip_horizontal=True,
                    position_x=0,
                    position_y=0
                )
            self.animations[state] = _ANIMATION_CACHE[cache_key]
            
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
        """Dessine avec conversion virtuel -> écran + scale UI"""
        if not self.current_sprite:
            return

        cx = self.window._sx(self.x)
        cy = self.window._sy(self.y)

        tex = self.current_sprite.texture
        scale_virtual = self.target_v_height / tex.height if tex and tex.height > 0 else 1.0
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
