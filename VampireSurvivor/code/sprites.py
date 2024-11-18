from settings import *

class TileSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        pos = pygame.math.Vector2(pos)
        pos *= TILE_SIZE
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)