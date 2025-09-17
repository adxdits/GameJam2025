import arcade
import os
from typing import List
from PIL import Image
import tempfile

class SimpleAnimatedSprite(arcade.Sprite):
    """Sprite avec animation simple et fiable"""
    
    def __init__(self, scale=1.0, animation_speed=6):
        super().__init__(scale=scale)
        self.animation_textures = []
        self.current_texture_index = 0
        self.animation_speed = animation_speed
        self.frame_counter = 0
        
        # Propriétés pour les transformations dynamiques
        self.base_textures = []  # Textures originales sans transformations
        self._current_rotation = 0
        self._current_flip_h = False
        self._current_flip_v = False
        
    def set_base_textures(self, textures: List):
        """Définit les textures de base pour permettre les transformations dynamiques"""
        self.base_textures = textures.copy()
        
    def set_position(self, x: float, y: float):
        """
        Définit la position du sprite
        
        Args:
            x: Position X (centre du sprite)
            y: Position Y (centre du sprite)
        """
        self.center_x = x
        self.center_y = y
        
    def move_to(self, x: float, y: float):
        """Alias pour set_position"""
        self.set_position(x, y)
        
    def move_by(self, dx: float, dy: float):
        """
        Déplace le sprite relativement à sa position actuelle
        
        Args:
            dx: Déplacement en X
            dy: Déplacement en Y
        """
        self.center_x += dx
        self.center_y += dy
        
    def apply_transform(self, rotation: float = None, flip_horizontal: bool = None, flip_vertical: bool = None):
        """
        Applique des transformations dynamiques aux textures
        
        Args:
            rotation: Nouvelle rotation en degrés (None = pas de changement)
            flip_horizontal: Nouveau miroir horizontal (None = pas de changement)  
            flip_vertical: Nouveau miroir vertical (None = pas de changement)
        """
        # Mettre à jour les valeurs si fournies
        if rotation is not None:
            self._current_rotation = rotation
        if flip_horizontal is not None:
            self._current_flip_h = flip_horizontal
        if flip_vertical is not None:
            self._current_flip_v = flip_vertical
        
        # Réappliquer les transformations à toutes les textures
        if self.base_textures:
            self.animation_textures = []
            for base_texture in self.base_textures:
                # Note: Cette méthode nécessiterait de stocker le chemin original
                # Pour une approche plus simple, utilisez les paramètres lors de la création
                pass
        
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
                               animation_speed: int = 6,
                               pixel_perfect: bool = True,
                               rotation: float = 0,
                               flip_horizontal: bool = False,
                               flip_vertical: bool = False,
                               position_x: float = 0,
                               position_y: float = 0):
    """
    Crée un sprite animé à partir d'un array de frames.
    
    Args:
        frame_paths: Liste des noms de fichiers des frames
        base_path: Chemin de base vers le dossier des frames
        scale: Échelle du sprite
        animation_speed: Vitesse d'animation (frames avant changement)
        pixel_perfect: Si True, redimensionne avec PIL pour éviter le flou
        rotation: Rotation en degrés (sens horaire)
        flip_horizontal: Miroir horizontal (utile pour faire face à gauche/droite)
        flip_vertical: Miroir vertical
        position_x: Position X du sprite
        position_y: Position Y du sprite
    """
    sprite = SimpleAnimatedSprite(scale=1.0, animation_speed=animation_speed)
    
    # Calculer la taille finale
    target_scale = int(scale) if scale == int(scale) else scale
    
    # Charger toutes les textures
    for frame_path in frame_paths:
        full_path = os.path.join(base_path, frame_path) if base_path else frame_path
        
        if os.path.exists(full_path):
            if pixel_perfect and (scale != 1.0 or rotation != 0 or flip_horizontal or flip_vertical):
                # Appliquer transformations avec PIL pour éviter le flou
                texture = load_texture_scaled_sharp(
                    full_path, 
                    target_scale, 
                    rotation, 
                    flip_horizontal, 
                    flip_vertical
                )
            else:
                texture = arcade.load_texture(full_path)
            
            sprite.animation_textures.append(texture)
        else:
            print(f"Warning: Impossible de trouver {full_path}")
    
    # Définir la première texture
    if sprite.animation_textures:
        sprite.texture = sprite.animation_textures[0]
    
    # Positionner le sprite
    sprite.center_x = position_x
    sprite.center_y = position_y
    
    return sprite

