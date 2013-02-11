#!/usr/bin/env python

import sys
from PySide import QtCore, QtGui

from ui_mainwindow import Ui_MainWindow
from qsoundcontrol import QSoundControl

class myMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self._sounds = []
        self.qsndctls = []
        self.profiles = []

        #TODO: add profiles
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        #TODO: init from app config files
        ip = len(self.profiles)
        self.profiles.append([])
        sp = len(self.profiles[ip])
        self.profiles[ip].append(QSoundControl(self.ui.soundsScrollArea, self, "S1"))
        self.profiles[ip][sp].setObjectName("S1")
        self.ui.verticalLayout_profile.addWidget(self.profiles[ip][sp])


    def hasSound(self, name):
        return (name in self._sounds)

    def getNewSoundName(self, name):
        #TODO: find a smart way to compute a new unique name        

        #TODO: this might fail to provide a good name when
        #      other than the last sound is removed
        return 'name%d' % (len(self._sounds)+1)

    def register(self, qsndctl, name):
        if not self.hasSound(name):
            self._sounds.append(name)
            self.qsndctls.append( {'name': name, 'ctl': qsndctl} )
        else:
            raise AttributeError("Name %s already exists" % name)

    def unregister(self, soundctl, name):
        if self.hasSound(name):
            self._sounds.remove(name)
            self.qsndctls.remove( {'name': name, 'ctl': soundctl} )
        else:
            #TODO: warning about inconsistency
            pass


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = myMainWindow()
    myapp.show()
    sys.exit(app.exec_())