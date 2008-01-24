import os
import webbrowser

from xerblin import (
    ExecutableWord,
    LoopExecutableWord,
    SequentialExecutableWord,
    BranchExecutableWord,
    basedir,
    )
from xerblin.util.stackcheckers import StackLen, StackType
from xerblin.gui.TextViewer import (
    TextViewer,
    Toplevel,
    END,
    )
from xerblin.gui.Viewers import (
    FileViewer,
    DocumentViewer,
    WordViewer,
    )


class OpenTOS(MetaExecutableWord):
    """"Open a new TextViewer and load the string on TOS into it."""

    def _stackok(self, stack):
        assert stack, 'stack empty, needs 1 thing'
        assert isinstance(
            stack[-1],
            (basestring, list)
            ), "TOS isn't a string or list"

    def execute(self, stack):
        T = Toplevel()
        T.title("Xerblin Text")
        if isinstance(stack[-1], list):
            self._openDocl(stack.pop(), T)
            return
        xt = TextViewer(
            T,
            interpreter=self.interp,
            width=75,
            wrap='word'
            )
        T.protocol("WM_DELETE_WINDOW", xt.onclose(T))
        data = stack.pop()
        if isinstance(data, basestring):
            data = [data]
        for thing in data:
            xt.insert(END, thing)
        xt.pack(expand=1, fill='both')

    def _openDocl(self, doc, T):
        xt = DocumentViewer(
            T,
            document=doc,
            interpreter=self.interp,
            width=75,
            wrap='word'
            )
        T.protocol("WM_DELETE_WINDOW", xt.onclose(T))
        xt.pack(expand=1, fill='both')


class NewText(MetaExecutableWord):
    """"Open a new TextViewer."""

    def execute(self, stack):
        T = Toplevel()
        T.title("Xerblin Text")
        xt = TextViewer(
            T,
            interpreter=self.interp,
            width=75,
            wrap='word'
            )
        T.protocol("WM_DELETE_WINDOW", xt.onclose(T))
        xt.pack(expand=1, fill='both')


class Tutorial(OpenTOS):

    def _stackok(self, stack):
        pass

    def execute(self, stack):
        START_TXT = os.path.join(basedir, 'data', 'start.txt')
        start_txt = open(START_TXT).read()
        stack.append(start_txt)
        OpenTOS.execute(self, stack)


class opendoc(StackLen(1), StackType(0, basestring), MetaExecutableWord):

    def execute(self, stack):
        URLish = stack.pop()
        eword = self.interp.dictionary.get(URLish)

        if eword is not None:
            self.openWord(eword)

        elif URLish.startswith('http://') or URLish.startswith('https://'):
            webbrowser.open(URLish)

        elif os.path.isfile(URLish):
            self._openFile(URLish)

        else:
            print 'opendoc', URLish

    def openWord(self, eword):
        T = Toplevel()
        T.title('Word: %s' % (eword.name,))
        xt = WordViewer(
            T,
            interpreter=self.interp,
            word=eword,
            width=75,
            wrap='word'
            )
        T.protocol("WM_DELETE_WINDOW", xt.onclose(T))
        xt.pack(expand=1, fill='both')

    def _openFile(self, path):
        T = Toplevel()
        T.title('File: %s' % (path,))
        xt = FileViewer(
            T,
            interpreter=self.interp,
            filename=path,
            width=75,
            wrap='word'
            )
        T.protocol("WM_DELETE_WINDOW", xt.onclose(T))
        xt.pack(expand=1, fill='both')


class listwords(MetaExecutableWord):
    '''This class puts a -list- of all the words onto the stack.'''
    def execute(self, stack):
        '''Put a list of words in the dictionary onto the stack.'''
        words = self.interp.dictionary.keys()
        words.sort()
        stack.append(words)


class printwords(MetaExecutableWord):
    '''THIS class prints out the names of all the words in the dictionary.'''
    def execute(self, stack):
        '''Print a list of words in the dictionary.'''
        words = self.interp.dictionary.keys()
        words.sort()
        print ' '.join(words)


class Words(MetaExecutableWord):
    '''This class puts the names of all the words in the dictionary onto the stack.'''

    __name__ = 'words'

    def execute(self, stack):
        '''Print a list of words in the dictionary.'''
        words = self.interp.dictionary.keys()
        words.sort()
        stack.append(' '.join(words))


