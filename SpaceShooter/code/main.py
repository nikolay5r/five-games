# Example file showing a basic pygame "game loop"
import pygame
from os.path import join
import random

IMAGES_PATH = join("assets", "images")
AUDIO_PATH = join("assets", "audio")
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
NUMBER_OF_STARS = 30

class Player(pygame.sprite.Sprite):
    def __init__(self, surface, *groups):
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 400
        self.can_shoot = True
        self.last_laser_shot_time = 0
        self.laser_cooldown = 500
    
    def __laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_laser_shot_time > self.laser_cooldown:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        just_pressed_keys = pygame.key.get_just_pressed()
        if just_pressed_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(LASER_SURF, self.rect.center, all_sprites, laser_sprites)
            self.can_shoot = False
            self.last_laser_shot_time = pygame.time.get_ticks()
        
        self.__laser_timer()


class Star(pygame.sprite.Sprite):
    def __init__(self, surface, *groups):
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_frect(center = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))


class Laser(pygame.sprite.Sprite):
    def __init__(self, surface, pos, *groups):
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 400

    def update(self, dt):
        if self.rect.bottom > 0:
            self.rect.center += self.direction * self.speed * dt
        else:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, surface, *groups):
        super().__init__(*groups)
        self.image = surface
        image_width = self.image.size[0]
        image_height = self.image.size[1]
        self.rect = self.image.get_frect(center = (random.randint(0 + image_width, WINDOW_WIDTH - image_width), -image_height))
        self.spawn_time = pygame.time.get_ticks()
        self.direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(400, 500)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


# pygame setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True

PLAYER_SURF = pygame.image.load(join(IMAGES_PATH, "player.png")).convert_alpha()
STAR_SURF = pygame.image.load(join(IMAGES_PATH, "star.png")).convert_alpha()
LASER_SURF = pygame.image.load(join(IMAGES_PATH, "laser.png")).convert_alpha()
METEOR_SURF = pygame.image.load(join(IMAGES_PATH, "meteor.png")).convert_alpha()

METEOR_EVENT = pygame.event.custom_type()

pygame.time.set_timer(METEOR_EVENT, 500)

clock = pygame.Clock()

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(NUMBER_OF_STARS):
    Star(STAR_SURF, all_sprites)
    
player = Player(PLAYER_SURF, all_sprites)

def collisions():
    if pygame.sprite.spritecollide(player, meteor_sprites, True):
        print("dead")

    for laser in laser_sprites:
        if pygame.sprite.spritecollide(laser, meteor_sprites, True):
            laser.kill()

while running:
    dt = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == METEOR_EVENT:
            Meteor(METEOR_SURF, all_sprites, meteor_sprites)

    collisions()

    display_surface.fill("darkgray")
    all_sprites.update(dt)
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()