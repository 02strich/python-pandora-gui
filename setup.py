#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

#mainscript = 'pandora_gui/pyside.py'
mainscript = 'pandora_gui/tkinter.py'

if sys.platform == 'darwin':
	try:
		import py2app
		extra_options = dict(
			setup_requires=['py2app'],
			app=[mainscript],
			# Cross-platform applications generally expect sys.argv to
			# be used for opening files.
			options = {"py2app":
				{"frameworks": ['libbass.dylib'] },
			},
		)
	except ImportError:
		extra_options = dict()
elif sys.platform == 'win32':
	try:
		import py2exe
		extra_options = dict(
			setup_requires=['py2exe'],
			windows=[{'script': mainscript, 'icon_resources':  [(0, "pandora.ico")]}],
			data_files = [('', ['bass.dll'])],
			options={ 
				"py2exe":{
					"optimize": 2,
				}
			},	
		)
	except ImportError:
		extra_options = dict()
else:
	extra_options = dict(
		# Normally unix-like platforms will use "setup.py install"
		# and install the main script as such
		scripts=[mainscript],
	)

setup(name='python-pandora-gui',
	version='0.1',
	description='Simple, platform-independent GUI for pandora.com',
	author='Stefan Richter',
	author_email='stefan@02strich.de',
	packages = find_packages(),
	install_requires=['python-pandora'],
	**extra_options)

# patch library.zip
if sys.argv[1] == 'py2exe':    
    from pandora import get_pkg_data_files
    import zipfile
    
    z = zipfile.ZipFile("dist/library.zip", "a")
    for pandora_data in get_pkg_data_files():
        z.write(pandora_data[1], 'pandora/'+pandora_data[0])
    z.close()
    