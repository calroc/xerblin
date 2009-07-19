#!/usr/bin/env python
'''
    Copyright (C) 2004 - 2008 Simon Forman

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

'''
from xerblin.lib import words
from xerblin import Object
from xerblin.startup import startup_script, word_source
from xerblin.documentation import docs
from xerblin.lib.widgets.listwidgets import SequenceController
from xerblin.lib.widgets.widgetwrapper import makeViewer
from xerblin.lib.programming import Variable
from xerblin.util.mainapp import MainApp


def fresh(T):

    # Create the world and populate it with the library's words.
    I = Object(name='Xerblin', dictionary=words)

    app = MainApp(T, I)

    # By default ALWAYS open a ListViewer (i.e. SequenceController) on
    # the world's Stack.
    I.dictionary['StackViewer'] = makeViewer(
        "Xerblin Stack",    # name
        I.stack,            # model
        SequenceController, # viewer/controller class
        )

    # Insert Guide, et. al.
    InscribeDocumentationWords(I)

    I.interpret(startup_script)

    if 'makewords' in I.dictionary:
        I.stack.extend((word_source, I))
        I.interpret('makewords drop')


def InscribeDocumentationWords(interpreter):
    '''
    This helper function takes the above Documentation dict and converts
    it into textviewer objects in the interpreter's dictionary.
    It's only used in the main xerblin script.
    '''
    TV = interpreter.dictionary.get('textviewer')
    if not TV:
        return

    for name, text in docs.iteritems():

        # Convert the string into a Variable word.
        t = Variable(name)
        t.value = text

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
