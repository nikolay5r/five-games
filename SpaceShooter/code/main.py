# Example file showing a basic pygame "game loop"
import pygame
from os.path import join
import random

IMAGES_PATH = join("assets", "images")
AUDIO_PATH = join("assets", "audio")

# pygame setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True

player_surface = pygame.image.load(join(IMAGES_PATH, "player.png")).convert_alpha()
star_surface = pygame.image.load(join(IMAGES_PATH, "star.png")).convert_alpha()
star_positions = [(random.randint(0 + star_surface.size[0], WINDOW_WIDTH - star_surface.size[0]),
             random.randint(0 + star_surface.size[1], WINDOW_HEIGHT - star_surface.size[1])) for i in range(20)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill("darkgray")
    display_surface.blit(player_surface, (100, 200)) 
    for pos in star_positions:
        display_surface.blit(star_surface, pos)

    pygame.display.update()

pygame.quit()