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

