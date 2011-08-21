# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'overviewer.ui'
#
# Created: Sat Aug 20 22:33:21 2011
#      by: pyside-uic 0.2.12 running on PySide 1.0.5
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(475, 250)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.worldComboBox = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.worldComboBox.sizePolicy().hasHeightForWidth())
        self.worldComboBox.setSizePolicy(sizePolicy)
        self.worldComboBox.setObjectName("worldComboBox")
        self.worldComboBox.addItem("")
        self.worldComboBox.addItem("")
        self.worldComboBox.addItem("")
        self.worldComboBox.addItem("")
        self.horizontalLayout.addWidget(self.worldComboBox)
        self.pushButton_goRender = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_goRender.sizePolicy().hasHeightForWidth())
        self.pushButton_goRender.setSizePolicy(sizePolicy)
        self.pushButton_goRender.setObjectName("pushButton_goRender")
        self.horizontalLayout.addWidget(self.pushButton_goRender)
        self.numProcessors = QtGui.QSpinBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numProcessors.sizePolicy().hasHeightForWidth())
        self.numProcessors.setSizePolicy(sizePolicy)
        self.numProcessors.setMinimum(1)
        self.numProcessors.setMaximum(4)
        self.numProcessors.setObjectName("numProcessors")
        self.horizontalLayout.addWidget(self.numProcessors)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lineEdit_pathToWorld = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_pathToWorld.setObjectName("lineEdit_pathToWorld")
        self.verticalLayout.addWidget(self.lineEdit_pathToWorld)
        self.lineEdit_pathToOutput = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_pathToOutput.setObjectName("lineEdit_pathToOutput")
        self.verticalLayout.addWidget(self.lineEdit_pathToOutput)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL("activated()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.worldComboBox.setItemText(0, QtGui.QApplication.translate("MainWindow", "World1", None, QtGui.QApplication.UnicodeUTF8))
        self.worldComboBox.setItemText(1, QtGui.QApplication.translate("MainWindow", "World2", None, QtGui.QApplication.UnicodeUTF8))
        self.worldComboBox.setItemText(2, QtGui.QApplication.translate("MainWindow", "World3", None, QtGui.QApplication.UnicodeUTF8))
        self.worldComboBox.setItemText(3, QtGui.QApplication.translate("MainWindow", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_goRender.setText(QtGui.QApplication.translate("MainWindow", "Render!", None, QtGui.QApplication.UnicodeUTF8))
        self.numProcessors.setToolTip(QtGui.QApplication.translate("MainWindow", "Processors", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_pathToWorld.setText(QtGui.QApplication.translate("MainWindow", "/Users/achin/devel/eminence-overviewer/exmaple", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_pathToOutput.setText(QtGui.QApplication.translate("MainWindow", "/Users/achin/devel/eminence-overviewer/output_dir", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

