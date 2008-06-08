#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Xerblin',
    version='0.9.3',
    description='Xerblin System',
    author='Simon Forman',
    author_email='forman.simon@gmail.com',
    license='GPL',
    url='http://code.google.com/p/xerblin/',
    packages = [
        "xerblin",
        "xerblin.lib",
        "xerblin.lib.widgets",
        "xerblin.lib.pygoo",
        "xerblin.lib.animation",
        "xerblin.util",
        ],
    scripts=[
        'bin/xerblin',
        ],
    )
