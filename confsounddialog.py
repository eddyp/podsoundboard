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
        self._initialfile = self._soundcontainer.fileOfSound(handler)

        self.setName(self._soundcontainer.soundName(self._handler))
        self.setFileName(self._soundcontainer.fileOfSound(self._handler))

        # connect the Choose button to the QFile Dialog
        self.ui.chooseFileButton.clicked.connect(self.getFileName)
        self.ui.buttonBox.accepted.connect(self.sendInfo2Parent)
        self.ui.soundNameEdit.textChanged.connect(self.uiNameChanged)

    def uiNameChanged(self, editString):
        self.setValidLineEdit(self.ui.soundNameEdit)
        if editString == self._initialname:
            return
        if self._soundcontainer.hasSound(editString):
            self.setValidLineEdit(self.ui.soundNameEdit, False)
        return

    def sendInfo2Parent(self):
        psn = self._soundcontainer.getSoundNameOfFile(self.file)
        if psn == None or self._initialname == psn:
            if not self._soundcontainer.updateNameAndFile(self._handler, self.name, self.file):
                warning(self, u'Eroare',
                        textwrap.dedent(
                        u"""
                        Proprietățile sunetului nu au putut fi schimbate.
                        Numele și sunetul trebuie să fie unice.
                        """
                        )
                        )
                return
            if self.file:
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

    @property
    def name(self):
        return self.ui.soundNameEdit.text()

    @property
    def file(self):
        return self.ui.fileNameEdit.text()

    def getFileName(self, soundName=None, fileName=None):
        if soundName:
            self.setName(soundName)
        if fileName:
            self.setFileName(fileName)
        defaultpath = QtCore.QDir.homePath() if self.file == u'' \
                        else path.dirname(self.file)
        #for some reason the filter is retuned, too
        fn, dummy = QtGui.QFileDialog.getOpenFileName(self, u'Alege fișierul',
                defaultpath,
                'Audio files (*.mp3 *.flac *.wav)')
        if fn:
            # TODO: check fn is a known sound for the parent
            self.setFileName(fn)
            self.setName(path.basename(fn.rstrip(sep + string.whitespace)))

        return fn

    def setFileName(self, fileName):

        self.setValidLineEdit(self.ui.fileNameEdit, True)
        if fileName is None:
            fileName = u''
        asn = self._soundcontainer.getSoundNameOfFile(fileName)
        if asn is not None and asn != self._initialname:
            self.setValidLineEdit(self.ui.fileNameEdit, False)
        self.ui.fileNameEdit.setText(fileName)

    def setName(self, soundName):
        self.ui.soundNameEdit.setText(soundName)

    def setValidLineEdit(self, lineedit, valid=True):
        font = lineedit.font()
        font.setStrikeOut(not valid)
        lineedit.setFont(font)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    sndcont = soundContainer()
    myapp = confSoundDialog(sndcont)
    myapp.show()
    sys.exit(app.exec_())
