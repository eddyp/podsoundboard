#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string
from os import sep, path
from PySide import QtCore, QtGui
import textwrap

information = QtGui.QMessageBox.information
warning = QtGui.QMessageBox.warning
critical = QtGui.QMessageBox.critical

from ui_confsounddialog import Ui_confSoundDialog

class confSoundDialog(QtGui.QDialog):
    _handler = None
    _parent = None

    _initialfile = None
    _initialname = None
    def __init__(self, soundcontainer, parent=None, handler=None):
        QtGui.QDialog.__init__(self, parent)
        self._parent = parent
        self.ui = Ui_confSoundDialog()
        self.ui.setupUi(self)

        self._soundcontainer = soundcontainer

        if handler == None:
            handler = self._soundcontainer.addSound()
        self._handler = handler
        self._initialname = self._soundcontainer.soundName(handler)
        self._initialname = self._soundcontainer.fileOfSound(handler)

        self.setName(self._soundcontainer.soundName(self._handler))
        self.setFileName(self._soundcontainer.fileOfSound(self._handler))

        # connect the Choose button to the QFile Dialog
        self.ui.chooseFileButton.clicked.connect(self.getFileName)
        self.ui.buttonBox.accepted.connect(self.sendInfo2Parent)
        self.ui.soundNameEdit.textChanged.connect(self.uiNameChanged)

    def uiNameChanged(self, editString):
        self.ui.buttonBox.setEnabled(True)
        if editString == self._initialname:
            return
        if self._soundcontainer.hasSound(editString):
            self.ui.buttonBox.setEnabled(False)
        return

    def sendInfo2Parent(self):
        if self._parent:
            psn = self._parent.getSoundNameOfFile(self._file)
            if psn == None or self._parent._name == psn:
                if not self._parent.setNameAndFile(self._name, self._file):
                    warning(self, u'Eroare',
                            textwrap.dedent(
                            u"""
                            Proprietățile sunetului nu au putut fi schimbate.
                            Probabil că numele există deja.
                            """
                            )
                            )
                    return
                if self._file:
                    self._parent.active = True
                self.accept()
            else:
                warning(self, u"Sunetul există deja",
                    textwrap.dedent(
                    u"""
                    Fișierul există deja sub numele '%s'.
                    Alegeți alt fișier.
                    """ % (psn))
                    )
                self.setName(psn)

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

        return fn

    def setFileName(self, fileName):
        self._file = fileName
        self.ui.fileNameEdit.setText(self._file)

    def setName(self, soundName):
        self._name = soundName
        self.ui.soundNameEdit.setText(soundName)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    sndcont = soundContainer()
    myapp = confSoundDialog(sndcont)
    myapp.show()
    sys.exit(app.exec_())
