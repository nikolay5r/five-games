from settings import *

def import_image(*path, format = "png", alpha = True):
    full_path = join(*path) + f".{format}"
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path):
    frames = []
    for root, _, files in walk(join(*path)):
        for file in sorted(files, key = lambda name: int(name.split('.')[0])):
            full_path = join(root, file)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames

def import_audio(*path) -> dict[str, pygame.mixer.Sound]:
    audio_dict = {}
    for root, _, files in walk(join(*path)):
        for file in files:
            full_path = join(root, file)
            audio_dict[file.split('.')[0]] = pygame.mixer.Sound(full_path)
    
    return audio_dict