#!/usr/bin/env python
"""
    Xerblin - A User Interface
    Copyright (C) 2004, 2005, 2006 Simon Forman.

    Xerblin is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA



This module implements the base of the Xerblin demo system.

The Interpreter class is the engine of the whole system.
ExecutableWord - class of active objects.

"""


import sys    #we'll need sys for error reporting below.
from xerblin.messaging import ListModel, log


class SimpleInterpreter:

    """
    Interpreter - This class organizes a Stack of data items and
    Dictionary of active objects (ExecutableWords) that act on the
    data items to form the Level 0 core of the Xerblin system.

    The Interpreter class provides several ways to execute the
    words in the Dictionary on the items in the Stack.

    Instance Variables:

        stack : a list of data items
        dictionary : a dictionary of ExecutableWords

    Public Methods:

        interpret - Interpret a string containing one or more commands.
        execute_name - Lookup and execute a single command (given as a string.)
        execute_word - Execute a given ExecutableWord object.

    """

    def __init__(self, stack=None, dictionary=None):
        """
        The default values for the stack and dictionary are an empty
        list and dictionary respectively.
        Optionally, you can pass a populated list or dictionary to
        the constructor. The only restriction is on the dictionary,
        the keys must all be strings and the values must all be
        instances of ExecutableWord.
        """

        if stack is None: stack = ListModel()
        if dictionary is None: dictionary = {}

        dictionary.setdefault('self', SelfWord(self))

        self.stack = stack
        self.dictionary = dictionary

    def interpret(self, command_string):
        """
        Given a command string, break it into whitespace-delimited
        commands and execute them one after another. Integers and
        floats are pushed onto the stack.
        """

        #The command string must be a string.
        assert isinstance(command_string, basestring)

        log.debug('interpret: %s', repr(command_string))

        #Split the command string on the whitespace.
        words = command_string.split()

        #For each command in the command string..
        for word in words:

            if word.startswith('"') and word.endswith('"') and \
               len(word) > 1:
                self.stack.insert(0, word[1:-1])
                continue

            #first, try making an integer..
            try:
                i = int(word)
                self.stack.insert(0, i)
            except ValueError:

                #if that didn't work, try making a float..
                try:
                    f = float(word)
                    self.stack.insert(0, f)
                except ValueError:

                    #not a float or integer, eh? Let's try executing it..
                    self.execute_name(word)

    def execute_name(self, word):
        """
        Given the name of an ExecutableWord in the dictionary (we hope,)
        Look up the word in self's dictionary and then execute it.
        """
        try:
            eword = self.dictionary[word]
        except KeyError:
            raise UnknownWordError(word)
        self.execute_word(eword)

    def execute_word(self, eword):
        """
        Given an instance of an ExecutableWord, execute it with self's stack.
        """
        BracketedExecuteWord(self.stack, eword)

    def _become(self, stack, dictionary):
        '''
        Given a new stack and dictionary, "become" the interpreter defined
        by them.  Support for state persistance.
        '''

        #the new stack becomes our stack
        self.stack[:] = stack

        #the new dictionary becomes our dictionary
        self.dictionary.clear()
        self.dictionary.update(dictionary)


def BracketedExecuteWord(stack, eword):
    """
    Given an instance of an ExecutableWord, execute it with stack.
    """

    #Check that the incoming arguments are acceptable.
    if __debug__:
        try:
            eword._stackok(stack)
        except AssertionError, message:
            print >> sys.stderr, 'input error "%s":' % eword.name, message
            raise

    #Execute the word.
    try:
        eword.execute(stack)
    except AssertionError, message:
        print >> sys.stderr, 'execute error "%s":' % eword.name, message
        raise

    #Check that the outgoing results are acceptable.
    if __debug__:
        try:
            eword._resultsok(stack)
        except AssertionError, message:
            print >> sys.stderr, 'output error "%s":' % eword.name, message
            raise


class ExecutableWord(object):
    """
    ExecutableWord - This class encapsulates the action of
    a single atomic command. It also carries metadata about
    the command, such as its name and the types and order of
    arguments it accepts and returns.

    Instance Variables:

        name : the name of the command.

    Methods:

        execute - Perform the action of the command on a given stack.
            ("execute" is overridden in subclasses to do useful work.)

        _stackok - Check if a list of args matches the input_args.
        _resultsok - Check if a list of results matches the output_args.

    """

    def __init__(self, name=None):
        """
        Create an ExecutableWord. If a name is given, use it.
        """

        if not name:

            #See if we've been given a name already.
            try:
                name = self.__name__

            #The default name is the name of self's class.
            except AttributeError:
                name = self.__class__.__name__

        #Remember the name.
        self.name = name

    def execute(self, stack):
        """
        Perform the action of self on the contents of the stack.
        """
        pass

    def _stackok(self, stack):
        """
        Check that the given stack is good for processing.
        """
        pass

    def _resultsok(self, stack):
        """
        Check that self's results agree with expectations.
        """
        pass

    def __repr__(self):
        return "Word %s" % self.name


