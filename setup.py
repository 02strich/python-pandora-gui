#!/usr/bin/env python
from setuptools import setup

setup(name='python-pandora-gui',
    version='0.1',
    description='Simple, platform-independent GUI for pandora.com',
    author='Stefan Richter',
    author_email='stefan@02strich.de',
    packages = ['pandora_gui'],
    install_requires=['python-pandora'],
)