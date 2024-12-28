from settings import *

def import_image(*path, format = "png", alpha = True):
    full_path = join(*path) + f".{format}"
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path):
    frames = []
    for root, _, files in walk(join("images", "player")):
        for file in sorted(files, key = lambda name: int(name.split('.')[0])):
            full_path = join(root, file)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames