import pygame
import settings

from abc import ABC, abstractmethod

class Paddle(pygame.sprite.Sprite, ABC):
    def __init__(self, type: str, groups: tuple):
        super().__init__(groups)

        self.image = pygame.Surface(settings.SIZE["paddle"])
        self.image.fill(settings.COLORS["paddle"])
        self.rect = self.image.get_frect(center = settings.POS[type])

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

    @abstractmethod
    def update(self, dt):
        pass
