#!/usr/bin/env python
from xerblin.base import interpret
from xerblin.btree import fillTree
from xerblin.library import words


def make_interpreter():
    dictionary = fillTree((), words)
    stack = ()
    I = stack, dictionary
    return I


if __name__ == '__main__':
    from pprint import pprint as P

    I = make_interpreter()

    I = interpret(I, (
        '"dup" lookup NewSeqWord "gary" inscribe '
        
        '"gary" lookup '
        'NewSeqWord '
        '"barry" '
        'inscribe '
        
        '23 gary '
        ).split())
##    print htmlTransform(I)
    P(I[0])

    while True:
        try:
            command = raw_input('> ').split()
        except EOFError:
            print
            break
        I = interpret(I, command)
        P(I[0])

