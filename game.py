import pygame
import pytmx
import pyscroll
from player import Player


class Game:
    """Représentation du concept du jeu"""
    def __init__(self):
        """Constructeur"""
        # Création de la fenêtre de
        self.screen = pygame.display.set_mode((1280, 720))
        # Change le titre de la fenêtre
        pygame.display.set_caption("Pyb0b")

        # Charge la carte tmx en créant un objet "TiledMap" contenant les calques, objets et images d'une carte .tmx
        tmx_data = pytmx.util_pygame.load_pygame("assets/maps/test_map.tmx")
        # On récupère les données du fichier .tmx dans map_data
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # On charge les calques du fichier .tmx
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Génération d'un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # Définition d'une liste stockant les boites de collision
        self.collision = []
        # On récupère tous les objets de la carte
        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques en créant un objet "PyscrollGroup"
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

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
            self.player.change_animation('down')
        elif pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')
        elif pressed[pygame.K_z] or pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        if pressed[pygame.K_LSHIFT]:
            self.player.speed = 3.5
        else:
            self.player.speed = 2

    def update(self):
        """Actualise le groupe"""
        self.group.update()

        # Vérification des collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.collision) > -1:
                sprite.move_back()

    def run(self):
        """Boucle du jeu"""
        # Création d'un objet "Clock" permettant de gérer le temps
        clock = pygame.time.Clock()
        running = True

        while running:

            # On mémorise la position du joueur
            self.player.save_location()
            # On gère toutes les entrées
            self.handle_imput()
            # Actualisation du groupe
            self.update()
            # On centre la caméra sur le joueur
            self.group.center(self.player.rect.center)
            # Affichage des calques sur la fenêtre d'affichage
            self.group.draw(self.screen)
            # Actualisation de la fenêtre
            pygame.display.flip()

            for event in pygame.event.get():
                # Stoppe la boucle de jeu lorsque la fenêtre est fermée
                if event.type == pygame.QUIT:
                    running = False

            # Cadence le taux de rafraîchissement de la fenêtre à 60 ips
            clock.tick(60)

        # Déinitialise tous les modules pygame
        pygame.quit()
