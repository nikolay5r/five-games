import surfaces

from settings import *
from math import atan2, degrees
from bullet import Bullet

class Gun(pygame.sprite.Sprite):
    def __init__(self, surface, player, groups, bullet_groups):
        self.player = player
        self.distance = 140
        self.direction = pygame.math.Vector2(1, 0)

        super().__init__(groups)
        self.surf = surface
        self.image = surface
        self.rect = self.image.get_frect(center = self.player.rect.center + self.distance * self.direction)

        self.fire_cooldown = 1500
        self.bullet_groups = bullet_groups
        self.can_fire_bullet = True
        self.last_fire_time = pygame.time.get_ticks()

    def __get_direction(self):
        mouse_pos = pygame.mouse.get_pos()
        player_pos = pygame.math.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        
        self.direction = (mouse_pos - player_pos).normalize() if mouse_pos != player_pos else self.direction

    def __rotate(self):
        angle = degrees(atan2(self.direction.x, self.direction.y)) - 90

        if self.direction.x > 0:
            self.image = pygame.transform.rotozoom(self.surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def __fire_timer(self):
        if not self.can_fire_bullet:
            current_time = pygame.time.get_ticks()

            if current_time + self.fire_cooldown >= self.last_fire_time:
                self.can_fire_bullet = True

    def __fire_bullet(self):
        just_pressed_keys = pygame.mouse.get_just_pressed()

        if just_pressed_keys[0] and self.can_fire_bullet:
            self.can_fire_bullet = False
            self.last_fire_time = pygame.time.get_ticks()
            Bullet(surfaces.BULLET_SURFACE, self.rect.center, self.direction, self.bullet_groups)
        

    def update(self, _):
        self.__get_direction()
        self.__rotate()
        self.rect.center = self.player.rect.center + self.distance * self.direction

        self.__fire_timer()
        self.__fire_bullet()
        print(self.can_fire_bullet)
