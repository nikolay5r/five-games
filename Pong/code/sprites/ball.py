import pygame
import settings

from random import choice, uniform

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups: tuple) -> None:
        super().__init__(groups)
        self.image = pygame.Surface(settings.SIZE["ball"], pygame.SRCALPHA)
        pygame.draw.circle(self.image, settings.COLORS["ball"], (settings.SIZE["ball"][0] / 2, settings.SIZE["ball"][1] / 2), settings.SIZE["ball"][0] / 2)
        
        self.rect = self.image.get_frect(center = (settings.WINDOW_HEIGHT / 2, settings.WINDOW_WIDTH / 2))
        self.direction = pygame.math.Vector2(choice((-1, 1)), uniform(0.7, 0.8) * choice((-1, 1)))
        self.speed = settings.SPEED["ball"]

    def __screen_collisions(self):
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction[1] *= -1
        elif self.rect.bottom > settings.WINDOW_HEIGHT:
            self.rect.bottom = settings.WINDOW_HEIGHT
            self.direction[1] *= -1

        if self.rect.left < 0:
            self.rect.left = 0
            self.direction[0] *= -1  
        elif self.rect.right > settings.WINDOW_WIDTH:
            self.rect.right = settings.WINDOW_WIDTH
            self.direction[0] *= -1

    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def collisions(self):
        self.__screen_collisions()

    def update(self, dt):
        self.move(dt)
        self.collisions()

    