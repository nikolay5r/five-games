import surfaces

from settings import *
from sprites import *
from player import Player
from enemy import Enemy
from gun import Gun
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivor")
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.running = True
        self.enemy_spawn_positions = []

        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 2000)
    
        self.__setupTileMap()    

    def __setupTileMap(self):
        world_map = load_pygame(join(MAPS_PATH, "world.tmx"))

        for x, y, image in world_map.get_layer_by_name("Ground").tiles():
            TileSprite((x, y), image, self.all_sprites)

        for obj in world_map.get_layer_by_name("Objects"):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for col in world_map.get_layer_by_name("Collisions"):
            CollisionSprite((col.x, col.y), pygame.Surface((col.width, col.height)), self.collision_sprites)

        for entity in world_map.get_layer_by_name("Entities"):
            if entity.name == "Player":
                self.player = Player((entity.x, entity.y), surfaces.PLAYER_SURFACE_FRAMES, (self.all_sprites, ), (self.collision_sprites, ))
            else:
                self.enemy_spawn_positions.append(pygame.math.Vector2(entity.x, entity.y))
            
        Gun(surfaces.GUN_SURFACE, self.player, self.all_sprites, (self.all_sprites, self.bullet_sprites)) 

    def __collisions(self):
        for bullet in self.bullet_sprites:
            collided_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, True, pygame.sprite.collide_mask)
            if collided_sprites:
                bullet.kill()

        collided_sprites = pygame.sprite.spritecollide(self.player, self.enemy_sprites, True, pygame.sprite.collide_mask)

        if collided_sprites:
            self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == self.enemy_event:
                    enemy_ind = random.randint(0, len(surfaces.ENEMY_SURFACES_FRAMES) - 1)
                    enemy_spawn_ind = random.randint(0, len(self.enemy_spawn_positions) - 1)
                    Enemy(
                        self.enemy_spawn_positions[enemy_spawn_ind], 
                        surfaces.ENEMY_SURFACES_FRAMES[enemy_ind],
                        self.player,
                        (self.all_sprites, self.enemy_sprites)
                    )

            self.display_surface.fill("lightgreen")
            self.all_sprites.update(dt)            
            self.all_sprites.draw(self.player.rect.center)

            self.__collisions()

            pygame.display.update()
        
        pygame.quit()


game = Game()
game.run()