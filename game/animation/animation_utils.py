import arcade
import os
from typing import List

class SimpleAnimatedSprite(arcade.Sprite):
    """Sprite avec animation simple et fiable"""
    
    def __init__(self, scale=1.0, animation_speed=6):
        super().__init__(scale=scale)
        self.animation_textures = []
        self.current_texture_index = 0
        self.animation_speed = animation_speed
        self.frame_counter = 0
        
    def update_animation(self, delta_time=1/60):
        """Met à jour l'animation"""
        if len(self.animation_textures) > 1:
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed:
                self.frame_counter = 0
                self.current_texture_index += 1
                if self.current_texture_index >= len(self.animation_textures):
                    self.current_texture_index = 0
                self.texture = self.animation_textures[self.current_texture_index]

def create_animation_from_frames(frame_paths: List[str], 
                               base_path: str = "", 
                               scale: float = 1.0,
                               animation_speed: int = 6):
    """
    Crée un sprite animé à partir d'un array de frames.
    
    Args:
        frame_paths: Liste des noms de fichiers des frames
        base_path: Chemin de base vers le dossier des frames
        scale: Échelle du sprite
        animation_speed: Vitesse d'animation (frames avant changement, plus petit = plus rapide)
        
    Returns:
        SimpleAnimatedSprite: Sprite animé prêt à utiliser
    """
    sprite = SimpleAnimatedSprite(scale=scale, animation_speed=animation_speed)
    
    # Charger toutes les textures
    for frame_path in frame_paths:
        full_path = os.path.join(base_path, frame_path) if base_path else frame_path
        
        if os.path.exists(full_path):
            texture = arcade.load_texture(full_path)
            sprite.animation_textures.append(texture)
        else:
            print(f"Warning: Impossible de trouver {full_path}")
    
    # Définir la première texture
    if sprite.animation_textures:
        sprite.texture = sprite.animation_textures[0]
    
    return sprite