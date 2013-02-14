#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PySide import QtCore, QtGui

from ui_filebrowse import Ui_browseDialog

class browseDialog(QtGui.QDialog):

    dm = QtGui.QFileSystemModel()
    fm = QtGui.QFileSystemModel()
    
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        self.ui = Ui_browseDialog()
        self.ui.setupUi(self)
        
        self.dm.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs)
        self.dm.setRootPath(QtCore.QDir().rootPath())
        self.ui.dirTreeView.setModel(self.dm)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = browseDialog()
    myapp.show()
    sys.exit(app.exec_())
