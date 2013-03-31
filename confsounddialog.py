#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string
from os import sep, path
from PySide import QtCore, QtGui

from ui_confsounddialog import Ui_confSoundDialog

class confSoundDialog(QtGui.QDialog):
    _file = None
    _name = None
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self._parent = parent
        self.ui = Ui_confSoundDialog()
        self.ui.setupUi(self)
        # connect the Choose button to the QFile Dialog
        self.ui.chooseFileButton.clicked.connect(self.getFileName)
        self.ui.buttonBox.accepted.connect(self.sendInfo2Parent)
        self.ui.soundNameEdit.textChanged.connect(self.uiNameChanged)

    def uiNameChanged(self, editString):
        self._name = editString

    def sendInfo2Parent(self):
        if self._parent:
            self._parent.setNameAndFile(self._name, self._file)
            self._parent.setActive(True)

    def getFileName(self, soundName=None, fileName=None):
        if soundName:
            self.setName(soundName)
        if fileName:
            self.setFileName(fileName)
        #for some reason the filter is retuned, too
        fn, dummy = QtGui.QFileDialog.getOpenFileName(self, u'Alege fișierul', \
                QtCore.QDir().homePath(), \
                'Audio files (*.mp3 *.flac *.wav)')
        if fn:
            # TODO: check fn is a known sound for the parent
            self.setFileName(fn)
            self.setName(path.basename(fn.rstrip(sep + string.whitespace)))

        return filename

    def setFileName(self, fileName):
        self.ui.fileNameEdit.setText(fileName)
        self.uiNameChanged(fileName)

    def setName(self, soundName):
        self._name = soundName
        self.ui.soundNameEdit.setText(soundName)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = confSoundDialog()
    myapp.show()
    sys.exit(app.exec_())
