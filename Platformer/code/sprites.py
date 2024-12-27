from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_frect(center = pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.setup_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_frect(center = pos)

    def setup_frames(self):
        for root, _, files in walk(join("images", "player")):
            self.frames = [pygame.image.load(join(root, file)) for file in files]