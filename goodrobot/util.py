from time import clock,time

def heartBeat(base, step,interval):
    quit = False
    currentTime = 0.0
    accumulator = 0.0
    accTime = 0.0
    while not quit:
        delta = time() - currentTime
        currentTime += delta
        print "Delta %f" % delta
        accumulator = accumulator + delta
        while (accumulator >= interval):
            step(accTime, interval)
            accTime = accTime + interval
            accumulator = accumulator - interval

        quit = base(currentTime,delta)



    
if __name__ == "__main__":
    import pygame

    class testBeat:
        def __init__(self):
            self.clock = pygame.time.Clock()
            

        def interval(self, time, step):
            print "interval: The time is %f and I my step is %f" % (time,step)

        def base(self, time,step):
            print "base: The time is %f and I my step is %f" % (time,step)
            self.clock.tick(9)
            return False

        def start(self):
            heartBeat(self.base, self.interval, 100)

    t = testBeat()
    t.start()

    
