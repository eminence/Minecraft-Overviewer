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
from overviewer_core import c_overviewer
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


avail_rendermodes = c_overviewer.get_render_modes()
rendermode_info = map(c_overviewer.get_render_mode_info, avail_rendermodes)
name_width = max(map(lambda i: len(i['name']), rendermode_info))

ui.render_mode_boxes = []
for info in rendermode_info:
    
    new_checkbox = QCheckBox(ui.renderModeGroupBox)
    ui.renderModeLayout.addWidget(new_checkbox)
    new_checkbox.setText(info['name'])
    new_checkbox.setToolTip(info['description'])
    ui.render_mode_boxes.append(new_checkbox)
    print "{name:{0}} {description}".format(name_width, **info)

## set up event connections

ui.pushButton_goRender.clicked.connect(goRender(ui))
ui.worldComboBox.activated.connect(worldSelect(ui))



MainWindow.show()

sys.exit(app.exec_())

