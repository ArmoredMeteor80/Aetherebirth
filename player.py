import pygame


# La classe "Player" hérite de la classe parente "Sprite" de pygame.sprite
class Player(pygame.sprite.Sprite):
    """Classe du joueur"""

    def __init__(self, x, y):
        """Constructeur qui initialise la Classe 'Sprite'"""
        super().__init__()
        self.sprite_sheet = pygame.image.load("assets/sprites/player/sprite_sheet_lutin_1.png")
        self.image = self.get_image(0, 0)
        # enlève le noir du sprite au profit du transparent
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.images = {
            "down": self.get_image(0, 0),
            "left": self.get_image(0, 40),
            "right": self.get_image(0, 80),
            "up": self.get_image(0, 120)
        }
        self.speed = 2

    def change_animation(self, name):
        """Change l'animation en fonction d'un nom d'animation"""
        self.image = self.images[name]
        self.image.set_colorkey((0, 0, 0))

    def move_right(self):
        """Déplace le joueur à droite"""
        self.position[0] += self.speed

    def move_left(self):
        """Déplace le joueur à gauche"""
        self.position[0] -= self.speed

    def move_up(self):
        """Déplace le joueur en haut"""
        self.position[1] -= self.speed

    def move_down(self):
        """Déplace le joueur en bas"""
        self.position[1] += self.speed

    def move_right_down(self):
        """Déplace le joueur en bas à droite"""
        self.position[0] += self.speed/1.25
        self.position[1] += self.speed/1.25

    def move_left_down(self):
        """Déplace le joueur en bas à gauche"""
        self.position[0] -= self.speed/1.25
        self.position[1] += self.speed/1.25

    def move_right_up(self):
        """Déplace le joueur en haut à droite"""
        self.position[0] += self.speed/1.25
        self.position[1] -= self.speed/1.25

    def move_left_up(self):
        """Déplace le joueur en haut à gauche"""
        self.position[0] -= self.speed/1.25
        self.position[1] -= self.speed/1.25

    def update(self):
        """Met à jour la position du joueur"""
        self.rect.topleft = self.position

    def get_image(self, x, y):
        """Renvoie les coordonnées x, y du sprite sheet du joueur """
        # Création d'une surface de 32 par 40 pixels
        image = pygame.Surface([32, 40])
        # On récupère uniquement le premier sprite du sprite sheet
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 40))
        return image
