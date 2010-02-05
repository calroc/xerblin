#!/usr/bin/env python
from pickle import dumps, loads
'''
This is a simple Binary Tree implementation that uses tuples in such a
way as to permit "persistant" usage, i.e. all previous versions of the
btree datastructures are retained and available (provided you don't throw
them away yourself.)

It uses functional-style programming.

The empty tree is represented as an empty tuple.  Nodes are a tuple
consisting of a key, a value, and two (possible empty) sub-nodes for the
lower and higher branches of the tree.

This module defines the following functions:

    insert(node, key, value)

    get(node, key)

    delete(node, key)

Both insert() and delete() return a new tuple that is the result of
applying the operation to the existing node.  (And both get() and delete()
will raise KeyErrors if the key is not in the tree.)

Because of the way that insert() and delete() are written, only as much
of the tree is changed as necessary and the rest of it is reused. This
provides persistance without using up memory for each version of the
tree.

These functions are implemented recursively so they have the potential to
raise a RuntimeError if the maximum recursion depth is exceeded.  This
should only be a problem if used with very large trees.  To avoid this
issue you can use sys.setrecursionlimit(), but I think I might just
rewrite these to not use recursion.
'''


def insert(node, key, value):
    '''
    Return a tree with value stored under key. Replaces old value if any.
    '''
    if not node:
        return key, value, (), ()

    node_key, node_value, lower, higher = node

    if key < node_key:
        return node_key, node_value, insert(lower, key, value), higher

    if key > node_key:
        return node_key, node_value, lower, insert(higher, key, value)

    return key, value, lower, higher


def get(node, key):
    '''
    Return the value stored under key or raise KeyError if not found.
    '''
    if not node:
        raise KeyError, key

    node_key, value, lower, higher = node

    if key == node_key:
        return value

    n = lower if key < node_key else higher
    return get(n, key)


def delete(node, key):
    '''
    Return a tree with the value (and key) removed or raise KeyError if
    not found.
    '''
    if not node:
        raise KeyError, key

    node_key, value, lower, higher = node

    if key < node_key:
        return node_key, value, delete(lower, key), higher

    if key > node_key:
        return node_key, value, lower, delete(higher, key)

    # So, key == node_key, delete this node itself.

    # If we only have one non-empty child node return it.  If both child
    # nodes are empty return an empty node (one of the children.)
    if not lower:
        return higher
    if not higher:
        return lower

    # If both child nodes are non-empty, we find the highest node in our
    # lower sub-tree, take its key and value to replace (delete) our own,
    # then get rid of it by recursively calling delete() on our lower
    # sub-node with our new key.
    # (We could also find the lowest node in our higher sub-tree and take
    # its key and value and delete it. I only implemented one of these
    # two symmetrical options. Over a lot of deletions this might make
    # the tree more unbalanced.  Oh well.)
    next = lower
    while next[3]:
        next = next[3]
    key = next[0]
    value = next[1]

    return key, value, delete(lower, key), higher


# The above functions are the "core" functionality for dealing with this
# tuple-based persistant BTree datastructure.  The rest of this module is
# just helper functions and examples.


def items(node):
    '''
    Iterate in order over the (key, value) pairs in a tree.
    '''
    if not node:
        return

    key, value, lower, higher = node
    
    for kv in items(lower):
        yield kv
    
    yield key, value
    
    for kv in items(higher):
        yield kv


def _yieldBalanced(sorted_items):
    '''
    Recursive generator function to yield the items in a sorted sequence
    in such a way as to fill a btree in a balanced fashion.
    '''
    # For empty sequences do nothing.
    if not sorted_items:
        return

    # Find the index of the middle item (rounding down for even-length
    # sequences due to integer division.)
    i = len(sorted_items) / 2

    # Yield the middle item.
    yield sorted_items[i]

    # Shortcut in case len(items) == 1
    if not i:
        return 

    # Now recurse on lower and higher halves of the sequence.
    for low in _yieldBalanced(sorted_items[:i]):
        yield low
    for high in _yieldBalanced(sorted_items[i+1:]):
        yield high


def fillTree(node, items):
    '''
    Add the (key, value) pairs in items to a btree in a balanced way.

    You can balance a tree like so:

        tree = fillTree((), items(tree))

    This iterates through the tree and returns a new, balanced tree from
    its contents.
    '''
    for key, value in _yieldBalanced(sorted(items)):
        node = insert(node, key, value)
    return node


'''
Tuple-based persistent stack.
'''


def push(stack, *items):
    '''Push arguments onto a stack.'''
    for item in items:
        stack = item, stack # push
    return stack


def pop(stack, number):
    '''Pop number arguments from stack.'''
    for _ in range(number):
        item, stack = stack # pop
        yield item
    yield stack


def iterStack(stack):
    '''Iterate through the items on the stack.'''
    while stack:
        item, stack = stack
        yield item


def lenStack(stack):
    '''Return the number of items on the stack.'''
    return sum(1 for _ in iterStack(stack))


