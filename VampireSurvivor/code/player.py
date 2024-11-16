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
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.math.Vector2()
        self.speed = 400

    def __input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
    def __move(self, dt):
        self.rect.center += self.direction * self.speed * dt
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
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_frect(center = self.rect.center)

    def update(self, dt):
        self.frame_index += self.animation_speed * dt
        self.__input()
        self.__animate()
        self.__move(dt)

        
        