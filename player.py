import pygame
import random

from animation import AnimateSprite


# La classe "Player" hérite de la classe parente "Sprite" de pygame.sprite
class Entity(AnimateSprite):
    """Classe d'une entité"""

    def __init__(self, name, x, y):
        """Constructeur qui initialise la Classe 'Sprite'"""
        super().__init__(name)
        self.image = self.get_image(32, 0)
        # enlève le noir du sprite au profit du transparent
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width*0.5, 8)
        self.old_position = self.position.copy()
        self.is_running = False

    def save_location(self):
        """mémorise la position du joueur"""
        self.old_position = self.position.copy()

    def move_right(self):
        """Déplace le joueur à droite"""
        animation = 'sprint_right' if self.is_running else 'right'
        self.change_animation(f"{animation}")
        self.position[0] += self.speed

    def move_left(self):
        """Déplace le joueur à gauche"""
        animation = 'sprint_left' if self.is_running else 'left'
        self.change_animation(f"{animation}")
        self.position[0] -= self.speed

    def move_up(self):
        """Déplace le joueur en haut"""
        animation = 'sprint_up' if self.is_running else 'up'
        self.change_animation(f"{animation}")
        self.position[1] -= self.speed

    def move_down(self):
        """Déplace le joueur en bas"""
        animation = 'sprint_down' if self.is_running else 'down'
        self.change_animation(f"{animation}")
        self.position[1] += self.speed

    def move_right_down(self):
        """Déplace le joueur en bas à droite"""
        animation = 'sprint_right' if self.is_running else 'right'
        self.change_animation(f"{animation}")
        self.position[0] += self.speed-1
        self.position[1] += self.speed-1

    def move_left_down(self):
        """Déplace le joueur en bas à gauche"""
        animation = 'sprint_left' if self.is_running else 'left'
        self.change_animation(f"{animation}")
        self.position[0] -= self.speed-1
        self.position[1] += self.speed-1

    def move_right_up(self):
        """Déplace le joueur en haut à droite"""
        animation = 'sprint_up' if self.is_running else 'up'
        self.change_animation(f"{animation}")
        self.position[0] += self.speed-1
        self.position[1] -= self.speed-1

    def move_left_up(self):
        """Déplace le joueur en haut à gauche"""
        animation = 'sprint_up' if self.is_running else 'up'
        self.change_animation(f"{animation}")
        self.position[0] -= self.speed-1
        self.position[1] -= self.speed-1

    def attack(self):
        """Déclenche une attaque"""
        self.change_animation("attack")

    def update(self):
        """Met à jour la position du joueur"""
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        """Replace le joueur à la position antérieure à une collision"""
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class Player(Entity):
    """Classe d'un joueur héritant de la Classe Entity"""

    def __init__(self):
        super().__init__("bob", 0, 0)


class NPC(Entity):
    """Classe des PNJ héritant de la Classe Entity"""

    def __init__(self, name, nb_points):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.points = []
        self.name = name
        self.speed = 1
        self.speed = 1
        self.current_point = 0

    def move(self):
        """Déplace le PNJ"""
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point == self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self):
        """Place le PNJ à son point d'apparition"""
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        """Charge les points de passage du PNJ"""
        for num in range(1, self.nb_points+1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
