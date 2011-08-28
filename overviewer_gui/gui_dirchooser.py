# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dirchooser.ui'
#
# Created: Sat Aug 27 22:51:35 2011
#      by: pyside-uic 0.2.12 running on PySide 1.0.5
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_dirChooser(object):
    def setupUi(self, dirChooser):
        dirChooser.setObjectName("dirChooser")
        dirChooser.setWindowModality(QtCore.Qt.ApplicationModal)
        dirChooser.resize(522, 334)
        dirChooser.setMinimumSize(QtCore.QSize(285, 219))
        self.gridLayout = QtGui.QGridLayout(dirChooser)
        self.gridLayout.setContentsMargins(7, 7, 8, 7)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtGui.QLabel(dirChooser)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.label_2.setFont(font)
        self.label_2.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select your Minecraft World directory</p></body></html>")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.treeView = QtGui.QTreeView(dirChooser)
        self.treeView.setAutoScrollMargin(16)
        self.treeView.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.treeView.setHeaderHidden(False)
        self.treeView.setObjectName("treeView")
        self.treeView.header().setVisible(True)
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.description_label = QtGui.QLabel(dirChooser)
        self.description_label.setText("")
        self.description_label.setObjectName("description_label")
        self.horizontalLayout.addWidget(self.description_label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(dirChooser)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
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

