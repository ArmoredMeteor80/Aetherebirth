
from ..ui import AnimateSprite
from . import Entity

class Player(Entity):
    """Classe d'un joueur héritant de la Classe Entity"""

    def __init__(self, position, player_health: int=100):
        super().__init__("bob", position[0], position[1])
        self.stats = {"health": 100, "stamina": 100, "attack_damage" : 25}
        self.health = player_health
        self.stamina = self.stats['stamina']
        self.attack_damage = self.stats['attack_damage']

    def stamina_regen(self, regen_rate):
        """Régénération passive/active d'endurance"""
        if self.stamina < self.stats['stamina']:
            self.stamina += regen_rate

    def stamina_depletion(self, deplet_rate, passive=True):
        """Epuisement passif/actif d'endurance"""
        if passive:
            if self.stamina >= deplet_rate:
                self.stamina -= deplet_rate
        else:
            self.stamina -= deplet_rate

    def health_regen(self, regen_rate):
        """Régénération de la vie"""
        if self.health < self.stats['health']:
            self.health += regen_rate

    def health_depletion(self, deplet_rate):
        """Epuisement de la vie"""
        self.health -= deplet_rate

    def check_exhaustion(self):
        """Change le statut d'épuisement du joueur"""
        if self.stamina <= 1:
            self.is_exhausted[0] = True
        elif self.stamina >= self.stats['stamina'] / 3 and self.is_exhausted[0]:
            self.is_exhausted[0] = False
            self.is_exhausted[1] = 0
