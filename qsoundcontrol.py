from PySide import QtCore, QtGui

from ui_soundcontrol import Ui_QSoundControl

class QSoundControl(QtGui.QWidget):

    def __init__(self, parent=None, name='sound', mp3=None, flac=None):
        self._name = name
        self.parent = parent
        self.text = name

        QtGui.QWidget.__init__(self, parent)

        if parent:
            if parent.hasSound(self.name):
                self.name = parent.getNewSoundName(self.name)
            parent.register(self, self.name)

        self.ui = Ui_QSoundControl()
        self.ui.setupUi(self)

    def __del__(self):
        if self.parent:
            try:
                self.parent.unregister(self, self.name)
            except AttributeError:
                #TODO: warn about the inconsistency
                pass

    #TODO: add actual code for QSoundControl

