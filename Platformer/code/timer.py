from settings import *

class Timer:
    def __init__(self, duration, func = None, repeat = None, autostart = False):
        self.duration = duration
        self.func = func
        self.repeat = repeat
        self.autostart = autostart
        self.active = self.autostart
        self.start_time = 0

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()
    
    def deactivate(self):
        self.active = False
        self.start_time = 0
    
    def update(self):
        curr_time = pygame.time.get_ticks()
        if self.active and curr_time - self.start_time >= self.duration:
            if not self.autostart:
                self.deactivate()