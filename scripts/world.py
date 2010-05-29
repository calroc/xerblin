#!/usr/bin/env python
'''
This script defines a proof-of-concept frame for interacting with a
xerblin interpreter.
'''
import pickle, pprint, StringIO
from xerblin.btree import items
from xerblin.world import HistoryListWorld, view0


if __name__ == "__main__":

    # Create a world with the basic view function.
    w = HistoryListWorld(view0)

    # For convenience print out the commands in the dictionary at
    # startup.
    dictionary = w.getCurrentState()[1]
    print ' '.join(name for name, value in items(dictionary))
    print

    # Drop into an event loop.
    while True:
        
        try:
            # Get a command and split it up.
            command = raw_input('> ').split()
        
        except EOFError:
            # User is done, quit.
            break
        
        # Run the command, the World object handles all the details for
        # us.
        w.step(command)

##
## Example run:
##
## ()
##
## NewBranchWord NewLoopWord NewSeqWord add drop dup inscribe listwords
## lookup mul over pick pickle rebalance sub swap tuck unpickle view
##
## > 23 18
## (18, (23, ()))
##
## > over
## (23, (18, (23, ())))
##
## > over
## (18, (23, (18, (23, ()))))
##
## > swap
## (23, (18, (18, (23, ()))))
##
## > sub
## (-5, (18, (23, ())))
##
## > drop
## (18, (23, ()))
##
## > over over sub
## (5, (18, (23, ())))
##
## > drop drop drop
## ()
##
## > 
##
##
