from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, frames, groups, collision_sprite_groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.animation_state = "down"
        self.animation_speed = 10

        self.image = self.frames[self.animation_state][self.frame_index]
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.hitbox_rect = self.rect.inflate(-60, -5)

        self.direction = pygame.math.Vector2()
        self.speed = 400

        self.collision_sprite_groups = collision_sprite_groups
    
    def __input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def __collision(self, direction):
        for collision_sprites in self.collision_sprite_groups:
            for sprite in collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if direction == "horizontal":
                        if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                        elif self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                    elif direction == "vertical":
                        if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                        elif self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom

    def __move(self, dt):
        self.hitbox_rect.centerx += self.direction.x * self.speed * dt
        self.__collision("horizontal")
        self.hitbox_rect.centery += self.direction.y * self.speed * dt
        self.__collision("vertical")
        self.rect.center = self.hitbox_rect.center

    def __get_animation_state(self):
        if self.direction == pygame.math.Vector2(0, 0):
            self.animation_state = "down"
            self.frame_index = 0
        elif self.direction.y > 0:
            self.animation_state = "down"
        elif self.direction.y < 0:
            self.animation_state = "up"
        elif self.direction.x > 0:
            self.animation_state = "right"
        elif self.direction.x < 0:
            self.animation_state = "left"
        else:
            self.animation_state = "down"

    def __animate(self):
        self.__get_animation_state()

        self.image = self.frames[self.animation_state][int(self.frame_index) % len(self.frames[self.animation_state])]
        self.rect = self.image.get_frect(center = self.rect.center)
        self.hitbox_rect = self.rect.inflate(-60, -5)

    def update(self, dt):
        self.frame_index += self.animation_speed * dt
        self.__input()
        self.__animate()
        self.__move(dt)

        
        