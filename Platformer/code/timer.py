from settings import *

class Timer:
    def __init__(self, duration, func = None, repeat = False, auto_start = False):
        self.duration = duration
        self.func = func
        self.repeat = repeat
        self.active = False
        self.start_time = 0

        if auto_start:
            self.activate()

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()
    
    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()
    
    def update(self):
        curr_time = pygame.time.get_ticks()
        if self.active and curr_time - self.start_time >= self.duration:
            if self.func:
                self.func()
            self.deactivate()