from settings import *
from timers import Timer

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_frect(center = pos)

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups):
        self.animation_speed = 7
        self.frame_index = 0
        self.frames = frames
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Bee(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

    def update(self, dt):
        self.animate(dt)

class Worm(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

    def update(self, dt):
        self.animate(dt)


class Player(AnimatedSprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(pos, frames, groups)

        # animation
        self.jump_frame_index = 1
        self.is_facing_left = False
        
        self.image = self.frames[self.frame_index]        
        self.rect = self.image.get_frect(center = pos)

        # collisions
        self.collision_sprites = collision_sprites

        # movement
        self.direction = pygame.math.Vector2()
        self.last_direction = self.direction
        self.speed = 300
        self.gravity = 50
        self.jump_velocity = 20
        self.can_jump = True

        # shooting
        self.shoot_timer = Timer(500)

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right

                if direction == 'vertical':
                    if self.direction.y < 0: 
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 0 # so the player doesn't float in the air when hitting an object from bellow

                    if self.direction.y > 0: 
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0 # so the direction doesn't increase to infinity
                        self.can_jump = True 

    def animate(self, dt):
        if self.direction.x:
            super().animate(dt)
            self.is_facing_left = self.direction.x < 0
        else:
            self.frame_index = 0
            self.image = self.frames[self.frame_index]
        
        if not self.can_jump:
            self.image = self.frames[self.jump_frame_index]
            self.frame_index = self.jump_frame_index + 1

        self.image = pygame.transform.flip(self.image, self.is_facing_left, False)

    def move(self, dt):
        # horizontal
        self.rect.centerx += self.direction.x * self.speed * dt
        self.collision("horizontal")

        # vertical
        self.direction.y += self.gravity * dt # apply gravity
        self.rect.centery += self.direction.y
        self.collision("vertical")

    def input(self):
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()

        self.direction.x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])

        # jump input
        if self.can_jump and (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]):
            self.direction.y = -self.jump_velocity  
            self.can_jump = False 

        if not self.shoot_timer and (keys[pygame.K_RETURN] or mouse_keys[0]):
            print("shoot")
            self.shoot_timer.activate()

    def update(self, dt):
        self.last_direction = self.direction

        self.shoot_timer.update()
        self.input()
        self.move(dt)
        self.animate(dt)