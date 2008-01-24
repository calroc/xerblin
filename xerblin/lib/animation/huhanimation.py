#!/usr/bin/env python
from sched import scheduler
from time import time, sleep


class TimeFrame:

    def __init__(self, frame_rate=3):
        self.scheduler = scheduler(getTimer(), sleep)
        self.interval = 1.0 / frame_rate

    def addCall(self, delay, func, *args):
        return self.scheduler.enter(delay, 1, func, args)


class Delta:

    def __init__(self, duration, begin, delta):
        self.duration = duration
        self.begin = begin
        self.delta = delta

    def attach(self, timeframe):
        interval = timeframe.interval
        return [
            timeframe.addCall(d, self.step, ())
            for d in self.yieldDelays(interval)
            ]

    def yieldDelays(self, interval):
        n = self.duration / interval


def getTimer():
    now = time()
    return lambda : time() - now


if __name__ == "__main__":

    n = 23
