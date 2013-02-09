from PySide import QtCore, QtGui

from ui_soundcontrol import Ui_QSoundControl

class QSoundControl(QtGui.QWidget):

    def __init__(self, parent=None, name='soundxxx', mp3=None, flac=None):
        self._name = name
        self.parent = parent

        QtGui.QWidget.__init__(self, parent)

        if parent:
            if parent.hasName(self.name):
                self.name = parent.getNewName(self.name)
            parent.register(self, self.name)

        self.ui = Ui_QSoundControl()
        self.ui.setupUi(self)

    def __del__(self):
        if self.parent:
            self.parent.unregister(self, self.name)

    #TODO: add actual code for QSoundControl

