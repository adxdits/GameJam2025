import json
import os
import arcade

class DialogManager:
    def __init__(self):
        self.current_dialog = ""
        self.timer = 0
        self.display_time = 3  # Display time in seconds
        self.dialogs = self.load_dialogs()

        # Load the bubble image
        bubble_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/HeroReactions/bubbles.png"))
        self.bubble_texture = arcade.load_texture(bubble_path)

        # Set the font path
        self.font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/Fonts/digital_disco/digital_disco.ttf"))

    def load_dialogs(self):
        """Load dialogs from the JSON file."""
        dialogs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/HeroReactions/dialogs.json"))
        with open(dialogs_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_dialog(self, mood):
        """Retrieve a random dialog based on the hero's mood."""
        import random        
        if str(mood) in self.dialogs:
            self.current_dialog = random.choice(self.dialogs[str(mood)])
            self.timer = self.display_time

    def update(self, delta_time):
        """Update the timer for dialog display."""
        if self.timer > 0:
            self.timer -= delta_time

    def draw(self):
        """Draw the dialog bubble and text if the timer is active."""
        if self.timer > 0:
            # Draw the bubble image
            bubble_x = 400  # X position of the bubble
            bubble_y = 500  # Y position of the bubble
            bubble_width = 300
            bubble_height = 150
            arcade.draw_texture_rectangle(bubble_x, bubble_y, bubble_width, bubble_height, self.bubble_texture)

            # Draw the dialog text
            text_x = bubble_x - bubble_width // 2 + 20  # Adjust text position inside the bubble
            text_y = bubble_y - 20
            arcade.draw_text(
                self.current_dialog,
                text_x,
                text_y,
                arcade.color.WHITE,
                14,
                width=bubble_width - 40,  # Leave some padding inside the bubble
                align="center",
                font_name=self.font_path
            )