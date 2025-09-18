import arcade
import random
from animation.animation_utils import create_animation_from_frames
from pathlib import Path

SOUND_PATH = "../assets/Sounds/"

# Liste des monstres disponibles par niveau
MONSTER_TYPES = {
    0: ["GoblinChauve", "Goblin", "EliteOrc"],        # Niveau 1
    1: ["Orcrider", "Werebear", "WereWolf"],          # Niveau 2
    2: ["Skeleton", "AxesSkeleton", "GreatSword"],    # Niveau 3
    3: ["Boss"]                                       # Niveau 4
}

class Monster():
    def __init__(self, health: int, x: int, y: int, speed: float, level: int = 1, window=None):
        self.window = window

        self.eattack_sound = arcade.load_sound(SOUND_PATH + "eattack.mp3")
        self.death_sound = arcade.load_sound(SOUND_PATH + "death.mp3")
        self.deathboss_sound = arcade.load_sound(SOUND_PATH + "deathboss.mp3")


        self.target_v_height = 800

        self.health = health
        self.x = x
        self.y = y
        self.move_speed = speed
        self.distance_moved = 0
        
        # Sélection aléatoire du type de monstre en fonction du niveau
        self.unit_type = random.choice(MONSTER_TYPES[level])

        if "Boss" in self.unit_type: 
            self.target_v_height = 2000
            self.death_sound = arcade.load_sound(SOUND_PATH + "deathboss.mp3")
                
        # Animation properties
        self.state = "walk"
        self.animations = {}
        self.current_sprite = None
        self.is_dying = False
        self.is_attacking = False
        self._load_animations()
        self.set_state("walk")
        
    def get_coordinates(self):
        return self.x, self.y

    def set_coordinates(self, x: int, y: int):
        self.x = x
        self.y = y
        
    def update_coordinates(self, delta_x: int, delta_y: int):
        prev_x = self.x
        prev_y = self.y
        self.x += delta_x
        self.y += delta_y
        distance = abs(delta_x) + abs(delta_y)
        self.distance_moved += distance
        
        # Si on a effectivement bougé (position changée)
        if distance > 0 and not self.is_dying and not self.is_attacking:
            self.set_state("walk")
        # Si on est arrêté et pas en train d'attaquer/mourir
        elif distance == 0 and not self.is_dying and not self.is_attacking:
            arcade.play_sound(self.eattack_sound,volume=10)
            self.set_state("attack")
        
    def get_speed(self):
        return self.move_speed
    
    def get_distance_moved(self):
        return self.distance_moved
        
    def take_damage(self, damage: float, monster_list=None):            
        self.health -= damage
        print(f"{self.health} points de vie restants.")
        return self.is_defeated(monster_list)
        
    def is_defeated(self, monster_list=None):
        if self.health <= 0:
            self.set_state("death")
            self.is_dying = True
            arcade.play_sound(self.death_sound, volume=10)
            if monster_list and self in monster_list:
                monster_list.remove(self)
                return True
        return False
    
    def _load_animations(self):
        """Charge les animations du monstre"""
        base_path = Path(__file__).resolve().parent.parent / "animation" / "cropped-assets" / self.unit_type
        
        folders_map = {
            "walk": [
                "walk",
                f"{self.unit_type}-walk",
                f"{self.unit_type}-Walking",
                "Wolf-walking",
                f"{self.unit_type}-walking"
            ],
            "attack": [
                "attack",
                f"{self.unit_type}-attack",
                "Wolf-attack",
                f"{self.unit_type}-Attack",
                f"{self.unit_type}-attacks"
            ],
            "death": [
                "death",
                "Death",
                f"{self.unit_type}-death",
                "Wolf-death",
                f"{self.unit_type}-Death"
            ],
            "idle": [
                "stand",
                "standing",
                f"{self.unit_type}-stand",
                f"{self.unit_type}-standing",
                "Wolf-standing",
                f"{self.unit_type}-Standing"
            ]
        }
        
        for anim_type, possible_folders in folders_map.items():
            for folder in possible_folders:
                folder_path = base_path / folder
                if folder_path.exists():
                    frame_files = sorted([f.name for f in folder_path.glob("*.png")])
                    if frame_files:
                        self.animations[anim_type] = create_animation_from_frames(
                            frame_paths=frame_files,
                            base_path=str(folder_path),
                            scale=8.0,
                            position_x=0,
                            position_y=0
                        )
                        break

    def set_state(self, new_state):
        """Change l'état et l'animation du monstre"""
        if new_state in self.animations:
            self.state = new_state
            self.current_sprite = self.animations[new_state]

    def update(self, delta_time):
        """Met à jour l'animation"""
        if self.current_sprite:
            self.current_sprite.update_animation(delta_time)
            
            if self.window is not None:
                cx = self.window._sx(self.x)
                cy = self.window._sy(self.y)
                self.current_sprite.center_x = cx
                self.current_sprite.center_y = cy

                # Scale en fonction de la hauteur virtuelle cible + ui_scale
                tex = self.current_sprite.texture
                if tex and tex.height > 0:
                    scale_virtual = self.target_v_height / tex.height
                else:
                    scale_virtual = 1.0
                self.current_sprite.scale = scale_virtual * self.window.ui_scale
            else:
                # Fallback si pas de window fournie
                self.current_sprite.center_x = self.x
                self.current_sprite.center_y = self.y
                self.current_sprite.scale = 1.0

            # Gestion de l'animation d'attaque
            if self.is_attacking and self.state == "attack":
                # Si l'animation d'attaque est terminée
                if hasattr(self.current_sprite, 'frame_num'):
                    if self.current_sprite.frame_num >= len(self.current_sprite.frames) - 1:
                        self.is_attacking = False
                        self.set_state("idle")
            
            # Gestion de l'animation de mort
            if self.is_dying and self.state == "death":
                # Si l'animation de mort est terminée
                if hasattr(self.current_sprite, 'frame_num'):
                    if self.current_sprite.frame_num >= len(self.current_sprite.frames) - 1:
                        return True
        return False

    def on_draw(self):
        """Dessine le monstre"""
        if self.current_sprite:
            self.current_sprite.draw()