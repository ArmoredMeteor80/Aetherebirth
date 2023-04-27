import pygame


class UI:
    """Interface Utilisateur"""
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/dialogs/dialog_font.ttf', 18)

        # Config des barres
        self.health_bar_rect = pygame.Rect(20, 20, 300, 25)
        self.stamina_bar_rect = pygame.Rect(20, 55, 200, 25)

    def show_bar(self, current_amount, max_amount, bg_rect, color):
        """Affiche les barres"""
        # On dessine le fond des barres
        pygame.draw.rect(self.display_surface, (49, 26, 18), bg_rect)

        # On convertit les stats en pixels
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # ON dessine les barres
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, (79, 56, 48), current_rect, 3)
        pygame.draw.rect(self.display_surface, (79, 56, 48), bg_rect, 3)

    def display(self, player):
        """Affiche l'interface utilisateur"""
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, 'red')
        if player.is_exhausted[0]:
            self.show_bar(player.stamina, player.stats['stamina'], self.stamina_bar_rect, 'orange')
        else:
            self.show_bar(player.stamina, player.stats['stamina'], self.stamina_bar_rect, 'blue')
