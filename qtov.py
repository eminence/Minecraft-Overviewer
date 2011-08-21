#!/usr/bin/env python

#    This file is part of the Minecraft Overviewer.
#
#    Minecraft Overviewer is free software: you can redistribute it and/or
#    modify it under the terms of the GNU General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or (at
#    your option) any later version.
#
#    Minecraft Overviewer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#    Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with the Overviewer.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os

from PySide.QtCore import *
from PySide.QtGui import *


from overviewer_core import optimizeimages, world, quadtree
from overviewer_core import googlemap, rendernode
import multiprocessing

cpuCount = multiprocessing.cpu_count()

from overviewer_gui import *

        



app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.dirChooser = None

## set up UI
ui.numProcessors.setMaximum(cpuCount)


worlds = world.get_worlds()
for name, info in sorted(worlds.iteritems()):
    print name, info['path']
    ui.worldComboBox.insertItem(ui.worldComboBox.count()-1, str(name), info['path'])


## set up event connections

ui.pushButton_goRender.clicked.connect(goRender(ui))
ui.worldComboBox.activated.connect(worldSelect(ui))



MainWindow.show()
sys.exit(app.exec_())

