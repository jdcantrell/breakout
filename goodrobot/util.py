from time import clock,time

def heartBeat(base, step,interval):
    quit = False
    currentTime = time()
    accumulator = 0.0
    accTime = 0.0
    while not quit:
        delta = time() - currentTime
        currentTime += delta
        accumulator = accumulator + delta
        while (accumulator >= interval):
            step(accTime, interval)
            accTime = accTime + interval
            accumulator = accumulator - interval

        quit = base(currentTime, delta, accumulator)
