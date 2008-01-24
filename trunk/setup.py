#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Xerblin',
    version='0.9.0',
    description='Xerblin System',
    author='Simon Forman',
    author_email='forman.simon@gmail.com',
    license='GPL',
    url='http://calroc.home.mindspring.com/xerblin',
    packages = [
        "xerblin",
        "xerblin.lib",
        "xerblin.lib.widgets",
        "xerblin.util",
        ],
    scripts=[
        'bin/xerblin',
        'bin/tkxerblin',
        ],
    )
