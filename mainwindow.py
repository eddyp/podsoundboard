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

        self.initSounds()
        self.initProfiles()

        # TODO: add profiles
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        appconf = appconfig(appname, appver)
        config = appconf.getConfig()
        self._initSoundsFromConfig(config)
        self._initProfilesFromConfig(config)

        self.initSlots()

    # TODO: keep everything together in dictionaries
    def initSounds(self):
        self._sounds = []              # all sound names
        self.qsndctls = []             # list of dicts with 'name' and 'ctl' keys

    def initProfiles(self):
        self._currentProfileIndex = -1 # active profile
        self.profiles = []             # a list of lists containing sound controls
        self.profileNames = []         # all profile names
        #self._conf = {}

    def _initSoundsFromConfig(self, config):
        self.initSounds()
        if len(config['sounds'].keys()) > 0:
            self._sounds = config['sounds'].keys().sort()

    def _initProfilesFromConfig(self, config):
        self.initProfiles()
        # TODO: correctly delete all existent sound controls

        profiles = config['profiles'].keys()
        if len(profiles) > 0:
            for p in config['profiles'].keys().sort():
                idx = self.addProfile(p)
                for a in True, False:
                    for s in config[p][a]:
                        self.addSound2Profile(soundName=s, profileIndex=idx, active=a)
            self._currentProfileIndex = self.profileNames.index(config['active_profile'])
        # TODO: refresh GUI interface


    def addProfile(self, profileName='Profile'):
        ip = len(self.profiles)
        self.profiles.append([])
        self.profileNames.append(profileName)
        self._currentProfileIndex = ip
        return ip


    def addSound2Profile(self, soundName="Sound", profileIndex=None, soundfile=None, active=False):

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
        p.append(soundControl(self.ui.soundsScrollArea, self, soundName, soundfile, active))
        #TODO: detect duplicate names
        p[sp].setObjectName(soundName)
        self.ui.verticalLayout_profile.addWidget(p[sp])
        return sp


    def initSlots(self):
        QtCore.QObject.connect(self.ui.soundAddButton, QtCore.SIGNAL("clicked()"), self.addSound2Profile)

    def hasSound(self, name):
        return (name in self._sounds)

    def getSoundName(self, file):
        qscl = [ x['ctl']._name for x in self.qsndctls if x['ctl']._file == file ]
        s = len(qscl)
        if s>0:
            assert s == 1
            return qscl[0]
        else:
            return None

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