def load_texture_scaled_sharp(image_path: str, scale: float, rotation: float = 0, 
                             flip_horizontal: bool = False, flip_vertical: bool = False):
    """
    Charge et redimensionne une texture sans flou en utilisant PIL
    
    Args:
        image_path: Chemin vers l'image
        scale: Facteur d'échelle
        rotation: Rotation en degrés (sens horaire)
        flip_horizontal: Miroir horizontal
        flip_vertical: Miroir vertical
    """
    try:
        # Ouvrir l'image avec PIL
        pil_image = Image.open(image_path)
        
        # Appliquer les transformations dans l'ordre optimal
        
        # 1. Miroirs d'abord (plus efficace avant rotation)
        if flip_horizontal:
            pil_image = pil_image.transpose(Image.FLIP_LEFT_RIGHT)
        
        if flip_vertical:
            pil_image = pil_image.transpose(Image.FLIP_TOP_BOTTOM)
        
        # 2. Rotation (si nécessaire)
        if rotation != 0:
            # Rotation avec expand=True pour éviter le crop, resample=Image.NEAREST pour pixel-perfect
            pil_image = pil_image.rotate(-rotation, expand=True, resample=Image.NEAREST, fillcolor=(0, 0, 0, 0))
        
        # 3. Redimensionnement en dernier
        if scale != 1.0:
            new_width = int(pil_image.width * scale)
            new_height = int(pil_image.height * scale)
            pil_image = pil_image.resize((new_width, new_height), Image.NEAREST)
        
        # Sauvegarder temporairement
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            pil_image.save(tmp_file.name, 'PNG')
            temp_path = tmp_file.name
        
        # Charger avec Arcade
        texture = arcade.load_texture(temp_path)
        
        # Nettoyer le fichier temporaire
        os.unlink(temp_path)
        
        return texture
        
    except Exception as e:
        print(f"Erreur lors de la transformation de {image_path}: {e}")
        # Fallback vers le chargement normal
        return arcade.load_texture(image_path)

# Alternative : Redimensionner toutes vos images d'un coup
def batch_resize_images(input_folder: str, output_folder: str, scale: int):
    """
    Redimensionne toutes les images d'un dossier avec un rendu net
    Utilisez cette fonction une seule fois pour préparer vos assets
    """
    import glob
    
    os.makedirs(output_folder, exist_ok=True)
    
    # Trouver toutes les images
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif']
    image_files = []
    
    for extension in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_folder, extension)))
    
    print(f"Redimensionnement de {len(image_files)} images...")
    
    for image_path in image_files:
        try:
            # Ouvrir et redimensionner
            pil_image = Image.open(image_path)
            new_size = (pil_image.width * scale, pil_image.height * scale)
            scaled_image = pil_image.resize(new_size, Image.NEAREST)
            
            # Sauvegarder dans le dossier de sortie
            filename = os.path.basename(image_path)
            output_path = os.path.join(output_folder, filename)
            scaled_image.save(output_path, 'PNG')
            
            print(f"✓ {filename} redimensionnée")
            
        except Exception as e:
            print(f"✗ Erreur avec {image_path}: {e}")

# Solution globale pour Arcade (à tester)
def configure_arcade_pixel_perfect():
    """
    Essaie de configurer Arcade globalement pour un rendu net
    """
    try:
        import pyglet.gl as gl
        
        # Configuration OpenGL globale
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        
        print("Configuration OpenGL pixel-perfect appliquée")
        return True
        
    except Exception as e:
        print(f"Configuration OpenGL échouée: {e}")
        return False

