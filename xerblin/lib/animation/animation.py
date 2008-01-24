#!/usr/bin/env python
from sched import scheduler
from time import time, sleep


class TimeFrame:

    def __init__(self, frame_rate=30):
        self.scheduler = scheduler(getTimer(), sleep)
        self.interval = 1.0 / frame_rate

    def addCall(self, delay, func, *args):
        return self.scheduler.enter(delay, 1, func, args)


class Delta:

    def __init__(self, duration, initial, delta):
        self.duration = duration
        self.initial = initial
        self.delta = delta

    def attach(self, timeframe):
        return [
            timeframe.addCall(delay, self.step, coord)
            for delay, coord in self.yieldCoords(timeframe.interval)
            ]

    def yieldCoords(self, interval):
        t = delta = 1.0 / (self.duration / interval)
        n = interval
        while t < 1.0:
            yield n, self.warp(t)
            t += delta
            n += interval

    def warp(self, t):
        return t**3 * self.delta + self.initial

    def step(self, coord):
        print int(round(coord))


class QuadraticDelta(Delta):
    def warp(self, t):
        return t**2 * self.delta + self.initial


def getTimer():
    now = time()
    return lambda : time() - now


if __name__ == "__main__":
    tf = TimeFrame()
##    d = Delta(7.0, 23, 45)
##    R = d.attach(tf)
#    tf.scheduler.run()
##    data = zip(*[(t, c[0]) for t, _, _, c in R])

    from Tkinter import *

    c = Canvas(width=640)
    c.pack(expand=True, fill=BOTH)

    i = c.create_oval(10, 10, 30, 30, fill='red')

    def moveIt(coord):
        x0, y0 = coord - 10, 10
        x1, y1 = coord + 10, 30
        c.coords(i, x0, y0, x1, y1)
        c.update_idletasks()

    class CDelta(Delta):
        def step(self, coord):
            moveIt(coord)

    CDelta(3.5, 20, 200).attach(tf)

    c.after(2500, tf.scheduler.run)

    c.mainloop()
