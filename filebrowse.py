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

        self.fm.setFilter(QtCore.QDir.Files | QtCore.QDir.Readable)
        self.fm.setRootPath(QtCore.QDir().rootPath())
        self.ui.fileListView.setModel(self.fm)

##        QtCore.QObject.connect(self.ui.dirTreeView, \
##                QtCore.SIGNAL("rootPathChanged(self, newPath)"), \
##                self.fm.setRootPath(newPath))
        #self.ui.dirTreeView.rootPathChanged.connect(self.fm.setRootPath)

        # try to see if QFileDialog is enough
        file = QtGui.QFileDialog.getOpenFileName(self, u'Alege fișierul', \
                QtCore.QDir().homePath(), \
                'Audio files (*.mp3 *.flac *.wav)')


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = browseDialog()
    myapp.show()
    sys.exit(app.exec_())
