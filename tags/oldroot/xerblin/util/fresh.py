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
from xerblin.startup import startup_script
from xerblin.lib.widgets.listwidgets import MakeViewer, SequenceController
from xerblin.lib.guide import InscribeDocumentationWords
from xerblin.util.mainapp import MainApp
from xerblin.util.timed import Timed
from xerblin.util.backtime import attemptBackup
from xerblin.messaging import RootViewer, ModelMixin


def fresh(T):

    # Create the world and populate it with the library's words.
    I = Object(name='Xerblin', dictionary=words)

    # Create a time-delayed proxy caller to attemptBackup()
    tm = Timed(T, lambda: attemptBackup(I))

    # Arrange to have it triggered on every NotifyMessage.
    ModelMixin.root = RootViewer(None, lambda message: tm.trigger())

    app = MainApp(T, I)

    # By default ALWAYS open a ListViewer (i.e. SequenceController) on
    # the world's Stack.
    I.dictionary['StackViewer'] = MakeViewer(
        "Xerblin Stack",    # name
        I.stack,            # model
        SequenceController, # viewer/controller class
        )

    # Insert Guide, et. al.
    InscribeDocumentationWords(I)

    I.interpret(startup_script)