class listdict(MetaExecutableWord):
    '''This class prints out the names and __doc__ strings of all the words
    in the dictionary.'''
    def execute(self, stack):
        '''Print a list of words and their descriptions.'''
        words = self.interp.dictionary.items()
        words.sort()
        for n, w in words:
            print '%s - %s' % (n, w.__doc__)


import pickle

class pickleme(MetaExecutableWord):
    '''
    This word pickles the current state of
    the Interpreter including stack and dictionary.
    '''
    def execute(self, stack):
        '''
        Pickle the Interpreter and put the
        pickled data on the stack.
        '''

        s = pickle.dumps(self.interp)
        stack.append(s)

class unpickleme(StackLen(1), StackType(0, basestring), MetaExecutableWord):
    '''
    This word unpickles a pickled Interpreter
    and puts it on the stack.
    '''
    def execute(self, stack):
        '''
        Unpickle a pickled Interpreter and put
        it on the stack.
        '''
        pickledata = stack[-1]

        new_interp = pickle.loads(pickledata)

        self.interp._become(new_interp.stack, new_interp.dictionary)


class chomp(MetaExecutableWord):
    '''
    This Words 'chomps' the next word in the command line into a string
    which it then puts onto the stack. If it is followed by blankspace only
    it will chomp and stack all of the blankspace. I.e., to get a single
    space character onto the stack using chomp issue the command,

        "chomp "

    If chomp appears at the end of a command line with nothing following it
    it will put an empty, zero-length string on the stack.

    chomp is a MetaExecutableWord, and should be instancetiated with an
    Interpreter instance as its first arg, like so:

        interp.dictionary['chomp'] = chomp(interp)

    (Note: chomp is not very useful for getting strings that contain blankspace
    onto the stack. For that, either push the string directly,

        interp.stack.append("Loo loo loo!")

    or use the GUI interface or a file or file-like object.)
    '''
    def execute(self, stack):
        '''
        Read the next word, or trailing blankspace or null char, from the
        command line and place it on the stack.
        '''
        #Get a local reference to self's Interpreter.
        interp = self.interp
        blankspace = self.interp.blankspace

        #Get local references to the command line and index
        i, command = interp.i, interp.command

        #Cache the length of the command line.
        l = len(command)

        #If we're at the end of the command line append a null string and
        #be done with it.
        if i == l:
            stack.append('')
            return

        #We should only begin on blankspace.
        assert command[i] in blankspace

        #Run past any more blankspace, or to the end.
        while (i < l) and (command[i] in blankspace): i += 1

        #If we've got to the end of the command but there wasn't any
        #non-blankspace, append the blankspace. That's how you get
        #blankspace-only strings onto the stack. :)
        if i == l:

            #interp.i remembers our starting point.
            begin = interp.i

        #Otherwise, we've got to some non-blankspace before the end of the line.
        else:

            #Make sure this is so.
            assert (i < l) and (command[i] not in blankspace)

            #Remember the beginning of the word.
            begin = i

            #Force increment i by one.
            i += 1

            #Run to the end of the line, or to the next blankspace char.
            while (i < l) and (command[i] not in blankspace): i += 1

            #We're either at the end of the line, or of the word.
            assert (i == l) or ((begin < i < l) and (command[i] in blankspace))

        #Append our new string.
        stack.append(command[begin:i])

        #Let our Interpreter know how much command line we've used.
        interp.i = i


class loadlibrary(StackLen(1), StackType(0, basestring), MetaExecutableWord):
    """Given the name of a library module, load the words it
    defines into the self's Interpreter."""

    def execute(self, stack):
        libname = stack[-1]

        lib = __import__(libname)
        components = libname.split('.')
        for comp in components[1:]:
            lib = getattr(lib, comp)

        #If there is a 'words' dictionary in the module, merge it into ours.
        if hasattr(lib, 'words'):
            self.interp.dictionary.update(lib.words)

        #If there is a 'getWords' method, call it on our Interpreter to
        #get and merge any MetaExecutableWords that the library defines.
        if hasattr(lib, 'getWords'):
            self.interp.dictionary.update(lib.getWords(self.interp))

	stack[-1] = 1

