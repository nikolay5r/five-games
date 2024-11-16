from settings import *

PLAYER_SURFACE_FRAMES = {
    "down": tuple(pygame.image.load(join(PLAYER_PATH, "down", f"{i}.png")) for i in range(4)),
    "up": tuple(pygame.image.load(join(PLAYER_PATH, "up", f"{i}.png")) for i in range(4)),
    "left": tuple(pygame.image.load(join(PLAYER_PATH, "left", f"{i}.png")) for i in range(4)),
    "right": tuple(pygame.image.load(join(PLAYER_PATH, "right", f"{i}.png")) for i in range(4))
}