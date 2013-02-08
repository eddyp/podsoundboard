
class QSoundControl(QWidget):

    def __init__(self, parent=None, name='soundxxx', mp3=None, flac=None):
        self._name = name
        self.parent = parent
        if parent:
            if parent.hasName(self.name):
                self.name = parent.getNewName(self.name)
            parent.register(self, self.name)

    def __del__(self):
        if parent:
            parent.unregister(self, self.name)

    #TODO: add actual code for QSoundControl

