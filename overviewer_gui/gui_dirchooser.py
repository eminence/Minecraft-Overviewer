# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dirchooser.ui'
#
# Created: Sun Aug 21 00:36:11 2011
#      by: pyside-uic 0.2.12 running on PySide 1.0.5
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_dirChooser(object):
    def setupUi(self, dirChooser):
        dirChooser.setObjectName("dirChooser")
        dirChooser.setWindowModality(QtCore.Qt.ApplicationModal)
        dirChooser.resize(382, 247)
        dirChooser.setMinimumSize(QtCore.QSize(285, 219))
        self.gridLayout = QtGui.QGridLayout(dirChooser)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView = QtGui.QTreeView(dirChooser)
        self.treeView.setAutoScrollMargin(16)
        self.treeView.setHeaderHidden(False)
        self.treeView.setObjectName("treeView")
        self.treeView.header().setVisible(True)
        self.verticalLayout.addWidget(self.treeView)
        self.buttonBox = QtGui.QDialogButtonBox(dirChooser)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(dirChooser)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), dirChooser.hide)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), dirChooser.hide)
        QtCore.QMetaObject.connectSlotsByName(dirChooser)

    def retranslateUi(self, dirChooser):
        dirChooser.setWindowTitle(QtGui.QApplication.translate("dirChooser", "Directory Chooser", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dirChooser = QtGui.QDialog()
    ui = Ui_dirChooser()
    ui.setupUi(dirChooser)
    dirChooser.show()
    sys.exit(app.exec_())

