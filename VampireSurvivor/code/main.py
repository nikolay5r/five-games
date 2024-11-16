from settings import *
from sprites import *
from player import Player
import surfaces

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivor")
        self.all_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.running = True
    
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.display_surface.fill("lightgreen")
            self.all_sprites.update(dt)            
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()
        
        pygame.quit()

game = Game()
game.run()