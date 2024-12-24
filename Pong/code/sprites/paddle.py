import pygame
import settings

from abc import ABC, abstractmethod

class Paddle(pygame.sprite.Sprite, ABC):
    def __init__(self, type: str, groups: tuple):
        super().__init__(groups)

        self.image = pygame.Surface(settings.SIZE["paddle"], pygame.SRCALPHA)
        pygame.draw.rect(self.image, settings.COLORS["paddle"], pygame.FRect((0, 0), settings.SIZE["paddle"]), 0, 4)
        self.rect = self.image.get_frect(center = settings.POS[type])
        self.old_rect = self.rect.copy()

        self.direction = 0
        self.speed = settings.SPEED[type]

    def __screen_collisions(self):
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > settings.WINDOW_HEIGHT:
            self.rect.bottom = settings.WINDOW_HEIGHT

    def collisions(self):
        self.__screen_collisions()

    def move(self, dt):
        self.rect.centery += self.speed * self.direction * dt
    
    @abstractmethod
    def get_direction(self):
        pass

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.move(dt)
        self.get_direction()
        self.collisions()


class Player(Paddle):
    def __init__(self, groups: tuple):
        super().__init__("player", groups)
    
    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])


class Opponent(Paddle):
    def __init__(self, groups: tuple, ball):
        super().__init__("opponent", groups)
        self.ball = ball
    
    def get_direction(self):
       self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1

