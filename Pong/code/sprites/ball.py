import pygame
import settings

from random import choice, uniform

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups: tuple, paddle_sprites: pygame.sprite.Group) -> None:
        super().__init__(groups)
        self.image = pygame.Surface(settings.SIZE["ball"], pygame.SRCALPHA)
        pygame.draw.circle(self.image, settings.COLORS["ball"], (settings.SIZE["ball"][0] / 2, settings.SIZE["ball"][1] / 2), settings.SIZE["ball"][0] / 2)
        
        self.rect = self.image.get_frect(center = (settings.WINDOW_HEIGHT / 2, settings.WINDOW_WIDTH / 2))
        self.old_rect = self.rect.copy()
        self.direction = pygame.math.Vector2(choice((-1, 1)), uniform(0.7, 0.8) * choice((-1, 1)))
        self.speed = settings.SPEED["ball"]

        self.paddle_sprites = paddle_sprites

    def __paddle_collisions(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.rect.right > sprite.rect.left and self.old_rect.right < sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction[0] *= -1
                    if self.rect.left < sprite.rect.right and self.old_rect.left > sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction[0] *= -1
                elif direction == "vertical":
                    if self.rect.bottom > sprite.rect.top and self.old_rect.bottom < sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction[1] *= -1
                    if self.rect.top < sprite.rect.bottom and self.old_rect.top > sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction[1] *= -1

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
        self.old_rect = self.rect.copy()

        self.rect.center += self.direction * self.speed * dt
        self.__paddle_collisions("horizontal")
        self.__paddle_collisions("vertical")

    def update(self, dt):
        self.move(dt)
        self.__screen_collisions()

    