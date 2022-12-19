import pygame


class Game:
    """Représentation du concept du jeu"""
    def __init__(self):
        """Constructeur"""
        # Création de la fenêtre de jeu
        pygame.display.set_mode((1280, 720))
        # Change le titre de la fenêtre
        pygame.display.set_caption("Pyb0b")

    def run(self):
        """Boucle du jeu"""
        # Création d'un objet "Clock" permettant de gérer le temps
        clock = pygame.time.Clock()
        running = True

        while running:

            for event in pygame.event.get():
                # Stoppe la boucle de jeu lorsque la fenêtre est fermée
                if event.type == pygame.QUIT:
                    running = False

            # Cadence le taux de rafraîchissement de la fenêtre à 60 ips
            clock.tick(60)

        # Déinitialise tous les modules pygame
        pygame.quit()
