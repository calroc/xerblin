#!/usr/bin/env python
'''

This is a basic, trivial text mode script to run commands on an
interpreter.  It's mostly useful as a demonstration of the xerblin system
as it doesn't do anything fancy like recording history.

'''

# We'll use Python's standard "Pretty Print" module to represent our
# stack after each command.
from pprint import pprint as P

# The interpret() function is the core interface to the system.  You
# don't need to import any of the base functionality but this, you can
# pass, e.g. ((), ()), to the interpret() function as the interpreter.
# You won't be able to run any commands (but you could store number and
# string literals) because there are none to run in the dictionary.
from xerblin.base import interpret

# We'll use the fillTree() function from the btree module to build a
# dictionary of command words from the words exported by the library
# module.
from xerblin.btree import fillTree
from xerblin.library import words


# We create a root interpreter to serve as the starting state for our
# interaction with the xerblin system.  (Note that, because this data
# structure is built entirely from tuples and other immutable datatypes,
# it is essentially a constant. It can be traversed, and new data
# structures can be built from it or by using its sub-parts, but it
# cannot be changed, other than to delete it.)
ROOT = (), fillTree((), words)


if __name__ == '__main__':

    # Build an interpreter out of the ROOT interpreter and a funky
    # initialization command.
    I = interpret(ROOT, (

        # This is an example of how to create new commands out of
        # existing commands.
        #
        # You use strings and the 'lookup' command to get command
        # functions on the stack...
        
        '"dup" lookup '
        
        # ...then call 'NewSeqWord' to turn the stack of functions into a
        # new sequence function...
        
        'NewSeqWord '

        # ...then you give it a name string and call 'inscribe' to
        # inscribe the new word into the dictionary under that name.
        
        '"gary" inscribe '


        # Now you can 'lookup' the new sequential command just like the
        # others.
        
        '"gary" lookup '

        # And use it to create additional new words.
        'NewSeqWord "sammy" inscribe '
        
        # If you put 23 onto the stack and call 'gary' it will 'dup' the
        # number and you'll have two 23's on the stack.
        '23 gary '

        # In case you didn't know, Python will concatenate string
        # literals that have no intervening symbols between them. Here we
        # are closing the parenthesis we opened above that essentially
        # allowed these interspersed string literals and comments to look
        # like one long string literal to the python interpreter.
        #
        # We call the split() method of this string to give us a nice
        # list of string commands to pass to the interpret() function.
        ).split())


    # This is a convenience function to print out the current stack.
    # Thanks to Python's dynamic scoping rules the I variable will pick
    # up the current value of I each time through the loop below.
    print_stack = lambda: P(I[0])

    # Drop into an infinite loop.
    while True:

        # Display the stack to the user.
        print_stack()

        try:
            # Read a command from the user.
            command = raw_input('> ').split()
        
        except EOFError:
            # The user's done, print the stack and exit.
            print_stack()
            print
            break

        # Here is the heart of the system. Executed the command against
        # the current state, and replace the current state with the
        # results.
        I = interpret(I, command)

        # This is where we can store the previous states in some sort of
        # history (rather than simply discarding them to the garbage
        # collector as is done here.)
        # We could use a simple list, or a Python pickle serialization
        # object.

