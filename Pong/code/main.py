import pygame
import settings

from sprites.player import Player
from sprites.ball import Ball
 
class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.running = True
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()

        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball((self.all_sprites), self.paddle_sprites)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.display_surface.fill(settings.COLORS["bg"])

            self.all_sprites.draw(self.display_surface)
            self.all_sprites.update(dt)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()

    
