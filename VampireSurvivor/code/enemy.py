from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, player, groups):
        super().__init__(groups)

        self.frames, self.frame_index, self.animation_speed = frames, 0, 20
        self.image = frames[self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_frect(center = pos)

        self.direction = pygame.math.Vector2()
        self.speed = 400

        self.player = player
        
    def __move(self, dt):
        player_pos = pygame.math.Vector2(self.player.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize() if self.rect.center != self.player.rect.center else self.direction
        self.rect.center += self.direction * self.speed * dt

    def __animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.__animate(dt)
        self.__move(dt)

        
