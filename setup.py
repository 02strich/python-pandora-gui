#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

try:
    import py2exe
except:
    pass

setup(name='python-pandora-gui',
    version='0.1',
    description='Simple, platform-independent GUI for pandora.com',
    author='Stefan Richter',
    author_email='stefan@02strich.de',
    packages = find_packages(),
    install_requires=['python-pandora'],
    
    # py2exe
    windows=['pandora_gui/tkinter.py'],
    data_files = [('', ['bass.dll', 'config.ini'])],
    options={
                "py2exe":{
                    "optimize": 2,
                }
    },
)

# patch library.zip
if sys.argv[1] == 'py2exe':    
    from pandora import get_pkg_data_files
    import zipfile
    
    z = zipfile.ZipFile("dist/library.zip", "a")
    for pandora_data in get_pkg_data_files():
        z.write(pandora_data[1], 'pandora/'+pandora_data[0])
    z.close()
    