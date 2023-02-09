import pygame
import pytmx
import pyscroll

from map import MapManager
from player import Player


class Game:
    """Représentation du concept du jeu"""
    def __init__(self, size):
        """Constructeur"""
        # Création de la fenêtre de jeu
        self.screen = pygame.display.set_mode(size, pygame.SCALED | pygame.HIDDEN, vsync=1)
        # Change le titre de la fenêtre
        pygame.display.set_caption("Pyb0b")
        # Génération d'un joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)

    def handle_imput(self):
        """Permet la gestion de toutes les entrées"""
        # Récupération des touches actionnées
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_s] and pressed[pygame.K_d] or pressed[pygame.K_DOWN] and pressed[pygame.K_RIGHT]:
            self.player.move_right_down()
        elif pressed[pygame.K_s] and pressed[pygame.K_q] or pressed[pygame.K_DOWN] and pressed[pygame.K_LEFT]:
            self.player.move_left_down()
        elif pressed[pygame.K_z] and pressed[pygame.K_d] or pressed[pygame.K_UP] and pressed[pygame.K_RIGHT]:
            self.player.move_right_up()
        elif pressed[pygame.K_z] and pressed[pygame.K_q] or pressed[pygame.K_UP] and pressed[pygame.K_LEFT]:
            self.player.move_left_up()
        elif pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.player.move_right()
        elif pressed[pygame.K_z] or pressed[pygame.K_UP]:
            self.player.move_up()
        if pressed[pygame.K_LSHIFT]:
            self.player.speed = 3
        else:
            self.player.speed = 2

    def update(self):
        """Actualise le groupe"""
        self.map_manager.update()

    def booting_animation(self):
        """Animation de fondu lors du démarrage"""
        # On rend visible la fenêtre de jeu
        pygame.display.set_mode(self.screen.get_size(), pygame.SCALED | pygame.SHOWN, vsync=1)
        self.map_manager.draw()
        self.map_manager.fade_out((255, 255, 255), 5)

    def run(self):
        """Boucle du jeu"""
        # Création d'un objet "Clock" permettant de gérer le temps
        clock = pygame.time.Clock()
        running = True
        is_booted = False

        while running:

            # On mémorise la position du joueur
            self.player.save_location()
            # On gère toutes les entrées
            self.handle_imput()
            # Actualisation du groupe
            self.update()
            # On centre la caméra sur le joueur et affichage des calques sur la fenêtre d'affichage
            self.map_manager.draw()
            # Actualisation de la fenêtre
            pygame.display.flip()

            for event in pygame.event.get():
                # Stoppe la boucle de jeu lorsque la fenêtre est fermée
                if event.type == pygame.QUIT:
                    self.map_manager.fade_in((0, 0, 0), 2)
                    running = False

            # Animation de démarrage
            if not is_booted:
                self.booting_animation()
            is_booted = True

            # Cadence le taux de rafraîchissement de la fenêtre à 60 ips
            clock.tick(60)

        # Déinitialise tous les modules pygame
        pygame.quit()
