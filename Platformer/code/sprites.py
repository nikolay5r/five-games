from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_frect(center = pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.setup_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        #collisions
        self.collision_sprites = collision_sprites

        #movement
        self.direction = pygame.math.Vector2()
        self.speed = 200
        self.jump_velocity = 100

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite == self: continue

            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right

                if direction == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom

    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.rect.centery += self.direction.y * self.jump_velocity * dt
        self.collision("vertical")

    def get_direction(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN])- int(keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE])

        if self.direction:
            self.direction = self.direction.normalize()

    def setup_frames(self):
        for root, _, files in walk(join("images", "player")):
            self.frames = [pygame.image.load(join(root, file)) for file in files]

    def update(self, dt):
        self.get_direction()
        self.move(dt)