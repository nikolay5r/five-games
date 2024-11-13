# Example file showing a basic pygame "game loop"
import pygame
from os.path import join
from pygame.math import Vector2
import random

IMAGES_PATH = join("assets", "images")
AUDIO_PATH = join("assets", "audio")
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

PLAYER_SURF = pygame.image.load(join(IMAGES_PATH, "player.png")).convert_alpha()

class Player(pygame.sprite.Sprite):
    def __init__(self, surface, *groups):
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = Vector2()
        self.speed = 400
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt



# pygame setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True

clock = pygame.Clock()

all_sprites = pygame.sprite.Group()

player = Player(PLAYER_SURF, all_sprites)

while running:
    dt = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill("darkgray")

    all_sprites.update(dt)
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()