from threading import Thread
import random
import time

class RandomWork:
    def start(self):
        self.thr=Thread(target=self.easywork,)
        self.flag=True
        self.thr.start()

    def easywork(self):
        while self.flag:
            self.r1=random.randint(2,10)
            self.r2=random.randint(1,10)
            self.r3=random.random()

            for i in range(1,self.r1):
                time.sleep(0.05)
                self.r3=self.r3*(self.r3+self.r2)%self.r2
                print(self.r3)

    def end(self):
        self.flag=False
        self.thr.join()
