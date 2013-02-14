#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui

from ui_soundcontrol import Ui_QSoundControl

class QSoundControl(QtGui.QWidget, Ui_QSoundControl):

    def __init__(self, parent, parentform=None, name='sound', mp3=None, flac=None):
        self._name = name
        self.parentform = parentform
        self.text = name

        QtGui.QWidget.__init__(self, parentform)

        if parentform:
            if self.parentform.hasSound(self._name):
                self._name = self.parentform.getNewSoundName(self._name)
            self.parentform.register(self, self._name)

        self.ui = Ui_QSoundControl()
        self.ui.setupUi(self)

    def __del__(self):
        if self.parentform:
            try:
                self.parentform.unregister(self, self._name)
            except AttributeError:
                #TODO: warn about the inconsistency
                pass

    #TODO: add actual code for QSoundControl

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = QSoundControl()
    myapp.show()
    sys.exit(app.exec_())
