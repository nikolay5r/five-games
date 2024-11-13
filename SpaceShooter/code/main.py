# Example file showing a basic pygame "game loop"
import pygame
from os.path import join

IMAGES_PATH = join("assets", "images")
AUDIO_PATH = join("assets", "audio")

# pygame setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True

player_surface = pygame.image.load(join(IMAGES_PATH, "player.png")).convert_alpha()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            
    display_surface.fill("darkgray")
    display_surface.blit(player_surface, (100, 200)) 
    
    pygame.display.update() 

pygame.quit()