def pick_(stack, n):
    '''
    Find the nth item on the stack and duplicate it to TOS. (Pick with
    zero is the same as "dup".)
    '''
    if n < 0:
        raise ValueError
    s = stack
    while True:
        try:
            item, s = s
        except ValueError:
            raise IndexError
        n -= 1
        if n < 0:
            break
    return item, stack


'''
The first three functions defined in this module are used to build
"combo" commands in the UI.  There are corresponding commands in the
library (NewSeqWord, NewLoopWord, and NewBranchWord) that build tuples
with these functions as the first item in the tuple.  When applyFunc()
encounters these tuples the initial handler function is used to "run" the
other functions in the tuple.

The three functions are:

    handleSequence

    handleBranch

    handleLoop

The applyFunc() function is used by the handlers and the interpret()
function in xerblin.py to "run" commands on the interpreter.
'''


# Helper function factored out from handleBranch() and handleLoop().
def _popTOS(I):
    '''
    Pop the top item off the stack and return it with the
    modified interpreter
    '''
    (TOS, stack), dictionary = I
    return TOS, (stack, dictionary)


# These three following functions process the three kinds of combo-words.

def handleSequence(I, seq):
    '''
    Run a sequence and return the modified interpreter.
    '''
    for func in seq[1:]:
        I = applyFunc(I, func)
    return I


def handleBranch(I, branch):
    '''
    Check TOS and do one thing or another depending.
    '''
    TOS, I = _popTOS(I)
    func = branch[(not TOS) + 1] # i.e. True = 1; False = 2
    return applyFunc(I, func)


def handleLoop(I, loop):
    '''
    Check TOS and do body if it's true, repeat.
    '''
    while True:
        TOS, I = _popTOS(I)
        if not TOS:
            break
        I = handleSequence(I, loop)
    return I


def applyFunc(I, func):
    '''
    Given an interpreter and a function or combo-word tuple, apply the
    function or combo to the interpreter and return the modified
    interpreter.
    '''
    if isinstance(func, tuple):
        handler = func[0]
        I = handler(I, func)
    else:
        I = func(I)
    return I


'''
This module builds a Xerblin system out of purely "functional" parts.

An interpreter is represented by a two-tuple that holds a stack and a
dictionary.

The stack is a sort of "linked list" structure while the dictionary is a
BTree that maps string names to four kinds of entries:

    Functions - These must accept an interpreter, modify it somehow, and
        return the modified interpreter.  They are defined in the library
        module.

    Or, one of three kinds of tuple.  The kind of the tuple is indicated
    by its first member, which is a handler function, and the rest of the
    tuple consists in its body as indicated:

        (SEQUENCE HANDLER, func0, func1, func2)
        
        (BRANCH HANDLER, true_func, false_func)
        
        (LOOP HANDLER, func0, func1, func2)

    where any of the functions can be themselves SEQ, BRANCH, LOOP, or
    plain functions as described above.


Interpretation is done by means of an applyFunc(interpreter, function)
function that knows how to deal with the above combo-word tuples as well
as library word functions.
'''


# This is the main point of this module.  It implements the system with
# the help of the applyFunc() function.
def interpret(I, command):
    '''
    Given an interpreter and a string command, interpret that string on
    the interpreter and return the modified interpreter.
    '''
    for word in command.split():

        # Is it an integer?
        try:
            literal = int(word)
        except ValueError:

            # Is it a float?
            try:
                literal = float(word)
            except ValueError:

                # Is it a string literal?
                if word.startswith('"') and word.endswith('"'):
                    literal = word[1:-1]

                # Nope, it must be a command word.
                else:
                    # Interpret the word.
                    func = get(I[1], word)
                    I = applyFunc(I, func)
                    continue

        # A literal was found, push it onto the stack.
        I = (literal, I[0]), I[1]

    return I


# Library

# Mark the current namespace contents.
_existing = set(dir())
_existing.add('_existing')

# Stack chatter.

def dup(interpreter):
    '''
    "Duplicate" the top item on the stack.
    '''
    stack, dictionary = interpreter
    return (stack[0], stack), dictionary


def swap(interpreter):
    '''
    Reverse the order of the top two items on the stack.
    '''

    stack, dictionary = interpreter
    TOS, second, stack = pop(stack, 2)
    stack = push(stack, TOS, second)
    return stack, dictionary


def pick(interpreter):
    '''
    Takes a number from the stack, counts back that many items (starting
    from zero for the top item) and puts a "duplicate" of the item found
    on the top of the stack. (So pick with 0 on the stack is thte same as
    the command "dup".)
    '''
    stack, dictionary = interpreter
    TOS, stack = stack
    stack = pick_(stack, TOS)
    return stack, dictionary


def tuck(interpreter):
    '''
    Put a "duplicate" of the item on the top of the stack just under the
    second item on the stack. (I.e. top, second, top.)
    '''
    stack, dictionary = interpreter
    TOS, second, stack = pop(stack, 2)
    stack = push(stack, TOS, second, TOS)
    return stack, dictionary


def drop(interpreter):
    '''
    Remove the item on the top of the stack and discard it.
    '''
    stack, dictionary = interpreter
    return stack[1], dictionary


