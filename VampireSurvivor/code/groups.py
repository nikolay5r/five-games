from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        ground_sprites = [obj for obj in self if hasattr(obj, "ground")]
        object_sprites = [obj for obj in self if not hasattr(obj, "ground")]

        for ground in ground_sprites:
            self.display_surface.blit(ground.image, ground.rect.topleft + self.offset)

        for obj in sorted(object_sprites, key = lambda sprite: sprite.rect.centery):
            self.display_surface.blit(obj.image, obj.rect.topleft + self.offset)