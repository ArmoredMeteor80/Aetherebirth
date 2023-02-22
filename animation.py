import pygame
import random


class AnimateSprite(pygame.sprite.Sprite):
    """Classe qui anime les sprites"""
    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"assets/sprites/sprite_sheet_{name}.png").convert_alpha()
        if name == "bob":
            # dictionnaire contenant pour chaque clé un tuple composé d'une liste d'images
            # et d'un entier correspondant à une orientation
            self.images = {
                "down": (self.get_images(0, 1, 5), 0),
                "up": (self.get_images(32, 1, 5), 1),
                "right": (self.get_images(64, 1, 5), 2),
                "left": (self.get_images(96, 1, 5), 3),
                "still": (self.get_images(0, 0, 1), 0),
                "sprint_down": (self.get_images(0, 6, 9), 0),
                "sprint_up": (self.get_images(32, 6, 9), 1),
                "sprint_right": (self.get_images(64, 6, 9), 2),
                "sprint_left": (self.get_images(96, 6, 9), 3),
                "attack": (self.get_images(128, 0, 11), 0)
            }
        else:
            self.images = {
                "down": (self.get_images(0, 0, 0), 0),
                "up": (self.get_images(32, 0, 0), 1),
                "right": (self.get_images(64, 0, 0), 2),
                "left": (self.get_images(96, 0, 0), 3),
                "still": (self.get_images(0, 0, 1), 0)
            }
        self.animation_index = 0
        self.attack_animation_index = 0
        self.clock = 0
        self.attack_clock = 0
        self.speed = 1

    def change_animation(self, name):
        """Change l'animation en fonction d'un nom d'animation"""
        if name == 'attack':
            if self.attack_animation_index >= len(self.images[name][0]):
                self.attack_animation_index = 0
            self.image = self.images[name][0][self.attack_animation_index]
            self.attack_clock += 20
            if self.attack_clock >= 100:
                # On passe à l'image suivante
                self.attack_animation_index += 1
                self.attack_clock = 0
        else:
            if name == 'still' and self.animation_index == 1:
                self.speed = random.randint(1, 10)/50
                self.attack_animation_index = 0

            if self.animation_index >= len(self.images[name][0]):
                self.animation_index = 0
            self.image = self.images[name][0][self.animation_index]
            self.clock += self.speed * 6

            # On cadence l'animation
            if self.clock >= 100:
                # On passe à l'image suivante
                self.animation_index += 1
                self.clock = 0
            if name != 'still':
                self.images['still'] = (self.get_images(self.images[name][1] * 32, 0, 1), 0)
                self.images['attack'] = (self.get_images(self.images[name][1]*32 + 128, 0, 11), 0)

    def get_images(self, y, start, end):
        """Renvoie une liste d'images"""
        images = []
        for i in range(start, end+1):
            x = i * 32
            image = self.get_image(x, y)
            images.append(image)
        return images

    def get_image(self, x, y):
        """Renvoie les coordonnées x, y du sprite sheet de l'entité """
        # Création d'une surface de 32 par 32 pixels
        image = pygame.Surface([32, 32], pygame.SRCALPHA)
        # On récupère le sprite du sprite sheet
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
