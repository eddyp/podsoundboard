#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PySide import QtCore, QtGui

from ui_mainwindow import Ui_MainWindow
from qsoundcontrol import QSoundControl

class myMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self._sounds = []
        self.qsndctls = []
        self._currentProfile = -1
        self.profiles = []
        self.profileNames = []

        #TODO: add profiles
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        #TODO: init from app config files
##        ip = self.addProfile('Profil')
##        sp = self.addSound2Profile("S1", ip)
##        sp = self.addSound2Profile("S1", ip)
        self.addSound2Profile("S1")
        self.addSound2Profile("S1")
        self.addSound2Profile("S1")
        self.addSound2Profile("S1")

        self.initSlots()


    def addProfile(self, profileName='Profile'):
        ip = len(self.profiles)
        self.profiles.append([])
        self.profileNames.append(profileName)
        self._currentProfile = ip
        return ip


    def addSound2Profile(self, soundName="Sound", profileIndex=None):

        if profileIndex is None:
            profileIndex = self._currentProfile

        # if there are no profiles, create one
        if profileIndex == -1:
            profileIndex = self.addProfile()

        try:
            p = self.profiles[profileIndex]
        except IndexError:
            # TODO: debug statement
            raise IndexError, "Internal error: inexistent profile index selected"

        # new sound's index
        sp = len(p)
        p.append(QSoundControl(self.ui.soundsScrollArea, self, soundName))
        #TODO: detect duplicate names
        p[sp].setObjectName(soundName)
        self.ui.verticalLayout_profile.addWidget(p[sp])
        return sp


    def initSlots(self):
        QtCore.QObject.connect(self.ui.soundAddButton, QtCore.SIGNAL("clicked()"), self.addSound2Profile)

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
