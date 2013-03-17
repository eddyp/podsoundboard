#!/usr/bin/env python
# -*- coding: utf-8 -*-

appname = 'PodSoundBoard'
appver = '0.1'
appauthor = 'eddyp'

import sys
from PySide import QtCore, QtGui

from ui_mainwindow import Ui_MainWindow
from soundcontrol import soundControl

from appconfig import appconfig

class myMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # TODO: keep everything together in dictionaries
        self._sounds = []              # all sound names
        self.qsndctls = []             # list of dicts with 'name' and 'ctl' keys
        self._currentProfileIndex = -1 # active profile
        self.profiles = []             # will contain a list of sound controls
        self.profileNames = []         # all profile names
        #self._conf = {}

        # TODO: add profiles
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        config = appconfig(appname, appver)

        self.initSlots()

    def addProfile(self, profileName='Profile'):
        ip = len(self.profiles)
        self.profiles.append([])
        self.profileNames.append(profileName)
        self._currentProfileIndex = ip
        return ip


    def addSound2Profile(self, soundName="Sound", profileIndex=None):

        if profileIndex is None:
            profileIndex = self._currentProfileIndex

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
        p.append(soundControl(self.ui.soundsScrollArea, self, soundName))
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
