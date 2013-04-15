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


class myMainWindow(QtGui.QMainWindow):

    _soundcontainer = None

    _currentprofilename = u'Profil'
    _dictprofiles = {
                    u'Profil': {}
                    }
    """
    _dictprofiles: a dictionary of profiles.
    Entry format:
        u'profilename': {
                        u'soundname1': { 'state':<st>, 'ctl': <ctl> }
                        u'soundname2': { 'state':<st>, 'ctl': <ctl> }
                        }
        <st>  - True/False - determines if the sound is enabled in the profile;
        <ctl> - None/soundControl - sound control of the sound
                                    value is None when profile has no UI
    """
    _autoprofcount = 0

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # TODO: add profiles
        self.ui = Ui_MainWindow()

        self._soundcontainer = soundContainer()

        self.ui.setupUi(self)

        appconf = appconfig(appname, appver)
        config = appconf.config
        self.dict_loadConfig(config)
        #self.dict_updateActiveProfileUi()

        self.dict_initSlots()

    def dict_wipeOutConfig(self):
        """Cleanly destroys all existent sounds, profiles and sound controls"""
        self._soundcontainer.wipeOutSounds()
        self._currentprofilename = None
        self.dict_wipeOutProfiles()

    def dict_wipeOutProfiles(self):
        for up in self._dictprofiles.keys():
            for us in self._dictprofiles[up].keys():
                soundctl = self._dictprofiles[up][us]['ctl']
                if soundctl:
                    del soundctl
                del self._dictprofiles[up][us]

    def dict_loadCfgProfile(self, profile, cfgprofile):
        up = profile.decode(osencoding)
        if up in self._dictprofiles:
            # TODO: warn
            return
        self._dictprofiles[up] = {}
        for enabled in [ False, True ]:
            for s in cfgprofile[enabled]:
                us = s.decode(osencoding)
                if self._soundcontainer.hasSound(us):
                    self._dictprofiles[up][us] = {'state': enabled, 'ctl': None}

    def dict_loadProfiles(self, cfgprofiles):
        for p in cfgprofiles.keys():
            self.dict_loadCfgProfile(p, cfgprofiles[p])

    def dict_loadActiveProfile(self, activeprofile):
        #print "Active profile: >%s< type: %s\n" % (activeprofile, type(activeprofile))
        if activeprofile is not None:
            uap = activeprofile.decode(osencoding)
            if uap in self._dictprofiles:
                self._currentprofilename = uap
                return
            else:
                # TODO: warn about inconsistency
                pass
        if len(self._dictprofiles)>0:
            self._currentprofilename = self._dictprofiles.keys()[0]
        else:
            self._currentprofilename = None

    def dict_loadConfig(self, config):
        """
        Loads into the interface the configuration defined by 'config'.
        'config' must be a dictionary in the format provided by appconfig.
        """

        self.dict_wipeOutConfig()

        self._soundcontainer.loadSounds(config['sounds'])
        self.dict_loadProfiles(config['profiles'])
        self.dict_loadActiveProfile(config['active_profile'])

    def dict_hasProfile(self, name):
        return (name in self._dictprofiles)

    def dict_getNewProfileName(self):
        name = None
        while True:
            name = u'Profile' + str(self._autoprofcount)
            self._autoprofcount += 1
            if not self.dict_hasProfile(name):
                break
        return name

    def addSound2Profile(self, name=None, file=None, active=False, profile=None):
        pn = profile
        if profile is None:
            pn = self._currentprofilename
            if pn is None:
                raise Exception, "No active profile exists to add sound to."
        # get the real name of the sound
        sname = self._soundcontainer.addSound(name, file)
        if sname in self._dictprofiles[pn]:
            # TODO: warn about overwrite
            raise Exception,  "Trying to add the same sound (%s) twice in profile" % sname
        self._dictprofiles[pn][sname] = { 'state': active, 'ctl': None }
        return sname

    def dict_updateActiveProfileUi(self):
        raise NotImplementedError("updating the profile UI is not implemented")

    def addProfile(self, profilename=None):
        pn = profilename
        if pn is None:
            pn = self.dict_getNewProfileName()
        if self.dict_hasProfile(pn):
            raise Exception, u"Profile %s is already in the application" % pn

    def uiAddSound2profile(self, soundName=None, soundFile=None, active=False, profile=None):
        if profile is None:
            profile = self._currentprofilename
        handler = self.addSound2Profile(soundName, soundFile, active, profile)

        uiProfileScrollArea = self.ui.soundsScrollArea
        uiProfileVerticalLayout = self.ui.verticalLayout_profile
        ctl = soundControl(self._soundcontainer, handler, uiProfileScrollArea, active)
        self._dictprofiles[profile][handler]['ctl'] = ctl
        # TODO: delete spacer add again later
        uiProfileVerticalLayout.addWidget(ctl)

    def dict_initSlots(self):
        QtCore.QObject.connect(self.ui.soundAddButton, \
                               QtCore.SIGNAL("clicked()"), \
                               self.uiAddSound2profile
                              )


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = myMainWindow()
    myapp.show()
    sys.exit(app.exec_())
