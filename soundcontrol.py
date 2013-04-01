#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui

from ui_soundcontrol import Ui_soundControl
from confsounddialog import confSoundDialog

class soundControl(QtGui.QWidget):

    _file = None
    def __init__(self, parent, parentform=None, name=u'sound', file=None, active=False):
        self.parentform = parentform
        self._name = name
        self._file = file

        QtGui.QWidget.__init__(self, parentform)

        if parentform:
            if self.parentform.hasSound(self._name):
                self._name = self.parentform.getNewSoundName(self._name)
            self.parentform.register(self, self._name)

        self.ui = Ui_soundControl()
        self.ui.setupUi(self)
        self.ui.soundButton.setText(self._name)
        self.ui.configButton.clicked.connect(self.openConfDialog)
        self.ui.delButton.clicked.connect(self.confirmClose)
        self.ui.soundButton.clicked.connect(self.playSound)
        self.setActive(active)

    def __del__(self):
        if self.parentform:
            try:
                self.parentform.unregister(self, self._name)
            except AttributeError:
                #TODO: warn about the inconsistency
                pass

    def confirmClose(self):
        confirm = QtGui.QMessageBox.warning(self, "Confirmare", \
                            u"Sigur vrei să închizi " + self._name + "?", \
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel, \
                            QtGui.QMessageBox.Cancel)
        if confirm is QtGui.QMessageBox.StandardButton.FirstButton:
            self.close()

    def openConfDialog(self):
        confdialog = confSoundDialog(self)
        confdialog.show()

    def setActive(self, state):
        self.ui.checkBox.setChecked(state)

    def setNameAndFile(self, name, file):
        self._name = name
        self._file = file
        self.ui.soundButton.setText(self._name)
        #m = QtGui.QMessageBox.information(self, 'info',name)

    #TODO: use a library for playing the media file
    def playSound(self):
        if self._file:
            import os
            if os.path.isfile(self._file):
                import subprocess
                subprocess.call(["mplayer", self._file])
            else:
                self.setActive(False)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = soundControl(u'sunet')
    myapp.show()
    sys.exit(app.exec_())
