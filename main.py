import pygame
import os

from src.game import Game

if __name__ == '__main__':
    # Initialisation de tous les modules Pygame
    pygame.init()

    # Création d'un objet "Game" gérant le jeu, ici seul le menu de démarrage est lancé
    size = (1920, 1080)
    game = Game(size, False)

    # On affiche le menu et récupérons le choix de l'utilisateur quant à la progression de sa partie
    new_game_or_continue = game.run()

    # Si le joueur a choisi "Nouvelle partie"..

    if new_game_or_continue == "new_game":
        # On supprime tous les fichiers de sauvegarde
        for filename in os.listdir("save_data"):
            file_path = os.path.join("save_data", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    elif new_game_or_continue == "quit":
        game.shutting_down()

    if game.running:
        # On crée une nouvelle instance de la classe Game
        game = Game(size, True)

        # On lance le jeu
        game.run()
