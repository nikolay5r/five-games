import pygame 
from os.path import join 
from os import walk
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720 
TILE_SIZE = 64

PLAYER_PATH = join("images", "player")
ENEMIES_PATH = join("images", "enemies")
GUN_PATH = join("images", "gun")