# Exemple d'utilisation recommandée
def example_usage():
    """
    Exemple d'utilisation avec position, rotation et miroirs
    """
    
    # Exemple 1: Personnage au centre de l'écran
    player_center = create_animation_from_frames(
        frame_paths=["walk1.png", "walk2.png", "walk3.png"],
        base_path="assets/sprites/",
        scale=4.0,
        position_x=512,  # Centre X d'un écran 1024px
        position_y=384   # Centre Y d'un écran 768px
    )
    
    # Exemple 2: Ennemi dans le coin supérieur droit
    enemy = create_animation_from_frames(
        frame_paths=["enemy1.png", "enemy2.png"],
        base_path="assets/sprites/",
        scale=3.0,
        position_x=900,
        position_y=700,
        flip_horizontal=True  # Regarde vers la gauche
    )
    
    # Exemple 3: Plusieurs sprites aux mêmes positions
    guard_positions = [(200, 300), (400, 300), (600, 300)]
    guards = create_multiple_sprites(
        frame_paths=["guard1.png", "guard2.png"],
        base_path="assets/sprites/",
        positions=guard_positions,
        scale=4.0,
        animation_speed=12
    )
    
    # Exemple 4: Sprite positionné automatiquement
    boss = create_sprite_at_corner(
        frame_paths=["boss1.png", "boss2.png", "boss3.png"],
        base_path="assets/sprites/",
        window_width=1024,
        window_height=768,
        corner="top_right",
        margin=100,  # 100px du bord
        scale=5.0,
        rotation=15  # Légèrement incliné
    )
    
    # Exemple 5: Déplacement dynamique après création
    player = create_animation_from_frames(
        frame_paths=["idle1.png", "idle2.png"],
        base_path="assets/sprites/",
        scale=4.0,
        position_x=100, position_y=100
    )
    
    # Déplacer le sprite après création
    player.move_to(500, 300)  # Nouvelle position absolue
    player.move_by(50, -20)   # Déplacement relatif
    
    return player_center, enemy, guards, boss, player

