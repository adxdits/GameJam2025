import arcade
import os

# Animation constants
LANCER_SCALE = 2.0
ANIMATION_SPEED = 0.1  # Lower values = slower animation

class LancerWalkingGame(arcade.Window):
    """
    Main application class for the Lancer walking animation.
    """

    def __init__(self):
        # ----------- Hero Animation Setup ----------- #

        # Sprite lists
        self.player_list = None
        
        # Player sprite
        self.player_sprite = None
        
        # Animation variables
        self.current_texture = 0
        self.texture_change_distance = 0
        self.animation_timer = 0
        self.auto_animate = False
        
        # Load walking textures
        self.walking_textures = []
        
        # -------------------------------------------- #

    def setup(self):
        """Set up the game and initialize variables."""
        
        # Create sprite lists
        self.player_list = arcade.SpriteList()
        
        # Set up the player sprite
        self.player_sprite = arcade.Sprite()
        self.player_sprite.scale = LANCER_SCALE
        
        # Load all walking animation frames
        self.load_walking_textures()
        
        # Set the initial texture
        if self.walking_textures:
            self.player_sprite.texture = self.walking_textures[0]
        
        # Position the player in the center of the screen
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = SCREEN_HEIGHT // 2
        
        # Add player to sprite list
        self.player_list.append(self.player_sprite)

    def load_walking_textures(self):
        """Load all the walking animation textures."""
        
        # Path to the walking animation frames
        walk_path = "cropped-assets/Lancer/Lancer-walk"
        
        # Walking animation frame filenames
        walk_frames = [
            "lancer-walk001.png",
            "lancer-walk002.png",
            "lancer-walk003.png",
            "lancer-walk004.png",
            "lancer-walk005.png",
            "lancer-walk006.png",
            "lancer-walk007.png",
            "lancer-walk008.png"
        ]
        
        # Load each frame
        for frame in walk_frames:
            frame_path = os.path.join(walk_path, frame)
            if os.path.exists(frame_path):
                texture = arcade.load_texture(frame_path)
                self.walking_textures.append(texture)
            else:
                print(f"Warning: Could not find {frame_path}")

    def on_draw(self):
        """Render the screen."""
        
        # Clear the screen
        self.clear()
        
        # Draw all sprite lists
        self.player_list.draw()
        
        # Draw instructions
        arcade.draw_text("Lancer Walking Animation", 10, SCREEN_HEIGHT - 30,
                        arcade.color.WHITE, 20)
        arcade.draw_text("Press SPACE to start/stop walking", 10, SCREEN_HEIGHT - 60,
                        arcade.color.WHITE, 16)
        arcade.draw_text("Use ARROW keys to move", 10, SCREEN_HEIGHT - 85,
                        arcade.color.WHITE, 16)

    def on_update(self, delta_time):
        """Movement and game logic."""
        
        # Update all sprites
        self.player_list.update()
        
        # Update animation timer
        self.animation_timer += delta_time
        
        # Update animation
        self.update_animation()

    



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        
        # Movement keys
        if key == arcade.key.UP:
            self.player_sprite.change_y = 200
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -200
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -200
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 200
        elif key == arcade.key.SPACE:
            # Toggle walking animation even when not moving
            self.auto_animate = not self.auto_animate
            if not self.auto_animate:
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    """Main function"""
    game = LancerWalkingGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
