import os, sys

from PySide.QtCore import *
from PySide.QtGui import *
from overviewer_gui import *


from overviewer_core import optimizeimages, world, quadtree
from overviewer_core import googlemap, rendernode

class renderThread (QThread):
    def __init__(self, ui, worlddir, outputdir):
        self.ui = ui
        self.worlddir = worlddir
        self.outputdir = outputdir
        QThread.__init__(self);
    def run(self):
        print "thread is now running"

        numProcs = self.ui.numProcessors.value()
	
        biomeDir = os.path.join(self.worlddir, "biomes")
        if not os.path.exists(biomeDir):
            isBiome = False
        else:
            isBiome = True

        w = world.World(self.worlddir, self.outputdir, useBiomeData=isBiome)
        w.go(numProcs)
        bg_color="#1A1A1A"
        bgcolor = (int(bg_color[1:3],16), int(bg_color[3:5],16), int(bg_color[5:7],16), 0)
        options={'procs': numProcs, 'bg_color': bg_color}

        qtree_args = {'imgformat':'png', 'forcerender':False, 'bgcolor': bgcolor}
        q = []
        qtree = quadtree.QuadtreeGen(w, self.outputdir, rendermode="normal", tiledir='tiles', **qtree_args)
        q.append(qtree)

        # do quadtree-level preprocessing
        for qtree in q:
            qtree.go(numProcs)


        # create the distributed render
        r = rendernode.RenderNode(q, options)
        
        # write out the map and web assets
        m = googlemap.MapGen(q, configInfo=options)
        m.go(numProcs)

        def statusCallback(complete, total, level, unconditional=False):
            # TODO calculate the percent complete for the entire render
            #      not just for this level
            self.ui.progressBar.setValue(100*(complete/float(total)))
        
        # render the tiles!
        r.go(numProcs, statusCallback=statusCallback)

        # finish up the map
        m.finalize()
        self.ui.pushButton_goRender.setText("Done!")

       


def worldSelected(ui, dc):
    def _worldSelected():
        print "worldSelected()"
        i = dc.treeView.currentIndex()
        p = dc.treeView.model().filePath(i)
        print "World %s has been selected" % p
        ui.lineEdit_pathToWorld.setText(p)
        ui.pushButton_goRender.setEnabled(True)
        #ui.dirChooser.deleteLater()
    return _worldSelected 



def worldSelect(ui):
    def _worldSelect(v):
        index = ui.worldComboBox.findText(v)
        print "You selected index %s"% index
        if index == 0:
            ui.lineEdit_pathToWorld.setText("")
            ui.pushButton_goRender.setEnabled(False)
        elif v == "Browse...": # display the directory chooser
            if not ui.dirChooser:
                ui.dirChooser = QDialog()
                dc = Ui_dirChooser()
                dc.setupUi(ui.dirChooser)

                dc.model = QFileSystemModel()
                dc.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
		dc.model.setRootPath(QDir.currentPath())
                dc.treeView.setModel(dc.model)
                dc.treeView.setRootIndex(dc.model.index(QDir.currentPath()))

                dc.buttonBox.accepted.connect(worldSelected(ui, dc))

            ui.dirChooser.show()
            print "Done with chooser"
        else:
            d = ui.worldComboBox.itemData(index)
            ui.lineEdit_pathToWorld.setText(d)
            ui.pushButton_goRender.setEnabled(True)

    return _worldSelect



def goRender(ui):
    def _goRender():
        ui.pushButton_goRender.setEnabled(False)
        ui.pushButton_goRender.setText("Rendering...")
        numProcs = ui.numProcessors.value()
        worlddir = ui.lineEdit_pathToWorld.text()
        outputdir = ui.lineEdit_pathToOutput.text()
        print "Rendering with %d processors!" % numProcs
        print "Rendering %s to %s" % (worlddir, outputdir)
        if not os.path.exists(worlddir):
            sys.exit("world dir does not exist")

        ui.runThread = renderThread(ui, worlddir, outputdir)
        ui.runThread.start()
        print "Started render thread"


    return _goRender

