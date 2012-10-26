#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe

setup(  windows=[{"script":"main.py"}], 
        options={
            "py2exe":{"includes":["sip"]}} )
