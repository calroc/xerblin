'''
    Copyright (C) 2004 - 2009 Simon Forman

    This file is part of Xerblin.

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

This module contains named documentation strings.  These strings will be made
into TextViewers in the main interpreter.

Helper module for startup.
'''


Guide = '''Welcome to Xerblin
    
    This is the Guide.
    
    You can close this textviewer and then open it again later by right-clicking on the word Guide in any textviewer.  You can also reopen this Guide by using the "Open Guide" button on the Xerblin main window.

    Right-clicking on a word that is the name of a Xerblin ExecutableWord will "Invoke" that word, causing it to perform its action.  You can tell if a word is a command because it will light up orange if you try right-clicking on it.  
    
    If you click the left button before releasing the right button you will open a textviewer with information about the word.

    You can invoke WordList which opens a textviewer on a categorized list of some of the more useful words.  Or for a list of all the commands in the system invoke Words which opens a textviewer with a generated list of all the current words.

    You can also put text on the stack.
    
    First select some text, then before you let go of the left mouse button press the right button too, then release both buttons.  The text you selected will appear on the stack.
    
    You can also use the middle button instead of the right button and the text selection will removed (cut) from the textviewer as well as put on the stack.

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

Stack Words
----------------------------------
drop dup over pick
rot swap tuck

Math and Logic Words
----------------------------------
add sub
mul div mod
and or
true false not boolean

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
setname
getattr getitem
setattr setitem

List Words
----------------------------------
new-list
meta unmeta
pop push

GUI Words
----------------------------------
new-text
listviewer textviewer

Misc. Words
----------------------------------
emit sys.exit
find ls pwd
time timedate

'''

docs = dict(
    (k, v)
    for k, v in globals().items()
    if not k.startswith('_')
    )