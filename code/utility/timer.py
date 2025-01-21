import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.pause_time = None
        self.unpaused_time = 0.0
        self.paused_time = 0.0
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True

    def pause(self):
        if self.running:
            self.unpaused_time += time.time() - self.start_time
            self.pause_time = time.time()
            self.running = False

    def resume(self):
        if not self.running:
            if self.pause_time is not None:
                self.paused_time += time.time() - self.pause_time
            self.start_time = time.time()
            self.running = True

    def reset(self):
        self.start_time = None
        self.pause_time = None
        self.unpaused_time = 0.0
        self.paused_time = 0.0
        self.running = False

    def get_unpaused_time(self):
        if self.running:
            return self.unpaused_time + (time.time() - self.start_time)
        return self.unpaused_time

    def get_paused_time(self):
        if not self.running and self.pause_time is not None:
            return self.paused_time + (time.time() - self.pause_time)
        return self.paused_time
    
    def get_total_time(self):
        return self.get_paused_time() + self.get_unpaused_time()
