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
