import arcade
from pathlib import Path

class EndGame:
    def __init__(self, window, victory: bool = True):
        self.window = window
        self.victory = victory

        # Chemin des assets
        project_root = Path(__file__).resolve().parent.parent.parent
        bg_path = project_root / "assets" / "End" / "cobble_road.png"
        image_path = project_root / "assets" / "End" / "journal.png"

        # Background
        self.background = arcade.Sprite(str(bg_path))
        self.background.center_x = self.window.width // 2
        self.background.center_y = self.window.height // 2
        self.background.scale = max(
            self.window.width / self.background.width,
            self.window.height / self.background.height
        )* 1.25

        # Image animée
        self.image = arcade.Sprite(str(image_path))
        self.image.center_x = self.window.width // 2
        self.image.center_y = self.window.height // 2
        self.image.scale = 2.0  # commence grande
        self.image.angle = 0

        # Animation
        self.target_scale = 0.8
        self.target_angle = 40
        self.scale_speed = 0.065
        self.rotation_speed = 1.0
        self.animation_done = False

        # Fondu au noir
        self.fade_alpha = 255  # commence noir
        self.fade_speed = 5    # vitesse du fondu
        self.fade_done = False

    def update(self, delta_time: float):
        # Fondu entrant : réduire alpha
        if not self.fade_done:
            self.fade_alpha -= self.fade_speed
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_done = True  # fin du fondu

        # Réduction progressive du scale et rotation pendant le fondu
        if not self.fade_done:  # Pendant le fondu
            # Réduction de l'échelle avec easing
            if self.image.scale > self.target_scale:
                diff = self.image.scale - self.target_scale
                self.image.scale -= diff * self.scale_speed
                if self.image.scale < self.target_scale:
                    self.image.scale = self.target_scale

            # Rotation progressive
            if self.image.angle < self.target_angle:
                diff_angle = self.target_angle - self.image.angle
                self.image.angle += diff_angle * 0.05  # easing rotation
                if self.image.angle > self.target_angle:
                    self.image.angle = self.target_angle

        # Vérifier si l'animation est terminée
        if self.fade_done and self.image.scale == self.target_scale and self.image.angle == self.target_angle:
            self.animation_done = True

    def draw(self):
        # Dessiner le fond et l'image
        self.background.draw()
        self.image.draw()
        message = "" if self.victory else ""
        arcade.draw_text(
            message,
            self.window.width // 2,
            self.window.height // 2 + 150,
            arcade.color.WHITE,
            30,
            anchor_x="center"
        )

        # Dessiner le fondu noir par-dessus
        if self.fade_alpha > 0:
            arcade.draw_lrtb_rectangle_filled(
                0, self.window.width,
                self.window.height, 0,
                (0, 0, 0, int(self.fade_alpha))
            )
