import arcade

class Monster():
    def __init__(self, health: int, x: int, y: int, speed: float):
        self.health = health
        self.x = x
        self.y = y
        self.move_speed = speed
        self.distance_moved = 0  # distance parcouru cumulée
        
    def get_coordinates(self):
        return self.x, self.y

    def set_coordinates(self, x: int, y: int):
        self.x = x
        self.y = y
        
    def update_coordinates(self, delta_x: int, delta_y: int):
        self.x += delta_x
        self.y += delta_y
        self.distance_moved += abs(delta_x) + abs(delta_y)  # distance parcouru cumulée
        
    def get_speed(self):
        return self.move_speed
    
    def get_distance_moved(self):
        return self.distance_moved
        
    def take_damage(self, damage: float, monster_list=None):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"{self.health} points de vie restants.")

        if self.is_defeated(monster_list):
            print("Le monstre est vaincu !")

    def is_defeated(self, monster_list=None) -> bool:
        if self.health <= 0:
            # Supprimer de la liste si elle est fournie
            if monster_list is not None and self in monster_list:
                monster_list.remove(self)
            return True
        return False
    
    def on_draw(self):
        arcade.draw_rectangle_filled(
            center_x=self.x,
            center_y=self.y,
            width=40,
            height=40,
            color=arcade.color.BLUE
        )