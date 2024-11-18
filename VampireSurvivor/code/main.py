from settings import *
from sprites import *
from player import Player
from pytmx.util_pygame import load_pygame
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
    
        self.__setupTileMap()
        self.player = Player((500, 600), surfaces.PLAYER_SURFACE_FRAMES, (self.all_sprites, ), (self.collision_sprites, ))
    

    def __setupTileMap(self):
        world_map = load_pygame(join(MAPS_PATH, "world.tmx"))

        for x, y, image in world_map.get_layer_by_name("Ground").tiles():
            TileSprite((x, y), image, self.all_sprites)

        for obj in world_map.get_layer_by_name("Objects"):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))


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