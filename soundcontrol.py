#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui

information = QtGui.QMessageBox.information
warning = QtGui.QMessageBox.warning
critical = QtGui.QMessageBox.critical

from ui_soundcontrol import Ui_soundControl
from confsounddialog import confSoundDialog
from soundcontainer import soundContainer

class soundControl(QtGui.QWidget):

    parentform = None

    def __init__(self, soundcontainer,
                            handler=None, parentform=None, active=False):

        self._soundcontainer = soundcontainer
        if handler is None:
            handler = self._soundcontainer.addSound()
        self._handler = handler
        self._soundcontainer.register(handler, self)
        self.parentform = parentform

        QtGui.QWidget.__init__(self, parentform)

        self.ui = Ui_soundControl()
        self.ui.setupUi(self)
        self.ui.soundButton.setText(
                    self._soundcontainer.soundName(self._handler))
        self.ui.configButton.clicked.connect(self.openConfDialog)
        self.ui.delButton.clicked.connect(self.confirmClose)
        self.ui.soundButton.clicked.connect(self.playSound)
        self.active = active

    def __del__(self):
        self._soundcontainer.unregister(self._handler, self)

    @property
    def file(self):
        return self._soundcontainer.fileOfSound(self._handler)

    @file.setter
    def file(self, file):
        return self._soundcontainer.updateFile(self._handler, file)

    def confirmClose(self):
        confirm = warning(self, "Confirmare",
                    u"Sigur vrei să închizi " +
                        self._soundcontainer.soundName(self._handler) + "?",
                    QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                    QtGui.QMessageBox.Cancel)
        if confirm is QtGui.QMessageBox.StandardButton.FirstButton:
            self.close()

    def openConfDialog(self):
        confdialog = confSoundDialog(self._soundcontainer, self, self._handler)
        confdialog.show()

    @property
    def active(self):
        self.ui.checkBox.isChecked()

    @active.setter
    def active(self, state):
        self.ui.checkBox.setChecked(state)

    def renamedCB(self):
        self.ui.soundButton.setText(
                self._soundcontainer.soundName(self._handler))

    #TODO: use a library for playing the media file
    def playSound(self):
        sfile = self.file
        if sfile is not None:
            import os
            if os.path.isfile(sfile):
                import subprocess
                import sys
                opts = ""
                if sys.platform == "win32":
                    player = "vlc"
                    opts = "--play-and-exit"
                    sfile = u"file:///" + sfile
                else:
                    player = "mplayer"
                subprocess.call([player, opts, sfile])
            else:
                self.active = False

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    sndcont = soundContainer()
    myapp = soundControl(soundcontainer=sndcont)
    myapp.show()
    sys.exit(app.exec_())