Nop = ExecutableWord('Nop')
Nop.__doc__ = 'No Operation. Default "do nothing" word.'


class UnknownWordError(Exception):
    """
    Raised when an unknown word is encountered by the Interpreter.
    """


################################################################################
##
##    ComboWords
##
##    These words are the basis for creating complex commands out of other words.
##
##    Each of these words organizes two or more other words into a certain
##    arrangement. The four types are:
##
##    Branch     - Do one thing or the other, depending on the results of a test.
##    Sequential - Do one thing after another.
##    Loop       - Do something over again, depending on the results of a test.
##    Parallel   - Do two things that don't interfere with each other.
##
##    That is all the kinds of combinations of words there are.
##
################################################################################


####################################
#### Branch Word                ####
####################################

class BranchExecutableWord(ExecutableWord):
    """
    """

    __name__ = "branch"

    def __init__(self, name=None):
        """
        Branch  - Do one thing or the other, depending on the results of a test.
        """

        #Remember self's children.
        self.word0 = self.word1 = Nop

        #Call the superclass constructor
        ExecutableWord.__init__(self, name)

    def _stackok(self, stack):
        assert stack, 'stack too small, needs 1 thing'
        super(BranchExecutableWord, self)._stackok(stack)

    def execute(self, stack):
        """
        Pop and check the top value from the stack, then
        either execute word0 or word1 depending.
        """

        #Get the boolean flag value.
        flag = stack.pop(0)

        #If true (i.e. flag != 0) execute word1..
        if flag:
            BracketedExecuteWord(stack, self.word1)

        #if false (i.e. flag == 0) execute word0.
        else:
            BracketedExecuteWord(stack, self.word0)

    def __repr__(self):
        return '%s & %s %s' % (
            self.name, self.word1.name, self.word0.name
            )


####################################
#### Sequence Word              ####
####################################
class SequentialExecutableWord(ExecutableWord, ListModel):
    """
    SequentialExecutableWord - This class executes its words one after
    the other. It doesn't check the argument signatures of its child
    words.

    Public Methods:
        execute - Execute self's words.

    """

    __name__ = "seq"

    def __init__(self, name=None, initlist=[]):
        list.__init__(self, initlist)
        # ListModel doesn't have its own __init__().
        ExecutableWord.__init__(self, name)

    def __getstate__(self):
        state = [self.name, list(self)]
        if hasattr(self, 'doc'):
            state.append(self.doc)
        return state

    def __setstate__(self, state):
        name, items = state[:2]
        self.name = name
##        list.__setslice__(self, 0, 0, items) # Huh!?  w/o this unpickling
        # creates the seq words just fine, with it they each have 2x their
        # words.  I.e. "seq = 0 1 2 0 1 2"  (not "= 0 1 2")
        if len(state) == 3:
            self.doc = state[2]

    def execute(self, stack):
        """
        Execute self's kids. (Doesn't that sound horrible!)
        Overrides superclass method.
        """
        for kid in self:
            BracketedExecuteWord(stack, kid)

    def __setitem__(self, k, v):
        assert isinstance(v, ExecutableWord)
        super(SequentialExecutableWord, self).__setitem__(k, v)

    def __setslice__(self, i, j, seq):
        assert False not in (isinstance(n, ExecutableWord) for n in seq)
        super(SequentialExecutableWord, self).__setslice__(i, j, seq)

    def __iadd__(self, other):
        assert False not in (isinstance(n, ExecutableWord) for n in other)
        return super(SequentialExecutableWord, self).__iadd__(other)

    def append(self, item):
        assert isinstance(item, ExecutableWord)
        super(SequentialExecutableWord, self).append(item)

    def insert(self, i, item):
        assert isinstance(item, ExecutableWord)
        super(SequentialExecutableWord, self).insert(i, item)

    def extend(self, other):
        assert False not in (isinstance(n, ExecutableWord) for n in other)
        super(SequentialExecutableWord, self).extend(other)

    def __repr__(self):
        return '%s = %s' % (self.name, ' '.join(n.name for n in self))


