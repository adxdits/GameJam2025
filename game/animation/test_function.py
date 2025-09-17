import arcade
from animation_utils import create_animation_from_frames

# Exemple d'utilisation de la fonction
class TestAnimation(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Test Animation Function")
        self.sprite_list = arcade.SpriteList()
        
    def setup(self):
        # Utilisation ultra-simple de la fonction
        frames = [
            "lancer-walk001.png", "lancer-walk002.png", "lancer-walk003.png", "lancer-walk004.png",
            "lancer-walk005.png", "lancer-walk006.png", "lancer-walk007.png", "lancer-walk008.png"
        ]
        
        # Créer l'animation en une ligne !
        animated_sprite = create_animation_from_frames(
            frame_paths=frames,
            base_path="cropped-assets/Lancer/Lancer-walk",
            scale=2.0,
            animation_speed=8
        )
        
        animated_sprite.center_x = 400
        animated_sprite.center_y = 300
        self.sprite_list.append(animated_sprite)
        
    def on_draw(self):
        self.clear()
        self.sprite_list.draw()
        
        arcade.draw_text("Animation créée avec create_animation_from_frames()", 
                        10, 550, arcade.color.WHITE, 20)
        arcade.draw_text("frames = ['frame1.png', 'frame2.png', ...]", 
                        10, 50, arcade.color.YELLOW, 16)
        arcade.draw_text("sprite = create_animation_from_frames(frames, 'path/', scale=2.0)", 
                        10, 20, arcade.color.YELLOW, 16)
        
    def on_update(self, delta_time):
        # Mettre à jour les sprites ET leur animation
        self.sprite_list.update()
        
        # Mettre à jour manuellement l'animation pour chaque sprite
        for sprite in self.sprite_list:
            if hasattr(sprite, 'update_animation'):
                sprite.update_animation(delta_time)

def main():
    game = TestAnimation()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()