import pygame
import random


# La classe "Player" hérite de la classe parente "Sprite" de pygame.sprite
class Entity(pygame.sprite.Sprite):
    """Classe d'une entité"""

    def __init__(self, name, x, y):
        """Constructeur qui initialise la Classe 'Sprite'"""
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"assets/sprites/sprite_sheet_{name}.png").convert_alpha()
        self.image = self.get_image(0, 0)
        # enlève le noir du sprite au profit du transparent
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.images = {
            "down": self.get_image(0, 0),
            "left": self.get_image(0, 96),
            "right": self.get_image(0, 64),
            "up": self.get_image(0, 32)
        }
        self.feet = pygame.Rect(0, 0, self.rect.width*0.5, 8)
        self.old_position = self.position.copy()
        self.speed = 2

    def save_location(self):
        """mémorise la position du joueur"""
        self.old_position = self.position.copy()

    def change_animation(self, name):
        """Change l'animation en fonction d'un nom d'animation"""
        self.image = self.images[name]
        self.image.set_colorkey((0, 0, 0))

    def move_right(self):
        """Déplace le joueur à droite"""
        self.change_animation('right')
        self.position[0] += self.speed

    def move_left(self):
        """Déplace le joueur à gauche"""
        self.change_animation('left')
        self.position[0] -= self.speed

    def move_up(self):
        """Déplace le joueur en haut"""
        self.change_animation('up')
        self.position[1] -= self.speed

    def move_down(self):
        """Déplace le joueur en bas"""
        self.change_animation('down')
        self.position[1] += self.speed

    def move_right_down(self):
        """Déplace le joueur en bas à droite"""
        self.position[0] += self.speed-1
        self.position[1] += self.speed-1

    def move_left_down(self):
        """Déplace le joueur en bas à gauche"""
        self.position[0] -= self.speed-1
        self.position[1] += self.speed-1

    def move_right_up(self):
        """Déplace le joueur en haut à droite"""
        self.position[0] += self.speed-1
        self.position[1] -= self.speed-1

    def move_left_up(self):
        """Déplace le joueur en haut à gauche"""
        self.position[0] -= self.speed-1
        self.position[1] -= self.speed-1

    def update(self):
        """Met à jour la position du joueur"""
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        """Replace le joueur à la position antérieure à une collision"""
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        """Renvoie les coordonnées x, y du sprite sheet du joueur """
        # Création d'une surface de 32 par 40 pixels
        image = pygame.Surface([32, 32], pygame.SRCALPHA)
        # On récupère uniquement le premier sprite du sprite sheet
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image


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
