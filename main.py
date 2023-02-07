import pygame

from game import Game

if __name__ == '__main__':
    # Initialise tous les modules Pygame
    pygame.init()
    # Création d'un objet "Game" gérant le jeu
    game = Game(1280, 720)
    game.run()
