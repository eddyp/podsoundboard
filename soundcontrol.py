#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui

information = QtGui.QMessageBox.information
warning = QtGui.QMessageBox.warning
critical = QtGui.QMessageBox.critical

from ui_soundcontrol import Ui_soundControl
from confsounddialog import confSoundDialog

class soundControl(QtGui.QWidget):

    _file = None
    def __init__(self, parent, parentform=None, name=u'sound', file=None, active=False):
        self.parentform = parentform
        self._name = name
        if not self.parentform:
            self._file = file

        QtGui.QWidget.__init__(self, parentform)


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

    @property
    def file(self):
        if self.parentform:
            return self.parentform.fileOfSound(self._name)
        else:
            return self._file

    @file.setter
    def file(self, file):
        p = self.parentform
        if p:
            return p.updateSound(self._name, self.file, self._name, file)
        else:
            self._file = file

    def confirmClose(self):
        confirm = warning(self, "Confirmare", \
                            u"Sigur vrei să închizi " + self._name + "?", \
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel, \
                            QtGui.QMessageBox.Cancel)
        if confirm is QtGui.QMessageBox.StandardButton.FirstButton:
            self.close()

    def openConfDialog(self):
        information(self, "Info", \
                u"_name: '%s'\nfile: '%s'\ntype(_name): %s\ntype(file):%s\n" \
                % (self._name, self.file, type(self._name), type(self.file))
                )
        confdialog = confSoundDialog(self, self._name, self.file)
        confdialog.show()

    def setActive(self, state):
        self.ui.checkBox.setChecked(state)

    def setNameAndFile(self, name, file):
        oname = self._name
        #if self.parentform.hasSound(name)
        # TODO: update sound in parent
        if self.parentform:
            if self.parentform.updateSound(oname, self.file, name, file):
                self._name = name
                self.file = file
                self.ui.soundButton.setText(self._name)
                return True
            else:
                return False
        else:
            self._name = name
            self.file = file

    def rename(self, newname):
        self._name = newname
        self.ui.soundButton.setText(self._name)

    #TODO: use a library for playing the media file
    def playSound(self):
        if self._file:
            import os
            if os.path.isfile(self._file):
                import subprocess
                subprocess.call(["mplayer", self.file])
            else:
                self.setActive(False)

    def getSoundNameOfFile(self, file):
        if self.parentform and file:
            return self.parentform.getSoundNameOfFile(file)
        else:
            return None

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = soundControl(u'sunet')
    myapp.show()
    sys.exit(app.exec_())
