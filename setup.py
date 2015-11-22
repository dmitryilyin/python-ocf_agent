#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ocf_agent import AUTHOR, LICENSE, VERSION, EMAIL, PROJECT
from distutils.core import setup

# from Cython.Build import cythonize
# ext_modules=cythonize(['ocf_agent/*.py', 'dummy.py'])

setup(
    name=PROJECT,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    py_modules=['ocf_agent'],
    packages=['ocf_agent', 'ocf_agent/modules'],
    license=LICENSE,
)
