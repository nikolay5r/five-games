import events

from sprites import Sprite, Player, Bullet
from groups import AllSprites
from support import *
from settings import * 

class Game:
    def __init__(self):
        # init
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        
        self.import_assets()
        self.setup_map()

    def import_assets(self):
        # import surfaces and frames
        self.player_frames = import_folder("images", "player")
        self.bee_frames = import_folder("images", "enemies", "bee")
        self.worm_frames = import_folder("images", "enemies", "worm")
        self.bullet_surf = import_image("images", "gun", "bullet")
        self.fire_surf = import_image("images", "gun", "fire")

        # import audio
        self.audio = import_audio("audio")

    def setup_map(self):
        tmx_map = load_pygame(join("data", "maps", "world.tmx"))
        
        for x, y, image in tmx_map.get_layer_by_name("Main").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image in tmx_map.get_layer_by_name("Decoration").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))

        for obj in tmx_map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.player_frames, self.all_sprites, self.collision_sprites)

    def create_bullet(self):
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        mouse_pos = pygame.mouse.get_pos()
        direction = pygame.Vector2(mouse_pos - player_pos).normalize()

        Bullet(self.player.rect.center, direction, self.bullet_surf, (self.all_sprites, self.bullet_sprites))

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
                if event.type == events.CREATE_BULLET:
                    self.create_bullet()

            # update
            self.all_sprites.update(dt)

            # draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 