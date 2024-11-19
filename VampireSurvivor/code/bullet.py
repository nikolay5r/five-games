from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surface, pos, direction, groups):
        super().__init__(groups)
        self.surf = surface
        self.image = surface
        print(pos)
        self.rect = self.image.get_frect(center = pos)

        self.direction = direction
        self.speed = 500
        self.lifetime = 1000
        self.spawn_time = pygame.time.get_ticks()

        self.rotation_speed = 20
    
    def __despawn_timer(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.lifetime >= self.spawn_time:
            self.kill()

    def __rotate(self, dt):
        self.image = pygame.transform.rotate(self.surf, self.rotation_speed * dt)
        self.rect = self.image.get_frect(center = self.rect.center)

    def update(self, dt):
        self.__despawn_timer()
        
        # self.__rotate(dt)
        self.rect.center += self.direction * self.speed * dt

