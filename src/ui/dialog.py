from __future__ import annotations
import pygame


class DialogBox:
    """Une boîte de dialogue"""

    def __init__(self):
        """Constructeur"""
        self.box = pygame.image.load('assets/dialogs/dialog_box.png').convert_alpha()
        self.box = pygame.transform.scale(self.box, (1200, 220))
        self.texts = []
        self.letter_index = 0
        self.text_index = 0
        self.font = pygame.font.Font('assets/dialogs/dialog_font.ttf', 36)
        self.reading = False
        self.sound = pygame.mixer.Sound('assets/sounds/dialog_sound.wav')

    def execute(self, dialog: list):
        """Permet l'execution de la boite de dialogue"""
        pygame.mixer.Sound.play(self.sound).set_volume(0.2)
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog

    def terminate(self):
        """Met fin au dialogue"""
        if self.reading:
            self.reading = False

    def render(self, screen: pygame.surface.Surface):
        """Affiche la boîte de dialogue"""
        if self.reading:
            # Positionnement et affichage de la boîte de dialogue
            x_position = screen.get_size()[0] * 0.19
            y_position = screen.get_size()[1] * (47 / 60)
            screen.blit(self.box, (x_position, y_position))

            # Obtenir le texte en cours de lecture et le découper en lignes de texte avec un passage à la ligne
            # tous les 50 caractères
            text = self.texts[self.text_index][:self.letter_index + 1]
            text_lines = []
            start = 0
            while True:
                end = start + 50
                if end >= len(text):
                    text_lines.append(self.font.render(text[start:].strip(), False, (255, 255, 255)))
                    break
                while end > start and text[end] != " ":
                    end -= 1
                text_lines.append(self.font.render(text[start:end].strip(), False, (255, 255, 255)))
                start = end + 1

            # Blitter chaque ligne de texte sur l'écran en prenant en compte la position verticale de chaque ligne
            line_height = self.font.get_height()
            for i, line in enumerate(text_lines):
                line_y = y_position + 15 + i * line_height
                screen.blit(line, (x_position + 100, line_y))

            # Attendre un peu avant de passer à la lettre suivante
            pygame.time.wait(10)
            self.letter_index += 1

    def next_text(self):
        """Passe au texte suivant"""
        self.text_index += 1
        self.letter_index = 0

        if self.text_index < len(self.texts):
            # affiche le texte suivant
            self.reading = True
        else:
            # Ferme la boîte de dialogue si le texte est terminé
            self.reading = False
