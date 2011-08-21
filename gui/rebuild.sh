#!/bin/sh

# When you update the overviewer.ui file, run this script to rebuild
# the gui_main.py file

pyside-uic -x overviewer.ui -o gui_main.py
pyside-uic -x dirchooser.ui -o gui_dirchooser.py
