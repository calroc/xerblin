#!/usr/bin/env python
from pprint import pprint as P
from xerblin.base import interpret
from xerblin.btree import fillTree
from xerblin.library import words


def make_interpreter():
    dictionary = fillTree((), words)
    stack = ()
    I = stack, dictionary
    return I
#
#   Obviously this could just be:
#   return (), fillTree((), words)
#   ...but c'mon.


if __name__ == '__main__':

    I = make_interpreter()

    I = interpret(I, (
        '"dup" lookup NewSeqWord "gary" inscribe '
        
        '"gary" lookup '
        'NewSeqWord '
        '"barry" '
        'inscribe '
        
        '23 gary '
        ).split())

    P(I[0])

    while True:
        try:
            command = raw_input('> ').split()
        except EOFError:
            print
            break
        I = interpret(I, command)
        P(I[0])

