from __future__ import annotations
import pygame

from ..ui import AnimateSprite


# La classe "Entity" hérite de la classe "AnimateSprite".
class Entity(AnimateSprite):
    """Classe d'une entité"""

    def __init__(self, name: str, x: int, y: int, size=32):
        """Constructeur qui initialise la Classe 'Sprite'"""
        super().__init__(name)
        if "chicken" in name:
            size = 16
        self.image = self.get_image(0, 0, size)
        # enlève le noir du sprite au profit du transparent
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 8)
        self.old_position = self.position.copy()
        self.is_running = False
        self.is_exhausted = [False, 0]
        self.is_attacking = False
        self.attack_cooldown = 0

    def save_location(self):
        """Mémorise la position de l'entité"""
        self.old_position = self.position.copy()

    def move_right(self):
        """Déplace l'entité à droite"""
        if self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_right'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_right' if self.is_running else 'right'
        self.change_animation(f"{animation}")
        self.position[0] += self.speed if not self.is_exhausted[0] else self.speed - 1

    def move_left(self):
        """Déplace l'entité à gauche"""
        if self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_left'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_left' if self.is_running else 'left'
        self.change_animation(f"{animation}")
        self.position[0] -= self.speed if not self.is_exhausted[0] else self.speed - 1

    def move_up(self):
        """Déplace l'entité en haut"""
        if self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_up'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_up' if self.is_running else 'up'
        self.change_animation(f"{animation}")
        self.position[1] -= self.speed if not self.is_exhausted[0] else self.speed - 1

    def move_down(self):
        """Déplace l'entité en bas"""
        if self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_down'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_down' if self.is_running else 'down'
        self.change_animation(f"{animation}")
        self.position[1] += self.speed if not self.is_exhausted[0] else self.speed - 1

    def move_right_down(self):
        """Déplace l'entité en bas à droite"""
        if self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_right'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_right' if self.is_running else 'right'
        self.change_animation(f"{animation}")
        self.position[0] += self.speed - 1
        self.position[1] += self.speed - 1

    def move_left_down(self):
        """Déplace l'entité en bas à gauche"""
        if self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_left'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_left' if self.is_running else 'left'
        self.change_animation(f"{animation}")
        self.position[0] -= self.speed - 1
        self.position[1] += self.speed - 1

    def move_right_up(self):
        """Déplace l'entité en haut à droite"""
        if self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_up'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_up' if self.is_running else 'up'
        self.change_animation(f"{animation}")
        self.position[0] += self.speed - 1
        self.position[1] -= self.speed - 1

    def move_left_up(self):
        """Déplace l'entité en haut à gauche"""
        if self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_up'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_up' if self.is_running else 'up'
        self.change_animation(f"{animation}")
        self.position[0] -= self.speed - 1
        self.position[1] -= self.speed - 1

    def stay_still(self, player: Player):
        """Permet aux PNJ de rester statiques"""
        x_diff = player.position[0] - self.position[0]
        y_diff = player.position[1] - self.position[1]
        distance = (x_diff ** 2 + y_diff ** 2) ** 0.5
        if distance <= 40:
            if abs(x_diff) > abs(y_diff):
                if x_diff > 0:
                    self.change_animation("still_npc_right")
                else:
                    self.change_animation("still_npc_left")
            else:
                if y_diff > 0:
                    self.change_animation("still_npc_down")
                else:
                    self.change_animation("still_npc_up")
        else:
            self.change_animation("still_npc_down")

    def attack(self):
        """Déclenche une attaque"""
        self.change_animation("attack")
        self.attack_cooldown += 1
        if self.attack_cooldown == 20:
            self.is_attacking = False
            self.attack_cooldown = 0

    def update(self):
        """Met à jour la position de l'entité"""
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        """Replace le joueur à la position antérieure à une collision"""
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

