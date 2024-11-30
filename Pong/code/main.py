import pygame
import settings

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.display_surface.fill(settings.COLORS["bg"])

            pygame.display.update()
        
        pygame.quit()


game = Game()
game.run()
