# Example file showing a basic pygame "game loop"
import pygame
from os.path import join
import random

IMAGES_PATH, AUDIO_PATH, FONTS_PATH = join("assets", "images"), join("assets", "audio"), join("assets", "fonts")
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
NUMBER_OF_STARS = 30
FONT_SIZE, FONT_PADDING = 40, 20

class Player(pygame.sprite.Sprite):
    def __init__(self, surface, *groups):
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)

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
            LASER_SOUND.play()
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
        self.mask = pygame.mask.from_surface(self.image)
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
        self.original_surface = surface
        self.image = surface
        image_width = self.image.size[0]
        image_height = self.image.size[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_frect(center = (random.randint(0 + image_width, WINDOW_WIDTH - image_width), -image_height))
        self.mask = pygame.mask.from_surface(self.image)

        self.direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(400, 500)
        self.rotation = 0
        self.rotation_speed = random.randint(50, 100)

    def update(self, dt):
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

        self.rect.center += self.direction * self.speed * dt

        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surface, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)


class Animation(pygame.sprite.Sprite):
    def __init__(self, frames, pos, *groups):
        super().__init__(*groups)
        self.frame_index = 0
        self.frames = frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        self.animation_speed = 25

    def update(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()
            

def collisions():
    if pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask):
        DAMAGE_SOUND.play()
        print("dead")

    for laser in laser_sprites:
        collision_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True, pygame.sprite.collide_mask)
        if collision_sprites:
            Animation(EXPLOSION_FRAMES, laser.rect.midtop, all_sprites)
            EXPLOSION_SOUND.play()
            laser.kill()

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = FONT.render(str(current_time), True, (240, 240, 240))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - FONT_PADDING))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(20, 10).move(0, -5), 5, 10)

# pygame setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True

#import
PLAYER_SURF = pygame.image.load(join(IMAGES_PATH, "player.png")).convert_alpha()
STAR_SURF = pygame.image.load(join(IMAGES_PATH, "star.png")).convert_alpha()
LASER_SURF = pygame.image.load(join(IMAGES_PATH, "laser.png")).convert_alpha()
METEOR_SURF = pygame.image.load(join(IMAGES_PATH, "meteor.png")).convert_alpha()
EXPLOSION_FRAMES = tuple(pygame.image.load(join(IMAGES_PATH, "explosion", f"{i}.png")) for i in range(21))

FONT = pygame.font.Font(join(FONTS_PATH, "Oxanium-Bold.ttf"), 40)

EXPLOSION_SOUND = pygame.mixer.Sound(join(AUDIO_PATH, "explosion.wav"))
LASER_SOUND = pygame.mixer.Sound(join(AUDIO_PATH, "laser.wav"))
DAMAGE_SOUND = pygame.mixer.Sound(join(AUDIO_PATH, "damage.ogg"))
GAME_MUSIC = pygame.mixer.Sound(join(AUDIO_PATH, "game_music.wav"))
GAME_MUSIC.play(-1)

METEOR_EVENT = pygame.event.custom_type()

pygame.time.set_timer(METEOR_EVENT, 500)

clock = pygame.Clock()

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(NUMBER_OF_STARS):
    Star(STAR_SURF, all_sprites)
    
player = Player(PLAYER_SURF, all_sprites)

while running:
    dt = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == METEOR_EVENT:
            Meteor(METEOR_SURF, all_sprites, meteor_sprites)

    collisions()

    display_surface.fill("#3a2e3f")
    display_score()
    all_sprites.draw(display_surface)

    all_sprites.update(dt)
    pygame.display.update()

pygame.quit()