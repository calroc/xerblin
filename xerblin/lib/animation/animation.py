#!/usr/bin/env python
from sched import scheduler
from time import time
from math import sin, pi, cos, ceil
import Tkinter # For Tkscheduler.


class Tkscheduler(scheduler):
    '''
    A scheduler that plays well with Tkinter mainloop by using after() to
    delay instead of sleep() or something similar.
    '''

    _tk = Tkinter._default_root or Tkinter.Tk()

    def run(self):
        q = self.queue
        while q:
            time, priority, action, argument = q[0]
            now = self.timefunc()
            if now < time:
                self._tk.after(int(round(1000 * (time - now))), self.run)
                break
            del q[0]
            void = action(*argument)
            self._tk.update_idletasks()


class TimeFrame:
    '''
    Basically a sched.scheduler object tied to a framerate.  Used with a
    Delta or ComposeDelta object to schedule a function to be called with
    the intermediate values generated by the deltas.
    '''

    def __init__(self, frame_rate=30):
        '''
        frame_rate is in frames per second.
        '''
        self.scheduler = Tkscheduler(getTimer(), None)
        self.interval = 1.0 / frame_rate

    def addCall(self, delay, func, *args):
        return self.scheduler.enter(delay, 1, func, args)


class Delta:
    '''
    Take a parameter from 0.0 => 1.0 over a duration in seconds.  The
    parameter is passed through the warp() method to return the actual
    result.  The default warp() method is the identity function, i.e.
    "do nothing", it returns 0.0 => 1.0.

    You use the attach() method to connect a function to a TimeFrame
    object so that it will be called at the right times with the
    transformed parameter.
    '''

    def __init__(self, duration):
        self.duration = duration

    def attach(self, function, timeframe):
        return [
            timeframe.addCall(delay, function, coord)
            for delay, coord in self.yieldCoords(timeframe.interval)
            ]

    def yieldCoords(self, interval):
        t = 0
        delta = 1.0 / (self.duration / interval)
        n = interval
        while t < 1.0:
            yield n, self.warp(t)
            t += delta
            n += interval
        n += interval / 2.0
        yield n, self.warp(1.0)

    def warp(self, t):
        return t

    def __mul__(self, other):
        result = ComposeDelta(self)

        if isinstance(other, Delta):
            result.addDelta(other)

        elif isinstance(other, ComposeDelta):
            result *= other

        else:
            raise ValueError

        return result


class ComposeDelta:

    def __init__(self, *deltas):
        # All initial deltas are assumed to have 0 starting offset time.
        self.deltas = list(deltas)
        self.delta_offsets = dict((delta, 0.0) for delta in deltas)

    def addDelta(self, delta, offset=0.0):
        self.deltas.append(delta)
        self.delta_offsets[delta] = offset

    def collectParameters(self, interval):

        # Create CoordPullers for each delta.
        sub_coords = []
        for delta in self.deltas:

            offset = self.delta_offsets[delta]

            # Make a dict of offset-adjusted delays mapped to coords.
            D = dict(
                (delay + offset, coord)
                for delay, coord in delta.yieldCoords(interval)
                )

            # Create the CoordPuller.
            cp = CoordPuller(D)

            sub_coords.append(cp)

        # Build a sorted list of all delays appearing in the CoordPullers.
        delays = set()
        for cp in sub_coords:
            delays.update(cp.D)
        delays = sorted(delays)

        # Iterate through them and pull out tuples of coordinates.
        for delay in delays:
            yield delay, tuple(cp(delay) for cp in sub_coords)

    def attach(self, function, timeframe):
        for delay, args in self.collectParameters(timeframe.interval):
            timeframe.addCall(delay, function, *args)

    def __mul__(self, other):
        result = ComposeDelta(*self.deltas)
        result.delta_offsets.update(self.delta_offsets)

        if isinstance(other, Delta):
            result.addDelta(other)

        elif isinstance(other, ComposeDelta):
            result *= other

        else:
            raise ValueError

        return result

    def __imul__(self, other):
        if isinstance(other, Delta):
            self.addDelta(other)

        elif isinstance(other, ComposeDelta):
            self.deltas.extend(other.deltas)
            self.delta_offsets.update(other.delta_offsets)

        else:
            raise ValueError

        return self


class CoordPuller:

    def __init__(self, D):
        self.D = D
        self.least = min(D)
        self.lower = D[self.least]

        # Note that self.current technically doesn't need to be defined
        # here because __call__() will always be called with n = self.least
        # before ever being called with n > self.least, so that will
        # guarantee that self.current will exist before being accessed.

    def __call__(self, n):
        # n will start at or below self.least, and thereafter only increase.

        try:
            coord = self.D[n]

        except KeyError:
            if n < self.least:
                coord = self.lower
            else:
                coord = self.current
        else:
            self.current = coord

        return coord


class CubicDelta(Delta):

    def __init__(self, duration, initial, delta):
        self.duration = duration
        self.initial = initial
        self.delta = delta

    def warp(self, t):
        return t**3 * self.delta + self.initial


class QuadraticDelta(CubicDelta):
    def warp(self, t):
        return t**2 * self.delta + self.initial


class SineDelta(CubicDelta):
    def warp(self, t):
        return sin(2 * pi * t) * self.delta + self.initial


class CosineDelta(CubicDelta):
    def warp(self, t):
        return cos(2 * pi * t) * self.delta + self.initial


def getTimer():
    now = time()
    return lambda : time() - now


if __name__ == "__main__":
    from Tkinter import *
    from xerblin.lib.widgets.widgetwrapper import MakeViewer, ListModel

    t = .5 # 3.8

    X, Y, D = 320, 200, 145
    cd = SineDelta(t, X, -D) * CosineDelta(t, Y, D)

    bx0, by0, bx1, by1 = 40, 40, 60, 50
    CD = (
        CubicDelta(t, bx1, 230) *
        QuadraticDelta(t, by1, 160) *
        CubicDelta(t, bx0, 150) *
        QuadraticDelta(t, by0, 120)
        )

    c = Canvas(width=640, height=480)
    c.pack(expand=True, fill=BOTH)

    o = MakeViewer('Demo "Zooming" Window', ListModel())

    c.create_line(X, 10, X, 470)
    i = c.create_oval(
        X - 10,
        Y + D - 10,
        X + 10,
        Y + D + 10,
        fill='red',
        )
    b = c.create_rectangle(bx0, by0, bx1, by1)

    _f = lambda n: int(round(n))

    def moveIt(x, y):
        x, y = map(_f, (x, y))
        x0, y0 = x - 10, y - 10
        x1, y1 = x + 10, y + 10
        c.coords(i, x0, y0, x1, y1)
        c.update_idletasks()

    def zoom(x0, y0, x1, y1):
        x0, y0, x1, y1 = map(_f, (x0, y0, x1, y1))
        c.coords(b, x0, y0, x1, y1)
        c.update_idletasks()

    def wtfwow(x0, y0, x1, y1):
        o.stack.insert(0, (x0, y0, x1, y1))
        o.interpret('setGeometry')

    tf = TimeFrame(18)

    def runme(event=None):
        cd.attach(moveIt, tf)
        CD.attach(zoom, tf)
        CD.attach(wtfwow, tf)
        tf.scheduler.run()

    c.bind("<Button-1>", runme)

    c.mainloop()