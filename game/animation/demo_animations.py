import arcade
from animation_utils import create_animated_sprite_from_frames, create_animated_sprite_from_folder, AnimatedSprite

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Animation Demo - Multiple Characters"

class MultiCharacterDemo(arcade.Window):
    """
    Démonstration de l'utilisation des fonctions d'animation.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.DARK_GRAY)

        # Sprite lists
        self.all_sprites = arcade.SpriteList()
        
        # Characters
        self.characters = {}

    def setup(self):
        """Set up the game and initialize variables."""
        
        # 1. Lancer - Animation de marche depuis une liste de frames
        lancer_frames = [
            "lancer-walk001.png", "lancer-walk002.png", "lancer-walk003.png", "lancer-walk004.png",
            "lancer-walk005.png", "lancer-walk006.png", "lancer-walk007.png", "lancer-walk008.png"
        ]
        
        lancer = create_animated_sprite_from_frames(
            frame_paths=lancer_frames,
            base_path="cropped-assets/Lancer/Lancer-walk",
            scale=2.0,
            animation_speed=8
        )
        lancer.center_x = 150
        lancer.center_y = 300
        self.all_sprites.append(lancer)
        self.characters['lancer'] = lancer
        
        # 2. Goblin - Animation d'attaque depuis un dossier
        goblin = create_animated_sprite_from_folder(
            folder_path="cropped-assets/Goblin/Goblin-attack",
            scale=2.0,
            animation_speed=6
        )
        goblin.center_x = 350
        goblin.center_y = 300
        self.all_sprites.append(goblin)
        self.characters['goblin'] = goblin
        
        # 3. Boss - Animation de marche depuis un dossier
        boss = create_animated_sprite_from_folder(
            folder_path="cropped-assets/Boss/Boss-Walking",
            scale=1.5,
            animation_speed=10
        )
        boss.center_x = 550
        boss.center_y = 300
        self.all_sprites.append(boss)
        self.characters['boss'] = boss
        
        # 4. Priest - Animation de soin depuis un dossier
        priest = create_animated_sprite_from_folder(
            folder_path="cropped-assets/Priest/Priest-Healing",
            scale=2.0,
            animation_speed=5
        )
        priest.center_x = 750
        priest.center_y = 300
        self.all_sprites.append(priest)
        self.characters['priest'] = priest
        
        # 5. Sprite avec multiple animations (exemple avancé)
        multi_anim_sprite = AnimatedSprite(scale=2.0)
        
        # Charger plusieurs animations pour le même sprite
        multi_anim_sprite.load_animation_from_folder("walk", "cropped-assets/Lancer/Lancer-walk")
        multi_anim_sprite.load_animation_from_folder("attack", "cropped-assets/Lancer/Lancer-attack")
        multi_anim_sprite.load_animation_from_folder("hurt", "cropped-assets/Lancer/Lancer-hurts")
        
        # Commencer avec l'animation de marche
        multi_anim_sprite.play_animation("walk")
        multi_anim_sprite.center_x = 850
        multi_anim_sprite.center_y = 450
        self.all_sprites.append(multi_anim_sprite)
        self.characters['multi'] = multi_anim_sprite

    def on_draw(self):
        """Render the screen."""
        
        # Clear the screen
        self.clear()
        
        # Draw all sprites
        self.all_sprites.draw()
        
        # Draw instructions
        arcade.draw_text("Animation Demo avec Arcade", 10, SCREEN_HEIGHT - 30,
                        arcade.color.WHITE, 24)
        
        # Labels pour chaque personnage
        arcade.draw_text("Lancer\n(Marche)", 80, 200, arcade.color.WHITE, 14)
        arcade.draw_text("Goblin\n(Attaque)", 280, 200, arcade.color.WHITE, 14)
        arcade.draw_text("Boss\n(Marche)", 480, 200, arcade.color.WHITE, 14)
        arcade.draw_text("Priest\n(Soin)", 680, 200, arcade.color.WHITE, 14)
        arcade.draw_text("Multi-Anim\n(Touche M)", 780, 350, arcade.color.WHITE, 14)
        
        # Instructions
        arcade.draw_text("Touches:", 10, SCREEN_HEIGHT - 80, arcade.color.YELLOW, 16)
        arcade.draw_text("ESPACE: Pause/Play toutes les animations", 10, SCREEN_HEIGHT - 110, arcade.color.WHITE, 12)
        arcade.draw_text("M: Changer animation du sprite multi (marche/attaque/blessure)", 10, SCREEN_HEIGHT - 130, arcade.color.WHITE, 12)
        arcade.draw_text("+ / -: Augmenter/Diminuer vitesse", 10, SCREEN_HEIGHT - 150, arcade.color.WHITE, 12)

    def on_update(self, delta_time):
        """Movement and game logic."""
        
        # Update all sprites
        self.all_sprites.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        
        if key == arcade.key.SPACE:
            # Toggle pause/play pour tous les sprites
            for sprite in self.all_sprites:
                if hasattr(sprite, 'is_animating'):
                    if sprite.is_animating:
                        sprite.pause_animation()
                    else:
                        sprite.play_animation()
        
        elif key == arcade.key.M:
            # Changer l'animation du sprite multi-animation
            multi_sprite = self.characters.get('multi')
            if multi_sprite and hasattr(multi_sprite, 'current_animation'):
                if multi_sprite.current_animation == "walk":
                    multi_sprite.play_animation("attack")
                elif multi_sprite.current_animation == "attack":
                    multi_sprite.play_animation("hurt")
                else:
                    multi_sprite.play_animation("walk")
        
        elif key == arcade.key.PLUS or key == arcade.key.EQUAL:
            # Augmenter vitesse (diminuer frames_per_change)
            for sprite in self.all_sprites:
                if hasattr(sprite, 'texture_change_frames'):
                    sprite.texture_change_frames = max(1, sprite.texture_change_frames - 1)
        
        elif key == arcade.key.MINUS:
            # Diminuer vitesse (augmenter frames_per_change)
            for sprite in self.all_sprites:
                if hasattr(sprite, 'texture_change_frames'):
                    sprite.texture_change_frames = min(20, sprite.texture_change_frames + 1)


def main():
    """Main function"""
    game = MultiCharacterDemo()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()