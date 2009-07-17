'''
Helper module for startup.  The basic Documentation words are defined here.
'''
from xerblin import ExecutableWord
from xerblin.lib.programming import Variable


# This dict contains named documentation strings.  These strings will be made
# into TextViewers in the main interpreter.
Documentation = dict(

    Guide = '''Welcome to Xerblin
    
    This is the Guide.  You can close this textviewer and then open it again later by right-clicking on the word Guide in any textviewer.  You can also reopen this Guide by using the "Open Guide" button on the Xerblin main window.

    Right-clicking on a word that is also the name of a Xerblin ExecutableWord will "Invoke" that word, causing it to perform its action.  You can tell if a word is a command because it will light up orange if you try right-clicking on it.  If you click the left button before releasing the right button you will open a doc about the word.

Fun words:

    calc - solve equations.  Type in an equation, put it on the stack (see below) and Invoke calc

    For a list of all the commands in the system Invoke Words .  Words opens a textviewer with a generated list of all the current words.  You can use open these words to read their documentation.  You can also Invoke WordList which opens a textviewer on a categorized list of some of the more useful words.

    You can also put text on the stack.  First select some text, then before you let go of the left mouse button press the right button too, then release both buttons.  The text you selected will appear on the stack.  You can also use the middle button instead of the right button and the text selection will removed (cut) from the textviewer as well as put on the stack.

Here is a summary of textviewer Mouse commands.  Open textviewer for more details about textviewers.

Invoke = Right
Open = Right, Left
Evoke = Right, Middle

Select/Point = Left
Copy = Left, Right
Cut = Left, Middle

Paste Selection = Middle
Paste TOS = Middle, Left
Pop/Paste TOS = Middle, Right

(TOS means "Top Of Stack", i.e. the item on the top of the Stack.)
''',

    WordList = '''WordList

Basic Words
==================================

Stack Words
----------------------------------
drop dup over pick
rot swap tuck

Math Words
----------------------------------
add div mod
mul sub

Logic Words
----------------------------------
and boolean
false not or
true


Advanced Words
==================================

Programming Words
----------------------------------
constant get makewords
NewBranchWord NewLoopWord NewSeqWord
Nop set variable

Object Words
----------------------------------
createObject execute getstack
Inscribe lookup self
warranty words

Special Words
----------------------------------
getattr getitem
setattr setitem setname

List Words
----------------------------------
meta unmeta
pop push


Additional Words
==================================

Animation Words
----------------------------------
attach run timeframe
cosinedelta cubicdelta
quadraticdelta sinedelta

GUI Words
----------------------------------
listviewer textviewer
makewidgets

Misc
----------------------------------
demotext emit s2t sys.exit

OS Words
----------------------------------
find ls pwd

Time Words
----------------------------------
time timedate

''',

    )


def InscribeDocumentationWords(interpreter):
    '''
    This helper function takes the above Documentation dict and converts
    it into textviewer objects in the interpreter's dictionary.
    It's only used in the main xerblin script.
    '''
    TV = interpreter.dictionary.get('textviewer')

    for name, text in Documentation.iteritems():

        # Convert the string into a Variable word.
        t = Variable(name, text)

        # Build a fake stack for TV.
        stack = [t, interpreter]

        # Make the textviewer Object.
        TV.execute(stack)
        T = stack[0]

        # Set the name.
        T.name = name

        T.dictionary['hide'].execute([])

        # "Inscribe" the word.
        interpreter.dictionary[name] = T


class GuideWords(ExecutableWord):
    '''
    A helper word to let the startup script create these words at runtime.
    Basically this is a hard-coded string constant.
    '''

    word_source = '''

        * Stack = "show" StackViewer
        * new-list = meta meta pop swap push unmeta
        * new-text = texts self "" textviewer push drop
        * save = meta scratchpad swap push drop

          t = pop swap drop unmeta
          i & t Nop
        * restore = scratchpad dup i

        * drop-all = meta drop
        * open = self swap open
        * Words = self dup words textviewer drop

    ''' + ''.join(
    # For each of the Documentation TextViewers, replace it with a SeqWord
    # that shows the textviewer.  This essentially makes the name of the
    # viewer open it.  To get the viewer you must Evoke the SeqWord and pick
    # out its trailing component (the textviewer object.)
    ' * %s = "show" %s ' % (n, n)
    for n in Documentation
    )

    def execute(self, stack):
        stack.insert(0, self.word_source)


