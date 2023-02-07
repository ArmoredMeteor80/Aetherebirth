from dataclasses import dataclass
import pygame
import pytmx
import pyscroll

import game
from player import Player


@dataclass
class Portal:
    """Data class contenant les caractéristiques des portails"""
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    """Data class contenant les propriétés d'une carte"""
    name: str
    collision: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]


class MapManager:
    """Gère la dynamique de carte"""
    def __init__(self, screen, player):
        # stockage des cartes dans un dictionnaire sous forme "test" -> Map("test", walls, group)
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "test_map"

        # Chargement des cartes
        self.register_map("test_map", portals=[
            Portal(from_world="test_map", origin_point="enter_clairiere", target_world="clairiere_map", teleport_point="spawn_clairiere")
        ])
        self.register_map("clairiere_map", portals=[
            Portal(from_world="clairiere_map", origin_point="enter_test", target_world="test_map", teleport_point="spawn_test")
        ])

        self.teleport_player("player")

    def check_collisions(self):
        """Détecte les collisions"""
        # Support des portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)
                    self.fade()

        # Support des collisions
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_collision()) > -1:
                sprite.move_back()

    def fade(self):
        """Filtre de fondu"""
        # on fait une copie de l'écran
        screen_image = self.screen.copy()
        # Surface qui va faire le fondu en augmentant et baissant sa valeur d'alpha
        fade = pygame.Surface(self.screen.get_size()).convert_alpha()
        fade.fill((49, 26, 18))
        for alpha in range(0, 256, 2):
            self.screen.blit(screen_image, (0, 0))
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()

        # Fondu inverse, on met d'abord à jour le joueur qui se met sur la nouvelle carte chargée,
        # puis on draw deux fois de sorte à afficher la carte derrière le fondu et centrer la caméra sur le joueur
        self.player.update()
        self.draw()
        self.draw()
        # Enfin on fait une copie de ce qu'il y a derriere le fondu (on exclut le fondu de la copie)
        fade_rect = fade.get_rect()
        self.screen.set_clip(fade_rect)
        screen_image = self.screen.copy()
        self.screen.set_clip(None)
        for alpha in range(255, -1, -2):
            self.screen.blit(screen_image, (0, 0))
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()

    def teleport_player(self, name):
        """Téléporte le joueur au point donné en paramètre"""
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[]):
        """Charge les différentes cartes"""
        # Charge la carte tmx en créant un objet "TiledMap" contenant les calques, objets et images d'une carte .tmx
        tmx_data = pytmx.util_pygame.load_pygame(f"assets/maps/{name}.tmx")
        # On récupère les données du fichier .tmx dans map_data
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # On charge les calques du fichier .tmx
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size(), alpha=True)
        map_layer.zoom = 3

        # Définition d'une liste stockant les boites de collision
        collision = []
        # On récupère tous les objets de la carte
        for obj in tmx_data.objects:
            if obj.name == "collision":
                collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques en créant un objet "PyscrollGroup"
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        group.add(self.player)

        # Création d'un objet Map qu'on injecte dans le dictionnaire les repertoriant
        self.maps[name] = Map(name, collision, group, tmx_data, portals)

    # Accesseurs (getters)
    def get_map(self):
        """Renvoie la carte actuellement affichée"""
        return self.maps[self.current_map]

    def get_group(self):
        """Renvoie le groupe"""
        return self.get_map().group

    def get_collision(self):
        """Renvoie les collisions"""
        return self.get_map().collision

    def get_object(self, name):
        """Renvoie l'objet demandé"""
        return self.get_map().tmx_data.get_object_by_name(name)

    # Mutateurs (setters)
    def draw(self):
        """Dessine la carte"""
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        """Actualise le groupe"""
        self.get_group().update()
        self.check_collisions()
