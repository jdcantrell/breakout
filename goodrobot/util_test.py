import util
import time
import pygame
import unittest

class utilTests(unittest.TestCase):
    def testHeartBeat(self):
        class testBeat:
            def __init__(self):
                self.clock = pygame.time.Clock()
                self.ticks = 0
                self.intervalTick = 0
                
            def interval(self, time, step):
                self.intervalTick += 1

            def base(self, t, dt, intLatency):
                self.ticks += 1
                self.clock.tick(60)
                if (time.time() - self.startT) >= .15:
                    return True
                return False

            def start(self):
                self.startT = time.time()
                util.heartBeat(self.base, self.interval, .01)
                end = time.time()
                print "Run Time: %f" % (end - self.startT)
                return (self.ticks, self.intervalTick)

        t = testBeat()
        self.assertEqual(t.start(), (10, 14))

if __name__ == "__main__":
    unittest.main()