class NPC(Entity):
    """Classe des PNJ héritant de la Classe Entity"""

    def __init__(self, name: str, nb_points: int = 1, dialog: list[str] = [], npc_id: int = 1, speed: float = 1):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.dialog = dialog
        self.points = []
        self.name = name
        self.default_speed = speed
        self.speed = 1
        self.current_point = 0
        self.id = npc_id

    def move(self, player: Player):
        """Déplace le PNJ"""
        if self.nb_points == 1 or self.speed == 0:
            self.stay_still(player)
        else:
            current_point = self.current_point
            target_point = self.current_point + 1

            if target_point == self.nb_points:
                target_point = 0

            current_rect = self.points[current_point]
            target_rect = self.points[target_point]
            if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
                self.move_down()
            elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
                self.move_up()
            elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
                self.move_left()
            elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
                self.move_right()

            if self.rect.colliderect(target_rect):
                self.current_point = target_point

    def teleport_spawn(self):
        """Place le PNJ à son point d'apparition"""
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data: pytmx.TiledMap):
        """Charge les points de passage du PNJ"""
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}_{self.id}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)


class Enemy(NPC):
    """Classe des ennemis héritant de la Classe Entity"""
    def __init__(self, name, health, attack_damage, attack_radius, notice_radius, npc_id=1, cooldown_time=30,
                 nb_points=1):
        super().__init__(name)
        self.hitbox = self.rect.inflate(0, 10)
        self.health = health
        self.attack_damage = attack_damage
        self.attack_radius = attack_radius
        self.notice_radius = notice_radius
        self.status = 'idle'
        self.direction = pygame.math.Vector2()
        self.cooldown_time = cooldown_time
        self.nb_points = nb_points
        self.pathing = False
        self.is_attacked = False
        self.id = npc_id

    def get_player_distance_direction(self, player: Player):
        """Renvoie la distance et la direction entre le joueur et l'ennemi"""
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return distance, direction

    def get_point_distance_direction(self):
        """Renvoie la distance et la direction entre le point de passage et l'ennemi"""
        enemy_vec = pygame.math.Vector2(self.rect.center)

        current_point_vec = pygame.math.Vector2(self.points[self.current_point].bottomright)
        distance = (current_point_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (current_point_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return distance, direction

    def get_status(self, player: Player):
        """Regarde où est le joueur"""
        distance = self.get_player_distance_direction(player)[0]
        if self.health <= 0:
            self.status = 'dead'
        elif distance <= self.attack_radius:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

        if not player.is_attacking:
            self.is_attacked = False
        if distance <= self.attack_radius+10 and player.is_attacking and not self.is_attacked:
            self.is_attacked = True
            self.health -= player.attack_damage

    def actions(self, player: Player):
        """Définis les actions selon le statut"""
        if self.status == "attack":
            self.attack_cooldown += 1
            if self.attack_cooldown == self.cooldown_time:
                self.attack_cooldown = 0
                player.health_depletion(self.attack_damage)

        elif self.status == "move":
            self.pathing = False
            self.direction = self.get_player_distance_direction(player)[1]

        else:
            if not self.pathing:
                self.direction = self.get_point_distance_direction()[1]

    def enemy_update(self, player: Player):
        """Met à jour les ennemis"""
        self.get_status(player)
        self.actions(player)

    def move_enemy(self, player: Player):
        """Déplace l'ennemi"""
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.position[0] += self.direction.x * self.speed
        self.position[1] += self.direction.y * self.speed

        x_diff = player.position[0] - self.position[0]
        y_diff = player.position[1] - self.position[1]
        distance = (x_diff ** 2 + y_diff ** 2) ** 0.5
        if distance <= self.notice_radius:
            if abs(x_diff) > abs(y_diff):
                if x_diff > 0:
                    self.change_animation("right")
                else:
                    self.change_animation("left")
            else:
                if y_diff > 0:
                    self.change_animation("down")
                else:
                    self.change_animation("up")
        else:
            x_diff = self.points[self.current_point][0] - self.position[0]
            y_diff = self.points[self.current_point][1] - self.position[1]
            if abs(x_diff) > abs(y_diff):
                if x_diff > 0:
                    self.change_animation("right")
                else:
                    self.change_animation("left")
            else:
                if y_diff > 0:
                    self.change_animation("down")
                else:
                    self.change_animation("up")
            if not self.pathing:
                if self.get_point_distance_direction()[0] == 0:
                    self.pathing = True
            else:
                self.move(player)



