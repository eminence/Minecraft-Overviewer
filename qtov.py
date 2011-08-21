
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

