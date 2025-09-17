import arcade
import random
from animation.animation_utils import create_animation_from_frames
from pathlib import Path

# Définir les unités disponibles par niveau
UNITS_BY_LEVEL = {
    1: ["Goblin", "Skeleton", "EliteOrc"],  # Unités de base
    2: ["GoblinSword", "GreatSword", "Orcrider"],  # Unités intermédiaires
    3: ["Boss", "Werebear", "WereWolf"]  # Unités avancées
}

class Monster:
    def __init__(self, health: int, x: int, y: int, speed: float, unit_type: str, window=None):
        self.health = health
        self.x = x
        self.y = y
        self.move_speed = speed
        self.distance_moved = 0
        self.window = window  # Store the window reference for animations
        
        # Animation properties
        self.state = "idle"
        self.animations = {}
        self.current_sprite = None
        self.unit_type = unit_type
        
        # Pour gérer l'animation d'attaque/mort
        self.is_attacking = False
        self.is_dying = False
        self.animation_time = 0
        self.attack_duration = 0.5
        self.death_duration = 0.7
        
        self._load_animations()
        self.set_state("idle")
        
    def _load_animations(self):
        base_path = Path(__file__).resolve().parent.parent / "animation" / "cropped-assets" / self.unit_type
        
        # Définir les chemins des animations selon le type d'unité
        animation_folders = {
            "idle": f"{self.unit_type}-standing" if "-" in self.unit_type else "standing",
            "attack": f"{self.unit_type}-attack" if "-" in self.unit_type else "attack",
            "death": f"{self.unit_type}-death" if "-" in self.unit_type else "death",
            "walk": f"{self.unit_type}-walk" if "-" in self.unit_type else "walk"
        }
        
        # Charger chaque animation
        for anim_type, folder in animation_folders.items():
            anim_path = base_path / folder
            if anim_path.exists():
                # Récupérer tous les fichiers PNG du dossier
                frame_files = sorted([f.name for f in anim_path.glob("*.png")])
                if frame_files:
                    self.animations[anim_type] = create_animation_from_frames(
                        frame_paths=frame_files,
                        base_path=str(anim_path),
                        scale=3.0,
                        position_x=self.x,
                        position_y=self.y
                    )
        
    def set_state(self, new_state):
        """Change l'état et l'animation du monstre"""
        if new_state in self.animations:
            self.state = new_state
            self.current_sprite = self.animations[new_state]
            
    def update(self, delta_time):
        """Met à jour l'animation et l'état"""
        if self.current_sprite:
            self.current_sprite.update_animation(delta_time)
            
            # Update the sprite position to match the monster position
            self.current_sprite.center_x = self.x
            self.current_sprite.center_y = self.y
            
            # Gérer l'animation d'attaque
            if self.is_attacking:
                self.animation_time += delta_time
                if self.animation_time >= self.attack_duration:
                    self.is_attacking = False
                    self.animation_time = 0
                    self.set_state("idle")
                    
            # Gérer l'animation de mort
            if self.is_dying:
                self.animation_time += delta_time
                if self.animation_time >= self.death_duration:
                    self.is_dying = False
                    self.animation_time = 0
                    return True  # Le monstre peut être supprimé
                    
        return False
            
    def draw(self):
        """Dessine le monstre"""
        if self.current_sprite:
            self.current_sprite.draw()
            
    def play_attack_animation(self):
        """Lance l'animation d'attaque"""
        if not self.is_attacking and not self.is_dying:
            self.is_attacking = True
            self.animation_time = 0
            self.set_state("attack")
            
    def play_death_animation(self):
        """Lance l'animation de mort"""
        if not self.is_dying:
            self.is_dying = True
            self.animation_time = 0
            self.set_state("death")

    def take_damage(self, damage: float, monster_list=None):
        self.health -= damage
        if self.health <= 0:
            self.play_death_animation()
        else:
            # Jouer une animation de hit si disponible
            if "hurt" in self.animations:
                self.set_state("hurt")
                
    @staticmethod
    def get_random_units_for_level(level: int, count: int = 3):
        """Retourne une liste d'unités aléatoires pour un niveau donné"""
        if level in UNITS_BY_LEVEL:
            return random.sample(UNITS_BY_LEVEL[level], count)
        return []