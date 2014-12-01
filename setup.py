#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import librarycloud
version = librarycloud.__version__

setup(
    name='librarycloud',
    version=version,
    author='',
    author_email='andromeda.yelton@gmail.com',
    packages=[
        'librarycloud',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.7.1',
    ],
    zip_safe=False,
    scripts=['librarycloud/manage.py'],
)
