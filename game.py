import pygame
import pytmx
import pyscroll

from dialog import DialogBox
from map import MapManager
from player import Player
from save_load_manager import SaveLoadSystem

# Création d'un objet "SaveLoadSystem" gérant le système de sauvegarde et de chargement
saveloadmanager = SaveLoadSystem(".save", "save_data")
player_position, current_map = saveloadmanager.load_game_data(["player_position", "current_map"], [(1568, 352), "clairiere_map"])


class Game:
    """Représentation du concept du jeu"""

    def __init__(self, size):
        """Constructeur"""
        # Création de la fenêtre de jeu
        self.screen = pygame.display.set_mode(size, pygame.SCALED | pygame.HIDDEN, vsync=1)
        # Change le titre de la fenêtre
        pygame.display.set_caption("Pyb0b")
        # Génération d'un joueur
        self.player = Player(player_position)
        self.map_manager = MapManager(self.screen, self.player, current_map)
        self.dialog_box = DialogBox()

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

        if self.player.is_attacking:
            self.player.attack()
        elif self.player.old_position[0] - self.player.position[0] == 0 \
                and self.player.old_position[1] - self.player.position[1] == 0 \
                and self.player.is_attacking is False:
            self.player.change_animation('still')
            self.player.attack_cooldown = 0

        if pressed[pygame.K_LSHIFT]:
            self.player.is_running = True
            self.player.speed = 3
        else:
            self.player.is_running = False
            self.player.speed = 2

    def update(self):
        """Actualise le groupe"""
        self.map_manager.update()

    def booting_animation(self):
        """Animation de fondu lors du démarrage"""
        # On rend visible la fenêtre de jeu
        pygame.display.set_mode(self.screen.get_size(), pygame.SCALED | pygame.SHOWN | pygame.FULLSCREEN, vsync=1)
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
            # Affiche les boites de dialogue
            self.dialog_box.render(self.screen)
            # Met fin aux boites de dialogues ouvertes si le joueur s'éloigne de la source
            self.map_manager.terminate_dialog(self.dialog_box)
            # Actualisation de la fenêtre
            pygame.display.flip()

            for event in pygame.event.get():
                # Stoppe la boucle de jeu lorsque la fenêtre est fermée
                if event.type == pygame.QUIT:
                    saveloadmanager.save_game_data([self.player.position, self.map_manager.current_map], ["player_position", "current_map"])
                    self.map_manager.fade_in((0, 0, 0), 2)
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.player.is_attacking = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.map_manager.check_dialog_collisions(self.dialog_box)

            # Animation de démarrage
            if not is_booted:
                self.booting_animation()
            is_booted = True

            # Cadence le taux de rafraîchissement de la fenêtre à 60 ips
            clock.tick(60)

        # Déinitialise tous les modules pygame
        pygame.quit()
