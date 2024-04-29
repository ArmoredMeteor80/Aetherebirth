import pygame
import random


# La classe "AnimateSprite" hérite de la classe parente "Sprite" de pygame.sprite
class AnimateSprite(pygame.sprite.Sprite):
    """Classe qui anime les sprites"""
    def __init__(self, name: str):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"assets/sprites/sprite_sheet_{name}.png",).convert_alpha()
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
                "exhausted_down": (self.get_images(0, 10, 13), 0),
                "exhausted_up": (self.get_images(32, 10, 13), 1),
                "exhausted_right": (self.get_images(64, 10, 13), 2),
                "exhausted_left": (self.get_images(96, 10, 13), 3),
                "attack": (self.get_images(128, 0, 11), 0)
            }
        elif "cat" in name or "cottain" in name:
            self.images = {
                "down": (self.get_images(0, 0, 2), 0),
                "up": (self.get_images(32, 0, 2), 1),
                "right": (self.get_images(64, 0, 2), 2),
                "left": (self.get_images(96, 0, 2), 3),
                "still_npc_down": (self.get_images(0, 0, 0), 0),
                "still_npc_up": (self.get_images(32, 0, 0), 1),
                "still_npc_right": (self.get_images(64, 0, 0), 2),
                "still_npc_left": (self.get_images(96, 0, 0), 3)
            }
        elif "chicken" in name:
            self.images = {
                "down": (self.get_images(0, 6, 9, 16), 0),
                "up": (self.get_images(16, 6, 9, 16), 1),
                "right": (self.get_images(32, 6, 9, 16), 2),
                "left": (self.get_images(48, 6, 9, 16), 3),
                "still_npc_down": (self.get_images(0, 0, 5, 16), 0),
                "still_npc_up": (self.get_images(16, 0, 5, 16), 1),
                "still_npc_right": (self.get_images(32, 0, 5, 16), 2),
                "still_npc_left": (self.get_images(48, 0, 5, 16), 3)
            }
        elif "dark_mage" in name:
            self.images = {
                "down": (self.get_images(0, 0, 3), 0),
                "up": (self.get_images(32, 0, 3), 1),
                "right": (self.get_images(64, 0, 3), 2),
                "left": (self.get_images(96, 0, 3), 3),
                "still_npc_down": (self.get_images(0, 0, 3), 0),
                "still_npc_up": (self.get_images(32, 0, 3), 1),
                "still_npc_right": (self.get_images(64, 0, 3), 2),
                "still_npc_left": (self.get_images(96, 0, 3), 3)
            }
        elif "skeleton" in name:
            self.images = {
                "down": (self.get_images(0, 4, 7), 0),
                "up": (self.get_images(32, 4, 7), 1),
                "right": (self.get_images(64, 4, 7), 2),
                "left": (self.get_images(96, 4, 7), 3),
                "still_npc_down": (self.get_images(0, 0, 3), 0),
                "still_npc_up": (self.get_images(32, 0, 3), 1),
                "still_npc_right": (self.get_images(64, 0, 3), 2),
                "still_npc_left": (self.get_images(96, 0, 3), 3)
            }
        elif "lutin" in name:
            self.images = {
                "down": (self.get_images(0, 0, 3), 0),
                "up": (self.get_images(32, 0, 3), 1),
                "right": (self.get_images(64, 0, 3), 2),
                "left": (self.get_images(96, 0, 3), 3),
                "still_npc_down": (self.get_images(0, 1, 1), 0),
                "still_npc_up": (self.get_images(32, 1, 1), 1),
                "still_npc_right": (self.get_images(64, 1, 1), 2),
                "still_npc_left": (self.get_images(96, 1, 1), 3)
            }
        else:
            self.images = {
                "down": (self.get_images(0, 0, 0), 0),
                "up": (self.get_images(32, 0, 0), 1),
                "right": (self.get_images(64, 0, 0), 2),
                "left": (self.get_images(96, 0, 0), 3),
                "still_npc_down": (self.get_images(0, 0, 0), 0),
                "still_npc_up": (self.get_images(32, 0, 0), 1),
                "still_npc_right": (self.get_images(64, 0, 0), 2),
                "still_npc_left": (self.get_images(96, 0, 0), 3)
            }
        self.animation_index = 0
        self.attack_animation_index = 0
        self.exhaust_animation_index = 0
        self.clock = 0
        if name == "bob":
            self.clock_speed = 6
        else:
            self.clock_speed = 10
        self.attack_clock = 0
        self.exhaust_clock = 0
        # Horloge permettant de cadencer le temps durant lequel on peut continuer un combo
        self.attack_clock_combo_extender = 0
        self.speed = 1

    def change_animation(self, name: str):
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
                self.attack_clock_combo_extender = 0
        else:
            self.attack_clock_combo_extender += 1
            if self.attack_clock_combo_extender >= 40:
                self.attack_animation_index = 0
                self.attack_clock_combo_extender = 0

            if "exhausted" in name:
                if self.exhaust_animation_index >= len(self.images[name][0]):
                    self.exhaust_animation_index = 0
                self.image = self.images[name][0][self.exhaust_animation_index]
                self.exhaust_clock += 20
                if self.exhaust_clock >= 100:
                    # On passe à l'image suivante
                    self.exhaust_animation_index += 1
                    self.exhaust_clock = 0
            else:
                if name == 'still' and self.animation_index == 1:
                    self.speed = random.randint(1, 10)/50

                if self.animation_index >= len(self.images[name][0]):
                    self.animation_index = 0
                self.image = self.images[name][0][self.animation_index]

                # On évite que l'animation soit trop lente
                if self.speed < 1 and name != 'still':
                    self.clock += self.clock_speed
                else:
                    self.clock += self.speed * self.clock_speed

                # On cadence l'animation
                if self.clock >= 100:
                    # On passe à l'image suivante
                    self.animation_index += 1
                    self.clock = 0

                if name != 'still':
                    self.images['still'] = (self.get_images(self.images[name][1] * 32, 0, 1), 0)
                    self.images['attack'] = (self.get_images(self.images[name][1]*32 + 128, 0, 11), 0)

    def get_images(self, y: int, start: int, end: int, size: int = 32):
        """Renvoie une liste d'images"""
        images = []
        for i in range(start, end+1):
            x = i * size
            image = self.get_image(x, y, size)
            images.append(image)
        return images

    def get_image(self, x: int, y: int, size: int = 32):
        """Renvoie les coordonnées x, y du sprite sheet de l'entité """
        # Création d'une surface de taille size par size
        image = pygame.Surface([size, size], pygame.SRCALPHA)
        # On récupère le sprite du sprite sheet
        image.blit(self.sprite_sheet, (0, 0), (x, y, size, size))
        return image
