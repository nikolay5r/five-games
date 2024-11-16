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
        self.collision_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(surfaces.PLAYER_SURFACE_FRAMES, (self.all_sprites, ), (self.collision_sprites, ))

        for i in range(6):
            x, y = random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)
            w, h = random.randint(50, 100), random.randint(50, 100)
            CollisionSprite((x, y), (w, h), (self.all_sprites, self.collision_sprites))
    
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