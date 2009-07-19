'''
Helper module for startup.  The basic Documentation words are defined here.
'''

# This module contains named documentation strings.  These strings will be made
# into TextViewers in the main interpreter.

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
'''


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
demotext emit sys.exit

OS Words
----------------------------------
find ls pwd

Time Words
----------------------------------
time timedate

'''

docs = dict(
    (k, v)
    for k, v in globals().items()
    if not k.startswith('_')
    )
