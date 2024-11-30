import pygame

from .paddle import Paddle

class Player(Paddle):
    def __init__(self, groups: tuple):
        super().__init__("player", groups)
    
    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])

    def update(self, dt):
        self.get_direction()
        self.move(dt)
        self.collisions()