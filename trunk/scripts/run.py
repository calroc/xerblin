#!/usr/bin/env python
from pprint import pprint as P
from xerblin.base import interpret
from xerblin.btree import fillTree
from xerblin.library import words


ROOT = (), fillTree((), words)


if __name__ == '__main__':

    I = interpret(ROOT, (
        '"dup" lookup NewSeqWord "gary" inscribe '
        
        '"gary" lookup '
        'NewSeqWord '
        '"barry" '
        'inscribe '
        
        '23 gary '
        ).split())

    print_stack = lambda: P(I[0])

    while True:
        print_stack()
        try:
            command = raw_input('> ').split()
        except EOFError:
            print_stack()
            print
            break
        I = interpret(I, command)

