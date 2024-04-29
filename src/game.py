import os
import sys
import pygame

from .networking import Network, NetworkEntityManager

from .save import SaveLoadSystem
from .map import MapManager
from .entity import Player
from .ui import UI
from .ui.dialog import DialogBox

NETWORK_SEND_DELAY = 6#frames between data send

class Game:
    """Représentation du concept du jeu"""

    def __init__(self, size, is_starting_menu_over):
        """Constructeur"""
        # Création de la fenêtre de jeu
        self.network = Network()
        self.network.start()

        self.screen = pygame.display.set_mode(size, pygame.SCALED | pygame.FULLSCREEN | pygame.HIDDEN, vsync=1)
        if is_starting_menu_over:
            # Création d'un objet "SaveLoadSystem" gérant le système de sauvegarde et de chargement
            self.saveloadmanager = SaveLoadSystem(".save", "save_data")
            # Chargement des données sauvegardées
            player_position, current_map, controls_shown, player_health = self.saveloadmanager.load_game_data(
                ["player_position", "current_map", "controls_shown", "player_health"],
                [(1568, 352), "clairiere_map", True, 100])

            # Génération d'un joueur
            self.player = Player(player_position)
            self.map_manager = MapManager(self.screen, self.player, current_map)
            self.dialog_box = DialogBox()
            self.controls_shown = controls_shown
            self.ui = UI()
            
            self.network_entities_manager = NetworkEntityManager(self.map_manager)
            self.network_players = self.network.getPlayers()

            self.last_network_send = 0

        # Dictionnaire contenant les sons du jeu
        self.sounds = {'click_sound_effect': pygame.mixer.Sound('assets/sounds/click_sound_effect.wav'),
                       'click_error_sound_effect': pygame.mixer.Sound('assets/sounds/click_error_sound_effect.wav'),
                       'punch_sound_effect': pygame.mixer.Sound('assets/sounds/punch_sound_effect.wav'),
                       'exhausted_sound_effect': pygame.mixer.Sound('assets/sounds/exhausted_sound_effect.wav')}

        # Change le titre de la fenêtre
        pygame.display.set_caption("Pyb0b")
        self.running = True
        self.is_starting_menu_over = is_starting_menu_over

    def send_network_data(self):
        return self.network.sendData(self.player, self.map_manager)

    def update_network(self, dt: int):
        self.last_network_send += dt
        if self.last_network_send >= NETWORK_SEND_DELAY:
            reply = self.send_network_data()
            #print(reply)
            self.last_network_send = 0
            if ("changed" in reply) and (reply['changed']==False):
                pass
            else:
                if "players" in reply:
                    print(reply)
                    self.network_entities_manager.updatePlayers(reply["players"])
                print(reply)

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

        # Attaque du joueur
        if self.player.is_attacking:
            self.player.attack()

        elif self.player.old_position == self.player.position and self.player.is_attacking is False:
            self.player.change_animation('still')
            self.player.attack_cooldown = 0

        # Régénération passive du joueur
        self.player.health_regen(1 / 180)
        # Course du joueur
        if pressed[pygame.K_LSHIFT] and not self.player.is_exhausted[0]:
            self.player.is_running = True
            self.player.speed = 3
            if self.player.stamina <= 1:
                self.player.is_exhausted[0] = True
                self.play_sound('exhausted_sound_effect')
            if self.player.position == self.player.old_position:
                # Régénération passive de vie et d'endurance
                self.player.stamina_regen(0.2)
            else:
                self.player.stamina_depletion(0.2)
        else:
            self.player.is_running = False
            self.player.speed = 2
            # Régénération passive de vie et d'endurance
            self.player.stamina_regen(0.2)
            self.player.check_exhaustion()

    def update(self):
        """Actualise le groupe"""
        self.map_manager.update(self.player)

    def shutting_down(self):
        """Ferme et sauvegarde les données du jeu"""
        if self.is_starting_menu_over:
            # Sauvegarde toutes les données du jeu que l'on veut récupérer lors du prochain chargement
            self.saveloadmanager.save_game_data(
                [self.player.position, self.map_manager.current_map, self.controls_shown, self.player.health],
                ["player_position", "current_map", "controls_shown", "player_health"])
        pygame.mixer.music.fadeout(1500)
        self.fade_in((0, 0, 0), 2)
        self.running = False
        # Déinitialise tous les modules pygame
        pygame.quit()
        sys.exit()

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
            # Fondu inverse, on met d'abord à jour le joueur qui se met sur la nouvelle carte chargée, puis
            # on dessine deux fois de sorte à afficher la carte derrière le fondu et centrer la caméra sur le joueur
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

    def play_sound(self, sound_name, volume=1):
        """Joue le son passé en paramètre"""
        if sound_name in self.sounds:
            pygame.mixer.Sound.play(self.sounds[sound_name]).set_volume(volume)

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
            background = pygame.image.load('assets/ressources/background.png').convert()
            logo = pygame.image.load('assets/ressources/logo_pybob.png').convert_alpha()
            logo = pygame.transform.scale(logo, (800, 400))

            # On charge la musique de fond puis on la joue, par la même on charge un son de clic
            pygame.mixer.music.load('assets/sounds/bg_music.ogg')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

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
                            self.play_sound('click_sound_effect')
                            return "new_game"
                        elif continue_button_rect.collidepoint(event.pos):
                            if len(os.listdir("save_data")) != 0:
                                self.play_sound('click_sound_effect')
                                return "continue"
                            else:
                                self.play_sound('click_error_sound_effect', 0.8)
                        elif quit_button_rect.collidepoint(event.pos):
                            self.play_sound('click_sound_effect')
                            return "quit"

                # On dessine les boutons
                pygame.draw.rect(self.screen, (61, 34, 20), new_game_button_rect)
                if not os.path.exists("save_data"):
                    os.makedirs("save_data")
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

        # Avant la boucle, on charge les images nécessaires
        box = pygame.image.load('assets/dialogs/dialog_box.png').convert_alpha()
        box = pygame.transform.scale(box, (330, 182))

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
            # Affiche l'interface utilisateur
            self.ui.display(self.player)
            # Affiche les boites de dialogue
            self.dialog_box.render(self.screen)
            # Met fin aux boites de dialogues ouvertes si le joueur s'éloigne de la source
            self.map_manager.terminate_dialog(self.dialog_box)

            # Affiche les contôles dans le coin supérieur gauche
            if self.controls_shown:
                self.screen.blit(box, (1590, 10))
                text_list, pos_list = ["Déplacements : Z, Q, S, D", "Sprint : Shift", "Interactions : E",
                                       "Combat : Clic Gauche", "Masquer commandes : P", "Fermer Jeu : Echap"], \
                                      [(1620, 21), (1620, 46), (1620, 71), (1620, 96), (1620, 121), (1620, 146)]
                self.draw_text(text_list, pos_list, size=20)

            # Actualisation de la fenêtre
            pygame.display.flip()

            for event in pygame.event.get():
                # Stoppe la boucle de jeu lorsque la fenêtre est fermée
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.shutting_down()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    exhausted_sound_played = True
                    if not (self.player.is_attacking or self.player.is_exhausted[0]):
                        self.play_sound('punch_sound_effect')
                        self.player.stamina_depletion(25, False)
                        self.player.is_attacking = True
                        exhausted_sound_played = False
                        self.player.check_exhaustion()
                    if exhausted_sound_played is False and self.player.is_exhausted[0]:
                        self.play_sound('exhausted_sound_effect')
                        # On désactive l'animation d'épuisement si le joueur attaque en se déplaçant
                        if self.player.position != self.player.old_position:
                            self.player.is_exhausted[1] = 20
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if self.controls_shown:
                            self.controls_shown = False
                        else:
                            self.controls_shown = True
                    if event.key == pygame.K_e:
                        self.map_manager.check_dialog_collisions(self.dialog_box)

            # Si le joueur décède
            if self.player.health <= 0:
                self.player.health = 100
                self.shutting_down()

            # Animation de démarrage du jeu
            if not is_booted:
                self.booting_animation()
            is_booted = True

            # Cadence le taux de rafraîchissement de la fenêtre à 60 ips
            dt = clock.tick(60)
            
            self.update_network(dt)
