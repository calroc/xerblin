from xerblin import ExecutableWord
from xerblin.base import BracketedExecuteWord
from xerblin.util.stackcheckers import StackLen, StackType, NUMBER_TYPES
from xerblin.lib.animation.animation import (
    TimeFrame,
    Delta,
    ComposeDelta,
    CubicDelta,
    QuadraticDelta,
    SineDelta,
    CosineDelta,
    )


# * timeframe
# delta
# attach
# run


class timeframe(
    StackLen(1),
    StackType(0, NUMBER_TYPES),
    ExecutableWord
    ):
    '''
    Create a TimeFrame object with a given framerate (in fps.)
    '''
    def execute(self, stack):
        framerate = stack[0]
        tf = TimeFrame(framerate)
        stack[0] = tf


class cubicdelta(
    StackLen(3),
    StackType(0, NUMBER_TYPES),
    StackType(1, NUMBER_TYPES),
    StackType(2, NUMBER_TYPES),
    ExecutableWord
    ):
    '''
    '''

    _delta_class = CubicDelta

    def execute(self, stack):
        duration, initial, delta = stack[2::-1]
        D = self._delta_class(duration, initial, delta)
        stack[:3] = [D]

class quadraticdelta(cubicdelta):
    _delta_class = QuadraticDelta

class sinedelta(cubicdelta):
    _delta_class = SineDelta

class cosinedelta(cubicdelta):
    _delta_class = CosineDelta


class attach(
    StackLen(3),
    StackType(0, ExecutableWord),
    StackType(1, TimeFrame),
    StackType(2, (Delta, ComposeDelta)),
    ExecutableWord
    ):
    '''
    Given a Delta, a TimeFrame, and an ExecutableWord on the stack, attach
    the ExecutableWord to the TimeFrame via Delta.
    '''
    def execute(self, stack):
        D, tf, word = stack[2::-1]
        def f(*args):
            BracketedExecuteWord([list(args)], word)
        D.attach(f, tf)
        del stack[:3]


class run(
    StackLen(1),
    StackType(0, TimeFrame),
    ExecutableWord
    ):
    '''
    '''
    def execute(self, stack):
        stack[0].scheduler.run()