def over(interpreter):
    '''
    Put a "duplicate" of the second item down in the stack on the top of
    the stack. (I.e. second, top, second.)
    '''
    stack, dictionary = interpreter
    TOS, second, stack = pop(stack, 2)
    stack = push(stack, second, TOS, second)
    return stack, dictionary

# Programming words.

def lookup(interpreter):
    '''
    Given a name on the top of the stack, look up the named command in
    the dictionary and put it on the stack in place of the name.
    '''
    (name, stack), dictionary = interpreter
    word = get(dictionary, name)
    return (word, stack), dictionary


def inscribe(interpreter):
    '''
    Given a name string on the top of the stack and a "combo" command
    underneath it (see NewSeqWord, NewLoopWord, and NewBranchWord for how
    to make combo commands) "inscribe" the combo command into the
    dictionary under that name, replacing any previous command of that
    name.
    '''
    stack, dictionary = interpreter
    name, word, stack = pop(stack, 2)
    dictionary = insert(dictionary, name, word)
    return stack, dictionary


def NewSeqWord(interpreter):
    '''
    This command takes all the items on the stack and puts them into a
    tuple with the Sequence Handler function in front of them.

    The items on the stack should all be commands from the dictionary,
    either functions or combo commands.  You get these by using the
    "lookup" command on the names of the functions you want.

    Put the first command to run on the stack first, then the second, and
    so on, so that the last item to run is on the top of the stack when
    you run this command.
    '''
    stack, dictionary = interpreter
    words = tuple(reversed(list(iterStack(stack))))
    seq = (handleSequence,) + words
    return (seq, ()), dictionary


def NewLoopWord(interpreter):
    '''
    This command takes all the items on the stack and puts them into a
    tuple with the Loop Handler function in front of them.

    A Loop consumes the top item on the stack, then depending on it's
    "truth" either runs the commands in its tuple and repeats if it's
    true or stops looping altogether if it's false.

    Put the first command to run on the stack first, then the second, and
    so on, so that the last item to run is on the top of the stack when
    you run this command.
    '''
    stack, dictionary = interpreter
    words = tuple(reversed(list(iterStack(stack))))
    loop = (handleLoop,) + words
    return (loop, ()), dictionary


def NewBranchWord(interpreter):
    '''
    Create a new Branch command word.  A branch consumes the top item on
    the stack and does one of two things depending on its "truth" value.
    Unlike Loops and Sequences which use all the items on the stack,
    Branch commands only take the top two items. The item on the top of
    the stack should be a function to use in case of "true" and the
    second should be a function to use for "false".
    '''
    stack, dictionary = interpreter
    true, false, stack = pop(stack, 2)
    branch = (handleBranch, true, false)
    stack = push(stack, branch)
    return stack, dictionary


# Math words.

def add(interpreter):
    '''
    Add the top two items on the stack and replace them with the sum.
    '''
    stack, dictionary = interpreter
    a, b, stack = pop(stack, 2)
    return (a + b, stack), dictionary


def sub(interpreter):
    '''
    Replace the top two items on the stack with the result of subtracting
    the top item from the second item.
    '''
    stack, dictionary = interpreter
    a, b, stack = pop(stack, 2)
    return (b - a, stack), dictionary


def mul(interpreter):
    '''
    Replace the top two items on the stack with the result of multiplying
    them together.
    '''
    stack, dictionary = interpreter
    a, b, stack = pop(stack, 2)
    return (a * b, stack), dictionary


# Pickling words.

def pickle(interpreter):
    '''
    Convert the current interpreter to a portable text format (called a
    "pickle".)
    '''
    stack, dictionary = interpreter
    p = dumps(interpreter)
    return (p, stack), dictionary


def unpickle(interpreter):
    '''
    Take a string "pickle" portable text representation of an interpreter
    and replace the current interpreter with it.
    '''
    stack = interpreter[0]
    return loads(stack[0])


# System words

def rebalance(interpreter):
    '''
    This "rebalances" a dictionary.  It makes it more efficient to access
    commands in the dictionary if you've added a lot of new ones.

    It's a good idea to use this command before creating a pickle to
    save so that the saved pickle's dictionary is already balanced.
    '''
    stack, dictionary = interpreter
    dictionary = fillTree((), items(dictionary))
    return stack, dictionary


def view(interpreter):
    '''
    Pretty print the interpreter to stdout.
    '''
    from pprint import pprint as p
    p(interpreter)
    return interpreter


def listwords(interpreter):
    '''
    Print the list of words in the dictionary to stdout.
    '''
    stack, dictionary = interpreter
    for name, func in items(dictionary):
        print name
    print
    return interpreter


# Now extract all the library functions we just defined.
_word_names = set(dir()) - _existing


# Pull words from this dict.
words = [
    (name, function)
    for name, function in locals().items()
    if name in _word_names
    ]


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
        ))
##    print htmlTransform(I)
    P(I[0])

    while True:
        try:
            command = raw_input('> ')
        except EOFError:
            print
            break
        I = interpret(I, command)
        P(I[0])

