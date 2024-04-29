
from ..ui import AnimateSprite
from . import Entity
import os


class Player(Entity):
    """Classe d'un joueur héritant de la Classe Entity"""

<<<<<<< HEAD
    def __init__(self, position, player_health: int=100, player_name: str = f"Player_{os.urandom(5)}"):
=======
    def __init__(self, position: tuple, player_health: int = 100):
>>>>>>> 39c5727 (Ajout de documentation, notamment les types des paramètres dans les méthodes et fonctions, autrement, ajout de la capacité de modifier l'opacité d'un layer selon son nom)
        super().__init__("bob", position[0], position[1])
        self.stats = {"health": 100, "stamina": 100, "attack_damage" : 25}
        self.health = player_health
        self.stamina = self.stats['stamina']
        self.attack_damage = self.stats['attack_damage']
        self.player_name = player_name

    def stamina_regen(self, regen_rate: float):
        """Régénération passive/active d'endurance"""
        if self.stamina < self.stats['stamina']:
            self.stamina += regen_rate

    def stamina_depletion(self, deplet_rate: float, passive=True):
        """Epuisement passif/actif d'endurance"""
        if passive:
            if self.stamina >= deplet_rate:
                self.stamina -= deplet_rate
        else:
            self.stamina -= deplet_rate

    def health_regen(self, regen_rate: float):
        """Régénération de la vie"""
        if self.health < self.stats['health']:
            self.health += regen_rate

    def health_depletion(self, deplet_rate: float):
        """Epuisement de la vie"""
        self.health -= deplet_rate

    def check_exhaustion(self):
        """Change le statut d'épuisement du joueur"""
        if self.stamina <= 1:
            self.is_exhausted[0] = True
        elif self.stamina >= self.stats['stamina'] / 3 and self.is_exhausted[0]:
            self.is_exhausted[0] = False
            self.is_exhausted[1] = 0
