#!/usr/bin/env python

import sys
from PySide import QtCore, QtGui

from ui_mainwindow import Ui_MainWindow

class myMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        sounds = []
        qsndctls = []
        #TODO: init from app config files
        #TODO: add profiles
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

    def hasSound(self, name):
        return (name in sounds)

    def getNewSoundName(self, name):
        #TODO: find a smart way to compute a new unique name        

        #TODO: this might fail to provide a good name when
        #      other than the last sound is removed
        return 'name%d' % (len(sounds)+1)

    def register(self, qsndctl, name):
        if not hasSound(name):
            self.sounds.append(name)
            self.qsndctls.append( {'name': name, 'ctl': qsndctl} )
        else:
            raise AttributeError("Name %s already exists" % name)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = myMainWindow()
    myapp.show()
    sys.exit(app.exec_())