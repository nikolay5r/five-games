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

        self.image = self.frames[self.frame_index]        
        self.rect = self.image.get_frect(center = pos)

        # collisions
        self.collision_sprites = collision_sprites

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.gravity = 50
        self.jump_velocity = 20
        self.can_jump = True


    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right

                if direction == 'vertical':
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    if self.direction.y > 0: 
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0 # so the direction doesn't increase to infinity
                        self.can_jump = True 


    def move(self, dt):
        # horizontal
        self.rect.centerx += self.direction.x * self.speed * dt
        self.collision("horizontal")

        # vertical
        self.direction.y += self.gravity * dt # apply gravity
        self.rect.centery += self.direction.y
        self.collision("vertical")

    def get_direction(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])

        # jump input
        if self.can_jump and (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]):
            self.direction.y = -self.jump_velocity  
            self.can_jump = False 

    def setup_frames(self):
        for root, _, files in walk(join("images", "player")):
            self.frames = [pygame.image.load(join(root, file)) for file in files]

    def update(self, dt):
        self.get_direction()
        self.move(dt)