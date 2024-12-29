from settings import *

class Timer:
    def __init__(self, duration, event_type: int = None, repeat = False, auto_start = False):
        self.duration = duration
        self.event_type = event_type
        self.repeat = repeat
        self.active = False
        self.start_time = 0

        if auto_start:
            self.activate()

    def __bool__(self):
        return self.active

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
            if self.event_type:
                pygame.event.post(pygame.Event(self.event_type))
            self.deactivate()