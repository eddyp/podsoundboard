#!/usr/bin/env python
# -*- coding: utf-8 -*-

appname = 'PodSoundBoard'
appver = '0.2'
appauthor = 'eddyp'

osencoding = 'utf8'

import sys
from PySide import QtCore, QtGui

import logging
logging.basicConfig(filename=appname + '.log',level=logging.DEBUG)

from ui_mainwindow import Ui_MainWindow
from soundcontrol import soundControl

from appconfig import appconfig
from soundcontainer import soundContainer
from profilecontainer import profileContainer



class myMainWindow(QtGui.QMainWindow):

    _soundcontainer = None
    _profilecontainer = None

    def __init__(self, parent=None):
        logging.getLogger("mainwindow")

        QtGui.QMainWindow.__init__(self, parent)

        # TODO: add profiles
        self.ui = Ui_MainWindow()
        # TODO: split uiProfiles methods into another class
        # hack to make it seem the uiProfiles is in another class
        self._uiprofiles = self

        self._soundcontainer = soundContainer()
        self._profilecontainer = profileContainer(self._soundcontainer)

        self.ui.setupUi(self)

        self._appconf = appconfig(appname, appver)
        self._appconf.readconfig()
        self._config = self._appconf.config
        self.loadConfig(self._config)
        #self.updateActiveProfileUi()

        self._initSlots()

    def wipeOutConfig(self):
        """Cleanly destroys all existent sounds, profiles and sound controls"""
        self._profilecontainer.wipeOutProfiles()
        self._soundcontainer.wipeOutSounds()


    def loadConfig(self, config):
        """
        Loads into the interface the configuration defined by 'config'.
        'config' must be a dictionary in the format provided by appconfig.
        """

        self.wipeOutConfig()

        self._soundcontainer.loadSounds(config['sounds'])
        self._profilecontainer.loadProfiles(config['profiles'], config['active_profile'])

        self._refreshUIFromConfig()

    def updateActiveProfileUi(self):
        raise NotImplementedError("updating the profile UI is not implemented")

    def getProfileUiScrollArea(self, profile=None):
        logging.debug("profile = %s", profile)
        if profile is not None and profile != self._profilecontainer.activeprofile:
            raise Exception("Internal error: profile parameter was used")
        return self.ui.soundsScrollArea

    def getProfileUILayout(self, profile=None):
        if profile is not None and profile != self._profilecontainer.activeprofile:
            raise Exception("Internal error: profile parameter was used")
        return self.ui.verticalLayout_profile

    def uiAddSound2profile(self, soundName=None, soundFile=None, active=False, profile=None):
        """
        Adds soundName with soundFile to profile via UI interaction.
        The sound control is also created through this operation.
        """
        if profile is None:
            profile = self._profilecontainer.activeprofile
        handler = self._profilecontainer.addSound2Profile(soundName, soundFile, active, profile)

        uiProfileScrollArea = self._uiprofiles.getProfileUiScrollArea(profile)
        ctl = soundControl(self._soundcontainer, handler, uiProfileScrollArea, active)
        self._profilecontainer.linkSoundCtlInProfile(handler, ctl, profile)
        # TODO: delete spacer add again later
        profileuilayout = self._uiprofiles.getProfileUILayout(profile)
        profileuilayout.addWidget(ctl)

    def uiSaveConfig(self):
        logging.debug("Save config called, cfg = %s" % self._appconf.config)
        self._appconf.writeconfig()

    def _refreshUIFromConfig(self):
        logging.debug("Refreshing UI from given config")
        logging.debug("Config is: %s" % self._config)

        # TODO: do this for all profiles
        sounds = self._profilecontainer.getSoundsInProfile()
        scroll = self._uiprofiles.getProfileUiScrollArea()
        for s in sounds:
            state = self._profilecontainer.getSoundState(s)
            sctl = soundControl(self._soundcontainer, s, scroll, state)
            self._uiprofiles.getProfileUILayout().addWidget(sctl)

    def uiLoadConfig(self):
        logging.debug("Load config called")
        self._appconf.readconfig()
        self._config = self._appconf.config
        self.loadConfig(self._config)
        self._refreshUIFromConfig()

    def _initSlots(self):
        QtCore.QObject.connect(self.ui.soundAddButton,
                               QtCore.SIGNAL("clicked()"),
                               self.uiAddSound2profile
                              )
        QtCore.QObject.connect(self.ui.actionSave,
                               QtCore.SIGNAL("activated()"),
                               self.uiSaveConfig
                              )
        QtCore.QObject.connect(self.ui.actionLoad,
                               QtCore.SIGNAL("activated()"),
                               self.uiLoadConfig
                              )


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = myMainWindow()
    myapp.show()
    sys.exit(app.exec_())
