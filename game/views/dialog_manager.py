import json
import os
import arcade

class DialogManager:
    def __init__(self):
        self.current_dialog = ""
        self.timer = 0
        self.display_time = 3  # Display time in seconds

        # Load the bubble image
        bubble_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/HeroReactions/bubbles.png"))
        self.bubble_texture = arcade.load_texture(bubble_path)
        print(f"Loading bubble texture from: {bubble_path}")
        print(f"Bubble texture loaded: {self.bubble_texture is not None}")

        # Load and register the custom font
        try:
            font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/Fonts/digital_disco/DigitalDisco.ttf"))
            print(f"Loading font from: {font_path}")
            
            if os.path.exists(font_path):
                # Charger et enregistrer la police avec son nom de base
                arcade.load_font(font_path)
                self.font_name = "DigitalDisco"  # Utiliser le nom de base de la police
                print(f"Font successfully loaded from {font_path}")
            else:
                print(f"Font file not found at {font_path}")
                self.font_name = "Arial"
        except Exception as e:
            print(f"Warning: Font loading error: {e}")
            self.font_name = "Arial"

        # Load dialogs
        self.dialogs = self.load_dialogs()
        print(f"Dialogs loaded: {len(self.dialogs)} moods available")

    def load_dialogs(self):
        """Load dialogs from the JSON file."""
        try:
            dialogs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/HeroReactions/dialogs.json"))
            print(f"Loading dialogs from: {dialogs_path}")
            with open(dialogs_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading dialogs: {e}")
            return {}

    def get_dialog(self, mood):
        """Retrieve a random dialog based on the hero's mood."""
        import random
        mood_str = str(mood)
        if mood_str in self.dialogs:
            self.current_dialog = random.choice(self.dialogs[mood_str])
            self.timer = self.display_time
            print(f"New dialog selected: {self.current_dialog}")
        else:
            print(f"No dialogs found for mood: {mood}")

    def update(self, delta_time):
        """Update the timer for dialog display."""
        if self.timer > 0:
            self.timer -= delta_time

    def draw_bubble(self, text, is_qte=False):
        """Draw the dialog bubble with the specified text, scaled to UI."""
        window = arcade.get_window()
        screen_width = window.width
        screen_height = window.height

        ui_scale = getattr(window, "ui_scale", 1.0)

        # Dimensions de base
        base_width = 400
        base_height = 200

        # Appliquer le scale
        bubble_width = int(base_width * ui_scale)
        bubble_height = int(base_height * ui_scale)

        # Position (haut de l’écran)
        bubble_x = screen_width // 2
        bubble_y = screen_height - bubble_height * 3 - int(20 * ui_scale)

        # Bulle
        if self.bubble_texture:
            arcade.draw_texture_rectangle(
                bubble_x, bubble_y, bubble_width, bubble_height, self.bubble_texture, alpha=255
            )

        # Texte
        if text:
            arcade.draw_text(
                text,
                bubble_x,  # centre de la bulle
                bubble_y + int(bubble_height * 0.10),  # centre vertical
                arcade.color.BLACK,
                int(20 * ui_scale),
                width=bubble_width - int(80 * ui_scale),
                align="center",
                multiline=True,
                font_name=self.font_name,
                anchor_x="center",
                anchor_y="center",
            )

    def draw(self):
        """Draw the appropriate bubble based on the current state."""
        if self.timer > 0:
            # Si un dialogue de héros est actif, l'afficher
            self.draw_bubble(self.current_dialog)