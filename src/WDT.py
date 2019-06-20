import time

class Watch_Dog:
    def __init__(self,delay=30):
        self.delay=delay
        self.timestamp = int(time.time()) + self.delay

    def set_time(self):
        self.timestamp=int(time.time())+self.delay


    def time_out(self):
        now=int(time.time())
        if now>=self.timestamp:
            return True
        else:
            return False


