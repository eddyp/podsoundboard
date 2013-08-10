#!/usr/bin/env python
# -*- coding: utf-8 -*-

appname = 'PodSoundBoard'
appver = '0.2'
appauthor = 'eddyp'

osencoding = 'utf8'

import sys
from PySide import QtCore, QtGui

from ui_mainwindow import Ui_MainWindow
from soundcontrol import soundControl

from appconfig import appconfig
from soundcontainer import soundContainer
from profilecontainer import profileContainer


class myMainWindow(QtGui.QMainWindow):

    _soundcontainer = None
    _profilecontainer = None

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # TODO: add profiles
        self.ui = Ui_MainWindow()

        self._soundcontainer = soundContainer()
        self._profilecontainer = profileContainer(self._soundcontainer)

        self.ui.setupUi(self)

        self._appconf = appconfig(appname, appver)
        self._appconf.readconfig()
        self._config = self._appconf.config
        self.dict_loadConfig(self._config)
        #self.dict_updateActiveProfileUi()

        self.dict_initSlots()

    def dict_wipeOutConfig(self):
        """Cleanly destroys all existent sounds, profiles and sound controls"""
        self._soundcontainer.wipeOutSounds()
        self._profilecontainer._currentprofilename = None
        self._profilecontainer.dict_wipeOutProfiles()


    def dict_loadConfig(self, config):
        """
        Loads into the interface the configuration defined by 'config'.
        'config' must be a dictionary in the format provided by appconfig.
        """

        self.dict_wipeOutConfig()

        self._soundcontainer.loadSounds(config['sounds'])
        self._profilecontainer.dict_loadProfiles(config['profiles'])
        self._profilecontainer.activeprofile = config['active_profile']

    def dict_updateActiveProfileUi(self):
        raise NotImplementedError("updating the profile UI is not implemented")

    def uiAddSound2profile(self, soundName=None, soundFile=None, active=False, profile=None):
        """
        Adds soundName with soundFile to profile via UI interaction.
        The sound control is also created through this operation.
        """
        if profile is None:
            profile = self._profilecontainer.activeprofile
        handler = self._profilecontainer.addSound2Profile(soundName, soundFile, active, profile)

        uiProfileScrollArea = self.ui.soundsScrollArea
        uiProfileVerticalLayout = self.ui.verticalLayout_profile
        ctl = soundControl(self._soundcontainer, handler, uiProfileScrollArea, active)
        self._profilecontainer.linkSoundCtlInProfile(profile, handler, ctl)
        # TODO: delete spacer add again later
        uiProfileVerticalLayout.addWidget(ctl)

    def uiSaveConfig(self):
        self._appconf.writeconfig()

    def refreshFromConfig(self, cfg):
        #TODO: remove all UI objects and repopulate based on config
        pass

    def uiLoadConfig(self):
        self._appconf.readconfig()
        self._config = self._appconf.config
        self.dict_loadConfig(self._config)
        self.refreshFromConfig(self._config)

    def dict_initSlots(self):
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
