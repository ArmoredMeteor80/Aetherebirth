import pygame

from animation import AnimateSprite


# La classe "Entity" hérite de la classe "AnimateSprite".
class Entity(AnimateSprite):
    """Classe d'une entité"""

    def __init__(self, name, x, y, size=32):
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
        if isinstance(self, Player) and self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_right'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_right' if self.is_running else 'right'
        self.change_animation(f"{animation}")
        self.position[0] += self.speed if not self.is_exhausted[0] else self.speed - 1

    def move_left(self):
        """Déplace l'entité à gauche"""
        if isinstance(self, Player) and self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_left'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_left' if self.is_running else 'left'
        self.change_animation(f"{animation}")
        self.position[0] -= self.speed if not self.is_exhausted[0] else self.speed - 1

    def move_up(self):
        """Déplace l'entité en haut"""
        if isinstance(self, Player) and self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_up'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_up' if self.is_running else 'up'
        self.change_animation(f"{animation}")
        self.position[1] -= self.speed if not self.is_exhausted[0] else self.speed - 1

    def move_down(self):
        """Déplace l'entité en bas"""
        if isinstance(self, Player) and self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_down'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_down' if self.is_running else 'down'
        self.change_animation(f"{animation}")
        self.position[1] += self.speed if not self.is_exhausted[0] else self.speed - 1

    def move_right_down(self):
        """Déplace l'entité en bas à droite"""
        if isinstance(self, Player) and self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_right'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_right' if self.is_running else 'right'
        self.change_animation(f"{animation}")
        self.position[0] += self.speed - 1
        self.position[1] += self.speed - 1

    def move_left_down(self):
        """Déplace l'entité en bas à gauche"""
        if isinstance(self, Player) and self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_left'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_left' if self.is_running else 'left'
        self.change_animation(f"{animation}")
        self.position[0] -= self.speed - 1
        self.position[1] += self.speed - 1

    def move_right_up(self):
        """Déplace l'entité en haut à droite"""
        if isinstance(self, Player) and self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_up'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_up' if self.is_running else 'up'
        self.change_animation(f"{animation}")
        self.position[0] += self.speed - 1
        self.position[1] -= self.speed - 1

    def move_left_up(self):
        """Déplace l'entité en haut à gauche"""
        if isinstance(self, Player) and self.is_exhausted[0] and self.is_exhausted[1] < 20:
            animation = 'exhausted_up'
            self.is_exhausted[1] += 1
        else:
            animation = 'sprint_up' if self.is_running else 'up'
        self.change_animation(f"{animation}")
        self.position[0] -= self.speed - 1
        self.position[1] -= self.speed - 1

    def stay_still(self, player):
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
        """Met à jour la position du joueur"""
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        """Replace le joueur à la position antérieure à une collision"""
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class Player(Entity):
    """Classe d'un joueur héritant de la Classe Entity"""

    def __init__(self, position):
        super().__init__("bob", position[0], position[1])
        self.stats = {"health": 100, "stamina": 100}
        self.health = self.stats['health']
        self.stamina = self.stats['stamina']

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

    def check_exhaustion(self):
        """Change le statut d'épuisement du joueur"""
        if self.stamina <= 1:
            self.is_exhausted[0] = True
        elif self.stamina >= self.stats['stamina'] / 3 and self.is_exhausted[0]:
            self.is_exhausted[0] = False
            self.is_exhausted[1] = 0


class NPC(Entity):
    """Classe des PNJ héritant de la Classe Entity"""

    def __init__(self, name, nb_points=1, dialog=None, npc_id=1, speed=1):
        super().__init__(name, 0, 0)
        if dialog is None:
            dialog = []
        self.nb_points = nb_points
        self.dialog = dialog
        self.points = []
        self.name = name
        self.default_speed = speed
        self.speed = 1
        self.current_point = 0
        self.id = npc_id

    def move(self, player):
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

    def load_points(self, tmx_data):
        """Charge les points de passage du PNJ"""
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}_{self.id}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)


class Enemy(Entity):
    """Classe des ennemis héritant de la Classe Entity"""
    def __init__(self, name, health, attack_damage, resistance, attack_radius, notice_radius):
        super().__init__(name, 0, 0)
        self.hitbox = self.rect.inflate(0, 10)
        self.health = health
        self.attack_damage = attack_damage
        self.resistance = resistance
        self.attack_radius = attack_radius
        self.notice_radius = notice_radius
        self.status = 'idle'

    def get_status(self, player):
        """Regarde où est le joueur"""
        distance = 1

        if distance <= self.attack_radius:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
