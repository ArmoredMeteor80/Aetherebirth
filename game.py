import os
import pygame


from dialog import DialogBox
from map import MapManager
from player import Player
from save_load_manager import SaveLoadSystem


class Game:
    """Représentation du concept du jeu"""

    def __init__(self, size, is_starting_menu_over):
        """Constructeur"""
        # Création de la fenêtre de jeu
        self.screen = pygame.display.set_mode(size, pygame.SCALED | pygame.FULLSCREEN | pygame.HIDDEN, vsync=1)
        if is_starting_menu_over:
            # Création d'un objet "SaveLoadSystem" gérant le système de sauvegarde et de chargement
            self.saveloadmanager = SaveLoadSystem(".save", "save_data")
            # Chargement des données sauvegardées
            player_position, current_map, controls_shown = self.saveloadmanager.load_game_data(
                ["player_position", "current_map", "controls_shown"],
                [(1568, 352), "clairiere_map", True])

            # Génération d'un joueur
            self.player = Player(player_position)
            self.map_manager = MapManager(self.screen, self.player, current_map)
            self.dialog_box = DialogBox()
            self.controls_shown = controls_shown

        # Change le titre de la fenêtre
        pygame.display.set_caption("Pyb0b")
        self.running = True
        self.is_starting_menu_over = is_starting_menu_over

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

    def shutting_down(self):
        """Ferme et sauvegarde les données du jeu"""
        if self.is_starting_menu_over:
            # Sauvegarde toutes les données du jeu que l'on veut récupérer lors du prochain chargement
            self.saveloadmanager.save_game_data(
                [self.player.position, self.map_manager.current_map, self.controls_shown],
                ["player_position", "current_map", "controls_shown"])
        self.fade_in((0, 0, 0), 2)
        self.running = False

    def fade_in(self, color, speed):
        """Filtre de fondu"""
        # on fait une copie de l'écran
        screen_image = self.screen.copy()
        # Surface qui va faire le fondu en augmentant et baissant sa valeur d'alpha
        fade = pygame.Surface(self.screen.get_size()).convert_alpha()
        fade.fill(color)
        for alpha in range(0, 256, speed):
            self.screen.blit(screen_image, (0, 0))
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()

    def fade_out(self, color, speed):
        """Filtre de fondu inverse"""
        fade = pygame.Surface(self.screen.get_size()).convert_alpha()
        fade.fill(color)
        if self.is_starting_menu_over:
            # Fondu inverse, on met d'abord à jour le joueur qui se met sur la nouvelle carte chargée,
            # puis on draw deux fois de sorte à afficher la carte derrière le fondu et centrer la caméra sur le joueur
            self.map_manager.player.update()
            self.map_manager.draw()
            self.map_manager.draw()
        # Enfin on fait une copie de ce qu'il y a derriere le fondu (on exclut le fondu de la copie)
        fade_rect = fade.get_rect()
        self.screen.set_clip(fade_rect)
        screen_image = self.screen.copy()
        self.screen.set_clip(None)
        for alpha in range(255, -1, -speed):
            self.screen.blit(screen_image, (0, 0))
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()

    def booting_animation(self):
        """Animation de fondu lors du démarrage"""
        # On rend visible la fenêtre de jeu
        if self.is_starting_menu_over:
            pygame.display.set_mode(self.screen.get_size(), pygame.SCALED | pygame.FULLSCREEN | pygame.SHOWN, vsync=1)
            self.map_manager.draw()
            self.map_manager.fade_out((255, 255, 255), 5)
        else:
            self.fade_out((255, 255, 255), 5)

    def draw_text(self, text_list, pos_list, size=36, text_color=(255, 255, 255)):
        """Dessine une liste de textes à leurs positions respectives sur l'écran"""
        font = pygame.font.Font('assets/dialogs/dialog_font.ttf', size)
        for i in range(len(text_list)):
            img = font.render(text_list[i], False, text_color)
            self.screen.blit(img, pos_list[i])

    def run(self):
        """Boucle du jeu"""
        # Création d'un objet "Clock" permettant de gérer le temps
        clock = pygame.time.Clock()
        is_booted = False

        if not self.is_starting_menu_over:
            # On crée les boutons
            new_game_button_rect = pygame.Rect(1300, 450, 400, 100)
            continue_button_rect = pygame.Rect(1300, 600, 400, 100)
            quit_button_rect = pygame.Rect(1300, 750, 400, 100)

            # On charge l'image de fond du menu ainsi que le logo du jeu
            background = pygame.image.load("assets/ressources/background.png").convert()
            logo = pygame.image.load("assets/ressources/logo_pybob.png").convert_alpha()
            logo = pygame.transform.scale(logo, (800, 400))

            screen = pygame.display.set_mode(self.screen.get_size(), pygame.SCALED | pygame.FULLSCREEN | pygame.SHOWN,
                                             vsync=1)
            # Boucle du menu de démarrage
            while self.running:
                screen.blit(background, (0, 0))
                screen.blit(logo, (1050, 20))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        self.shutting_down()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if new_game_button_rect.collidepoint(event.pos):
                            return "new_game"
                        elif continue_button_rect.collidepoint(event.pos) and len(os.listdir("save_data")) != 0:
                            return "continue"
                        elif quit_button_rect.collidepoint(event.pos):
                            return "quit"

                # On dessine les boutons
                pygame.draw.rect(self.screen, (61, 34, 20), new_game_button_rect)
                # S'il n'y a pas de fichiers de sauvegarde, le bouton "continue" est grisé et inopérant
                if len(os.listdir("save_data")) == 0:
                    pygame.draw.rect(self.screen, (109, 82, 81), continue_button_rect)
                else:
                    pygame.draw.rect(self.screen, (61, 34, 20), continue_button_rect)
                pygame.draw.rect(self.screen, (61, 34, 20), quit_button_rect)

                text_list, pos_list = ["Nouvelle partie", "Continuer", "Quitter"], [(1310, 460), (1377, 610),
                                                                                    (1415, 760)]
                # On affiche le texte des boutons
                self.draw_text(text_list, pos_list, size=50)

                # On affiche le nom des incroyables développeurs de ce jeu
                text_list2, pos_list2 = ["By Mathieu Tuloup and Thomas Levadoux"], [(1200, 1020)]
                self.draw_text(text_list2, pos_list2, size=25)

                # Animation de démarrage du menu
                if not is_booted:
                    self.booting_animation()
                is_booted = True

                # On change la couleur des boutons quand on passe la souris dessus
                mx, my = pygame.mouse.get_pos()
                if new_game_button_rect.collidepoint((mx, my)):
                    pygame.draw.rect(self.screen, (114, 117, 27), new_game_button_rect)
                    self.draw_text(text_list, pos_list, size=50)
                if continue_button_rect.collidepoint((mx, my)):
                    if len(os.listdir("save_data")) == 0:
                        pygame.draw.rect(self.screen, (117, 32, 27), continue_button_rect)
                    else:
                        pygame.draw.rect(self.screen, (114, 117, 27), continue_button_rect)
                    self.draw_text(text_list, pos_list, size=50)
                if quit_button_rect.collidepoint((mx, my)):
                    pygame.draw.rect(self.screen, (114, 117, 27), quit_button_rect)
                    self.draw_text(text_list, pos_list, size=50)

                # Cadence le taux de rafraîchissement de la fenêtre à 60 ips
                clock.tick(60)
                # On met à jour la fenêtre
                pygame.display.flip()

        # Boucle du jeu
        while self.running:

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
            # Affiche les contôles dans le coin supérieur gauche
            if self.controls_shown:
                box = pygame.image.load('assets/dialogs/dialog_box.png').convert_alpha()
                box = pygame.transform.scale(box, (330, 182))
                self.screen.blit(box, (0, 4))
                text_list, pos_list = ["Déplacements : Z, Q, S, D", "Sprint : Shift", "Interactions : E",
                                       "Combat : Clic Gauche", "Masquer commandes : P", "Fermer Jeu : Echap"], \
                                      [(35, 15), (35, 40), (35, 65), (35, 90), (35, 115), (35, 140)]
                self.draw_text(text_list, pos_list, size=20)
            # Actualisation de la fenêtre
            pygame.display.flip()

            for event in pygame.event.get():
                # Stoppe la boucle de jeu lorsque la fenêtre est fermée
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.shutting_down()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.player.is_attacking = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if self.controls_shown:
                            self.controls_shown = False
                        else:
                            self.controls_shown = True
                    if event.key == pygame.K_e:
                        self.map_manager.check_dialog_collisions(self.dialog_box)

            # Animation de démarrage du jeu
            if not is_booted:
                self.booting_animation()
            is_booted = True

            # Cadence le taux de rafraîchissement de la fenêtre à 60 ips
            clock.tick(60)

        # Déinitialise tous les modules pygame
        pygame.quit()

