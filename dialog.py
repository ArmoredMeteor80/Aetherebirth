import pygame


class DialogBox:
    """Une boîte de dialogue"""

    def __init__(self):
        """Constructeur"""
        self.box = pygame.image.load('dialogs/dialog_box.png').convert_alpha()
        self.box = pygame.transform.scale(self.box, (1200, 188))
        self.texts = []
        self.letter_index = 0
        self.text_index = 0
        self.font = pygame.font.Font('dialogs/dialog_font.ttf', 36)
        self.reading = False

    def execute(self, dialog=[]):
        """Permet l'execution de la boite de dialogue"""
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

    def render(self, screen):
        """Affiche la boîte de dialogue"""
        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index

            x_position = screen.get_size()[0]*0.19
            y_position = screen.get_size()[1]*(47/60)
            screen.blit(self.box, (x_position, y_position))

            # Créer une liste de surfaces de texte avec un passage à la ligne tous les 23 caractères
            text_lines = []
            text_length = len(self.texts[self.text_index])
            start = 0
            while start < text_length:
                end = start + 23
                if end > text_length:
                    end = text_length
                text_lines.append(self.font.render(self.texts[self.text_index][start:end], False, (255, 255, 255)))
                start = end

            # Blitter chaque ligne de texte sur l'écran en prenant en compte la position verticale de chaque ligne
            line_height = self.font.get_height()
            for i, line in enumerate(text_lines):
                line_y = y_position + 15 + i * line_height
                screen.blit(line, (x_position + 100, line_y))

    def next_text(self):
        """Passe au texte suivant"""
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            self.reading = False
