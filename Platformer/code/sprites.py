from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_frect(center = pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.setup_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        #movement
        self.direction = pygame.math.Vector2()
        self.speed = 200

    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def get_direction(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        
        if self.direction:
            self.direction = self.direction.normalize()

    def setup_frames(self):
        for root, _, files in walk(join("images", "player")):
            self.frames = [pygame.image.load(join(root, file)) for file in files]

    def update(self, dt):
        self.get_direction()
        self.move(dt)