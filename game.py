import pygame
import pytmx
import pyscroll


class Game:
    """Représentation du concept du jeu"""
    def __init__(self):
        """Constructeur"""
        # Création de la fenêtre de
        self.screen = pygame.display.set_mode((1280, 720))
        # Change le titre de la fenêtre
        pygame.display.set_caption("Pyb0b")

        # Charge la carte tmx en créant un objet "TiledMap" contenant les calques, objets et images d'une carte .tmx
        tmx_data = pytmx.util_pygame.load_pygame("carte.tmx")
        # On récupère les données du fichier .tmx dans map_data
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # On charge les calques du fichier .tmx
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        # Dessiner le groupe de calques en créant un objet "PyscrollGroup"
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

    def run(self):
        """Boucle du jeu"""
        # Création d'un objet "Clock" permettant de gérer le temps
        clock = pygame.time.Clock()
        running = True

        while running:

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
