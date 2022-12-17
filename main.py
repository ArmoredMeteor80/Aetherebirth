import pygame

# Initialise tous les modules Pygame
pygame.init()

# Création de la fenêtre de jeu
pygame.display.set_mode((1280, 720))
# Change le titre de la fenêtre
pygame.display.set_caption("Pyb0b")

# Boucle du jeu
running = True

while running:
    for event in pygame.event.get():
        # Stoppe la boucle de jeu lorsque la fenêtre est fermée
        if event.type == pygame.QUIT:
            running = False

# Déinitialise tous les modules pygame
pygame.quit()
