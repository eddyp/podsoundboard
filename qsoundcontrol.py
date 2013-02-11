from PySide import QtCore, QtGui

from ui_soundcontrol import Ui_QSoundControl

class QSoundControl(QtGui.QWidget, Ui_QSoundControl):

    def __init__(self, parent, parentform=None, name='sound', mp3=None, flac=None):
        self._name = name
        self.myparent = parentform
        self.text = name

        QtGui.QWidget.__init__(self, parentform)

        if parentform:
            if myparent.hasSound(self.name):
                self.name = myparent.getNewSoundName(self.name)
            myparent.register(self, self.name)

        self.ui = Ui_QSoundControl()
        self.ui.setupUi(self)

    def __del__(self):
        if self.myparent:
            try:
                self.myparent.unregister(self, self.name)
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
