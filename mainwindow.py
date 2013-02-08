#!/usr/bin/env python

import sys
from PySide import QtCore, QtGui

from ui_mainwindow import Ui_MainWindow

class myMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = myMainWindow()
    myapp.show()
    sys.exit(app.exec_())