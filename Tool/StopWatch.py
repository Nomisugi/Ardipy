import time

class StopWatch():
    def __init__(self, name=None):
        self.name = name
        self.start_time = 0
        self.stop_time = 0

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.stop_time = time.perf_counter()
        tm = self.stop_time - self.start_time
        return(round( tm, 4))

    def clear(self):
        self.start_time = 0

    def isName(self):
        return self.name


if __name__ == "__main__":
    sw1 = StopWatch("A")
    sw2 = StopWatch("B")    
    sw1.start()
    time.sleep(1)

    print(sw1.stop())
    sw2.start()
    for i in range(1000000):
        i=i+0.01
    print(sw1.name + ":" + str(sw1.stop()))
    print(sw2.name + ":" + str(sw2.stop()))
    
