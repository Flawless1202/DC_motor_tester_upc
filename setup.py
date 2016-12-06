# -*- coding: utf-8 -*-

#
# Run the build process by running the command 'python setup.py build_msi' for windows
# or 'python setup.py build_dmg' for mac os
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        'motor_test.py',  # the name of the python file
        base=base,
        shortcutName="motor",  # the name of the app
        shortcutDir="DesktopFolder",
    )
]

build_exe_options = {"packages": [
    "numpy", "matplotlib", "sys", "motor", "wx", "os", "matplotlib.figure", "matplotlib.backends","FileDialog"]}

setup(name='motor',
      version='1.0',
      description='setup description',
      options={"build_exe": build_exe_options},
      executables=executables
      )