####################################
#### Loop Word                  ####
####################################
class LoopExecutableWord(SequentialExecutableWord):
    """
    """

    __name__ = "loop"

    def _stackok(self, stack):
        assert stack, 'stack too small, needs 1 thing'
        super(LoopExecutableWord, self)._stackok(stack)

    def execute(self, stack):
        """
        Check the value on the TOS for Trueness, execute body if so.

        There is an infinite loop check in the form of the safety counter.
        It's a crude but effective protection for now but it shouldn't remain
        for long.
        """

        safety = 10000
        while safety:
            safety -= 1 #no more than 10000 interations for now.

            if __debug__:
                self._stackok(stack) # Re-check the stack on each iteration.

            flag = stack.pop(0)

            if flag:
                SequentialExecutableWord.execute(self, stack)

            else:
                safety = True #in case flag == False and safety == 0
                break

        if not safety:
            raise OverflowError, (self, 'recursion limit exceeded.')

    def __repr__(self):
        return '%s @ %s' % (self.name, ' '.join(n.name for n in self))


####################################
####  Parallel Word             ####
####################################
class ParallelExecutableWord(ExecutableWord):
    """
    This is just a preliminary first approximation.
    """

    __name__ = "fork"

    def __init__(self, name=None, word0=Nop, word1=Nop):
        """
        """

        #Check that both words are ExecutableWords.
        assert isinstance(word0, ExecutableWord)
        assert isinstance(word1, ExecutableWord)

        #Remember self's children.
        self.word0 = word0
        self.word1 = word1

        #Call the superclass constructor
        ExecutableWord.__init__(self, name)

    def execute(self, stack):
        """
        """
        raise NotImplementedError, self

    def __repr__(self):
        return '%s | %s %s' % (
            self.name, self.word1.name, self.word0.name
            )


class warranty(ExecutableWord):
    """
                            NO WARRANTY

BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY
FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN
OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES
PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED
OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS
TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE
PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING,
REPAIR OR CORRECTION.

IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR
REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED
TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY
YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER
PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE
POSSIBILITY OF SUCH DAMAGES.

    """
    def execute(self, stack):
        print self.__doc__


class SelfWord(ExecutableWord):

    __name__ = 'self'

    def __init__(self, interpreter):
        ExecutableWord.__init__(self)
        self.interpreter = interpreter

    def execute(self, stack):
        stack.insert(0, self.interpreter)

    def __repr__(self):
        return '%s word - %s ' % (
            self.name,
            getattr(self.interpreter, 'name', self.interpreter)
            )

class Interpreter(SimpleInterpreter):
    __doc__ = SimpleInterpreter.__doc__

    def __init__(self, stack=None, dictionary=None):
        SimpleInterpreter.__init__(self, stack, dictionary)
        self.dictionary.setdefault('Nop', Nop)
        self.dictionary.setdefault('warranty', warranty())
        self.windows = []


class DefaultExecute(ExecutableWord):
    '''
    This is a class to make 'execute' ExecutableWords for Objects.
    '''

    def __init__(self, thing):
        ExecutableWord.__init__(self, 'execute')
        self.thing = thing

    def _stackok(self, stack):
        assert len(stack) >= 1, 'stack too small, needs 1 thing'

    def execute(self, stack):
        '''
        To use:

            Put some args onto the stack then put a string command onto
            the stack, the inner Object gets those args as a list on it's
            stack.

            Caller: ["some commands", a, b, c]

            Caller calls Object.execute() which appends caller's stack
            onto callee's stack, like so:

                [["some commands", a, b, c], x, y, z] <=:Callee's stack.

                DefaultExecute.execute() pops the message/command off of
                the caller's embedded stack

                [[a, b, c], x, y, z] : <= "some commands"
        '''

        message = stack[0].pop(0)

        self.thing.interpret(message)

    def __repr__(self):
        return '%s word - %s ' % (
            self.name,
            getattr(self.thing, 'name', self.thing)
            )


class Object(Interpreter, ExecutableWord):
    """"
    An Object class created by merging an Interpreter and an ExecutableWord.
    """

    def __init__(self, name=None, stack=None, dictionary=None):
        Interpreter.__init__(self, stack, dictionary)
        ExecutableWord.__init__(self, name)
        if 'execute' not in self.dictionary:
            self.dictionary['execute'] = DefaultExecute(self)

    def execute(self, stack):
        try:
            execute = self.dictionary['execute']
        except KeyError:
            return
        self.stack.insert(0, stack)
        self.execute_word(execute)

    def __repr__(self):
        return 'Object %s' % self.name


if __name__ == '__main__':

    class dotess(ExecutableWord):
        __name__ = '.s'
        def execute(self, stack):
            print stack

    interp = Object(dictionary = {'.s':dotess()})

    interp.interpret('.s 1 2.3 4 .s')

##Output:
##[]
##[1, 2.2999999999999998, 4]