# Exemple d'utilisation dans une classe de jeu
class GameExample:
    """Exemple d'intégration dans une classe de jeu"""
    
    def __init__(self, window_width=1024, window_height=768):
        self.window_width = window_width
        self.window_height = window_height
        self.sprites = {}
        self.setup_characters()
    
    def setup_characters(self):
        """Configure tous les personnages avec leurs positions"""
        
        # Joueur au centre
        self.sprites['player'] = create_sprite_at_center(
            frame_paths=["player_walk1.png", "player_walk2.png"],
            base_path="assets/sprites/",
            window_width=self.window_width,
            window_height=self.window_height,
            scale=4.0
        )
        
        # Ennemis dans les coins
        corners = ["bottom_left", "bottom_right", "top_left", "top_right"]
        for i, corner in enumerate(corners):
            self.sprites[f'enemy_{i}'] = create_sprite_at_corner(
                frame_paths=["enemy1.png", "enemy2.png"],
                base_path="assets/sprites/",
                window_width=self.window_width,
                window_height=self.window_height,
                corner=corner,
                margin=80,
                scale=3.0,
                flip_horizontal=(corner.endswith("left"))  # Regardent vers le centre
            )
        
        # PNJs alignés en bas
        npc_positions = []
        for i in range(5):
            x = (self.window_width // 6) * (i + 1)
            y = 150
            npc_positions.append((x, y))
        
        npc_sprites = create_multiple_sprites(
            frame_paths=["npc1.png", "npc2.png"],
            base_path="assets/sprites/",
            positions=npc_positions,
            scale=3.5,
            animation_speed=15
        )
        
        for i, npc in enumerate(npc_sprites):
            self.sprites[f'npc_{i}'] = npc
    
    def update(self):
        """Met à jour toutes les animations"""
        for sprite in self.sprites.values():
            sprite.update_animation()
    
    def move_player(self, direction):
        """Déplace le joueur selon la direction"""
        player = self.sprites['player']
        speed = 5
        
        if direction == "up":
            player.move_by(0, speed)
        elif direction == "down":
            player.move_by(0, -speed)
        elif direction == "left":
            player.move_by(-speed, 0)
        elif direction == "right":
            player.move_by(speed, 0)

# Fonction utilitaire pour créer rapidement des variantes
def create_character_animations(base_frames: List[str], base_path: str, scale: float = 4.0, 
                              position_x: float = 0, position_y: float = 0):
    """
    Crée automatiquement les animations dans les 4 directions
    
    Args:
        base_frames: Liste des frames d'animation
        base_path: Chemin vers les sprites
        scale: Échelle des sprites
        position_x: Position X de départ
        position_y: Position Y de départ
    
    Returns:
        dict: Dictionnaire avec les animations 'right', 'left', 'up', 'down'
    """
    animations = {}
    
    # Droite (original)
    animations['right'] = create_animation_from_frames(
        base_frames, base_path, scale, pixel_perfect=True,
        position_x=position_x, position_y=position_y
    )
    
    # Gauche (miroir horizontal)
    animations['left'] = create_animation_from_frames(
        base_frames, base_path, scale, pixel_perfect=True, flip_horizontal=True,
        position_x=position_x, position_y=position_y
    )
    
    # Haut (rotation 270° ou -90°)
    animations['up'] = create_animation_from_frames(
        base_frames, base_path, scale, pixel_perfect=True, rotation=270,
        position_x=position_x, position_y=position_y
    )
    
    # Bas (rotation 90°)
    animations['down'] = create_animation_from_frames(
        base_frames, base_path, scale, pixel_perfect=True, rotation=90,
        position_x=position_x, position_y=position_y
    )
    
    return animations

# Fonctions utilitaires pour le positionnement
def create_sprite_at_center(frame_paths: List[str], base_path: str, 
                           window_width: int, window_height: int, **kwargs):
    """
    Crée un sprite positionné au centre de l'écran
    """
    return create_animation_from_frames(
        frame_paths, base_path,
        position_x=window_width // 2,
        position_y=window_height // 2,
        **kwargs
    )

def create_sprite_at_corner(frame_paths: List[str], base_path: str,
                          window_width: int, window_height: int,
                          corner: str = "bottom_left", margin: int = 50, **kwargs):
    """
    Crée un sprite positionné dans un coin de l'écran
    
    Args:
        corner: "bottom_left", "bottom_right", "top_left", "top_right"
        margin: Marge depuis le bord de l'écran
    """
    positions = {
        "bottom_left": (margin, margin),
        "bottom_right": (window_width - margin, margin),
        "top_left": (margin, window_height - margin),
        "top_right": (window_width - margin, window_height - margin)
    }
    
    x, y = positions.get(corner, (margin, margin))
    
    return create_animation_from_frames(
        frame_paths, base_path,
        position_x=x, position_y=y,
        **kwargs
    )

def create_multiple_sprites(frame_paths: List[str], base_path: str,
                          positions: List[tuple], **kwargs):
    """
    Crée plusieurs sprites aux positions spécifiées
    
    Args:
        positions: Liste de tuples (x, y) pour chaque position
        
    Returns:
        List[SimpleAnimatedSprite]: Liste des sprites créés
    """
    sprites = []
    
    for x, y in positions:
        sprite = create_animation_from_frames(
            frame_paths, base_path,
            position_x=x, position_y=y,
            **kwargs
        )
        sprites.append(sprite)
    
    return sprites

if __name__ == "__main__":
    # Exemple de pré-traitement des images
    # Décommentez pour redimensionner vos assets :
    # batch_resize_images("path/to/small/images", "path/to/large/images", 4)
    pass