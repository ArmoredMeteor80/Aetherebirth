from dataclasses import dataclass
from typing import List, Tuple

import pygame
import pyscroll
import pytmx

from .. import game

from ..entity import NPC, Enemy, Player
from ..ui import DialogBox


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
    sign_texts: dict
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]
    enemies: list[Enemy]


class MapManager:
    """Gère la dynamique de carte"""

    def __init__(self, screen: pygame.surface.Surface, player: Player, current_map: str):
        # stockage des cartes dans un dictionnaire sous forme "castle" -> Map("castle", walls, group)
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = current_map

        # Chargement des cartes
        self.register_map("clairiere_map", portals=[
            Portal(from_world="clairiere_map", origin_point="enter_village1", target_world="village_map",
                   teleport_point="spawn_village1")
        ], npcs=[NPC("joffrey_cottain")])

        self.register_map("village_map", portals=[
            Portal(from_world="village_map", origin_point="enter_clairiere", target_world="clairiere_map",
                   teleport_point="spawn_clairiere2"),
            Portal(from_world="village_map", origin_point="enter_castle", target_world="castle_map",
                   teleport_point="spawn_castle"),
            Portal(from_world="village_map", origin_point="enter_maison1", target_world="maison1_map",
                   teleport_point="spawn_maison1"),
            Portal(from_world="village_map", origin_point="enter_maison2", target_world="maison2_map",
                   teleport_point="spawn_maison2"),
            Portal(from_world="village_map", origin_point="enter_maison3", target_world="maison3_map",
                   teleport_point="spawn_maison3")
        ], npcs=[NPC('lutin_pink'),
                 NPC('lutin_lime_green'),
                 NPC('lutin_purple'),
                 NPC('lutin_yellow'),
                 NPC('lutin_cyan'),
                 NPC('skeleton', nb_points=4, dialog=["Mhoooooo, ce mini squelette est super trognon..."]),
                 NPC('cat_white', nb_points=4, dialog=["~~ Meooww ~~"], speed=0.7),
                 NPC('chicken', nb_points=6, dialog=["Mais c'est quoi ce poulet !?"], speed=0.5),
                 NPC('chicken', nb_points=26, dialog=["Il est démoniaque ce poulet, ses mouvements sont chaotiques et "
                                                      "il va si vite !",
                                                      "Il doit sûrement s'appeler Chicken Run."], speed=3, npc_id=2),

                 NPC('lutin_lime_green', nb_points=4, dialog=["Ce lutin a l'air louche...",
                                                              "Mieux vaut ne pas l'approcher"], npc_id=2),
                 NPC('lutin_green', nb_points=7,
                     dialog=["Salutations !", "Tu ne trouves pas que la STATUE est magnifique ?",
                             "Moi elle m'apaise !", "J'adore cette STATUE !",
                             "Même Bartholdi il en fait pas des comme ça !",
                             "Au moins celle là elle a ses 2 bras... PAS COMME UNE CERTAINE 'VÉNUS' !",
                             "À bon entendeur..."]),
                 NPC('lutin_green', nb_points=2, dialog=["1...2...1...2", "Le sport c'est important...",
                                                         "Vous décidez de ne pas le déranger plus longtemps."],
                     npc_id=2, speed=2),
                 NPC('lutin_red', nb_points=10,
                     dialog=["Bienvenue à Châtelard !", "J'espère que tu y passeras un agréable séjour",
                             "Malheureusement pour toi l'accès au château est interdit pour le moment.",
                             "Coup dur pour le tourisme..."]),
                 NPC('lutin_cyan', nb_points=4, dialog=["Tu n'aurais pas vu mon chat ?", "JEAN PIERRE !",
                                                        "JEAN PIEEEEEERREEE !",
                                                        "VIENS ICI JEAN PIEEEEERRE !"], npc_id=2)])

        self.register_map("castle_map", portals=[
            Portal(from_world="castle_map", origin_point="enter_village5", target_world="village_map",
                   teleport_point="spawn_village2")], enemies=[Enemy("blue_blob", health=100, attack_damage=10,
                                                                     attack_radius=30, notice_radius=130, nb_points=6),
                                                               Enemy(name="blue_blob", health=100, attack_damage=10,
                                                                     attack_radius=30, notice_radius=130, nb_points=4,
                                                                     npc_id=2)])

        self.register_map("maison1_map", portals=[
            Portal(from_world="maison1_map", origin_point="enter_village2", target_world="village_map",
                   teleport_point="spawn_village4")])

        self.register_map("maison2_map", portals=[
            Portal(from_world="maison2_map", origin_point="enter_village3", target_world="village_map",
                   teleport_point="spawn_village5")
        ], npcs=[NPC('lutin_yellow')])

        self.register_map("maison3_map", portals=[
            Portal(from_world="maison3_map", origin_point="enter_village4", target_world="village_map",
                   teleport_point="spawn_village6")
        ], npcs=[NPC('dark_mage', nb_points=2, dialog=["Sans savoir pourquoi, vous connaissez le nom de cette "
                                                       "personne, Branlusque le Solitaire.",
                                                       "Ce mage noir est en passe de devenir un archimage noir, "
                                                       "en effet il a 49 ans."]),
                 NPC('lutin_green'),
                 NPC('lutin_purple'),
                 NPC('lutin_blue', nb_points=9, dialog=["Du travail.", "ENCORE du travail...", "TROP DE TRAVAIL !",
                                                        "Repasse plus tard, je suis trop occupé."]),
                 NPC('lutin_red', nb_points=2, dialog=["Bienvenue dans le bâtiment principal de Châtelard !",
                                                       "Il fait office de bibliothèque, de mairie,"
                                                       " et même de lieu de culte et de cimetière.",
                                                       "Tu y trouvera des tas de choses utile..."
                                                       " Si tu arrives à te concentrer",
                                                       "malgré EUGÈNE QUI N'ARRÊTE PAS DE COURIR !"])])
        self.teleport_npcs_enemies()

    def check_dialog_collisions(self, dialog_box: DialogBox):
        """Détecte les collisions avec les PNJ et les Panneaux"""
        for sprite in self.get_group().sprites():
            # Dialogues avec PNJ
            if sprite.rect.colliderect(self.player.rect) and type(sprite) is NPC and len(sprite.dialog) > 0:
                dialog_box.execute(sprite.dialog)
        # Dialogues avec Panneaux
        try:
            for key in self.get_sign_collision().keys():
                if self.player.rect.colliderect(self.get_sign_collision()[key][0]):
                    dialog_box.execute(self.get_sign_collision()[key][1])
        except:
            None

    def terminate_dialog(self, dialog_box: DialogBox):
        """Met fin au dialogue"""
        player_position = self.player.old_position
        if player_position != self.player.position:
            dialog_box.terminate()

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
                    game.Game.fade_in(self, (49, 26, 18), 5)
                    self.fade_out((49, 26, 18), 5)

        # Support des collisions
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.rect.inflate(10, 10).colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = sprite.default_speed
                if sprite.feet.inflate(-2, -2).colliderect(self.player.feet):
                    sprite.speed = 0
                    self.player.move_back()
            if sprite.feet.collidelist(self.get_collision()) > -1:
                sprite.move_back()

            elif type(sprite) is Enemy:
                if sprite.rect.inflate(-15, -15).colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = sprite.default_speed
                if sprite.feet.colliderect(self.player.feet):
                    sprite.speed = 0
                    self.player.move_back()
            if sprite.feet.collidelist(self.get_collision()) > -1:
                sprite.move_back()

    def fade_out(self, color: tuple, speed: int):
        """Filtre de fondu inverse"""
        fade = pygame.Surface(self.screen.get_size()).convert_alpha()
        fade.fill(color)
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
        for alpha in range(255, -1, -speed):
            self.screen.blit(screen_image, (0, 0))
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()

    def teleport_player(self, name: str):
        """Téléporte le joueur au point donné en paramètre"""
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name: str, portals: List[Portal] = [], npcs: List[NPC] = [], enemies: List = []):
        """Charge les différentes cartes"""
        # Charge la carte tmx en créant un objet "TiledMap" contenant les calques, objets et images d'une carte .tmx
        tmx_data = pytmx.util_pygame.load_pygame(f"assets/maps/{name}.tmx")
        self.tmx_data = tmx_data
        # On récupère les données du fichier .tmx dans map_data
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # On charge les calques du fichier .tmx
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 4

        self.change_layer_opacity('shadows1', 100)

        # Définition d'une liste stockant les boites de collision
        collision = []
        # Définition d'un dictionnaire stockant les textes des panneaux
        sign_texts = {}
        # On récupère tous les objets de la carte
        for obj in tmx_data.objects:
            if obj.name == "collision":
                collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if "sign" in obj.name:
                sign_texts[obj.name] = (pygame.Rect(obj.x, obj.y, obj.width, obj.height), [])
                for prop in obj.properties:
                    if prop.startswith("text"):
                        sign_texts[obj.name][1].append(obj.properties[prop])

        # Créer le groupe de calques en créant un objet "PyscrollGroup"
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        group.add(self.player)

        # On récupère tous les PNJ pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)

        for enemy in enemies:
            group.add(enemy)

        # Création d'un objet Map qu'on injecte dans le dictionnaire les repertoriant
        self.maps[name] = Map(name, collision, sign_texts, group, tmx_data, portals, npcs, enemies)

    def change_layer_opacity(self, layer_name: str, opacity: int):
        """Change pour chaque tuile des layers shadows1 l'opacité"""
        for tile in self.tmx_data.get_layer_by_name(layer_name).tiles():
            tile[2].set_alpha(opacity)

    # Accesseurs (getters)
    def get_map(self) -> Map:
        """Renvoie la carte actuellement affichée"""
        return self.maps[self.current_map]

    def get_group(self) -> pyscroll.PyscrollGroup:
        """Renvoie le groupe"""
        return self.get_map().group

    def get_collision(self) -> list:
        """Renvoie les collisions"""
        return self.get_map().collision

    def get_sign_collision(self) -> dict:
        """Renvoie les collisions avec les panneaux"""
        return self.get_map().sign_texts

    def get_object(self, name: str) -> pytmx.TiledObject:
        """Renvoie l'objet demandé"""
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs_enemies(self):
        """Teleporte les PNJ"""
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs
            enemies = map_data.enemies
            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()
            for enemy in enemies:
                enemy.load_points(map_data.tmx_data)
                enemy.teleport_spawn()

    def draw(self):
        """Dessine la carte et les sprites"""
        # On trie les sprites par ordre croissant de leur coordonnée y
        sprites = sorted(self.get_group().sprites(), key=lambda sprite: sprite.feet.y)

        # On parcourt la liste triée, on baisse le layer des sprites si le joueur se trouve en dessous des sprites
        # à l'inverse, on augmente le layer s'il est au-dessus
        player_passed = False
        for sprite in sprites:
            if sprite == self.player:
                player_passed = True
            else:
                if player_passed:
                    self.get_group().change_layer(sprite, 5)
                else:
                    self.get_group().change_layer(sprite, 3)

        # On dessine le groupe et on centre la caméra sur le joueur
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self, player: Player):
        """Actualise le groupe"""
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move(self.player)

        for enemy in self.get_map().enemies:
            if enemy.status == "dead":
                self.get_group().remove(enemy)
            enemy.enemy_update(player)
            enemy.move_enemy(player)
