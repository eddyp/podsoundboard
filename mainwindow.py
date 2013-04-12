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

from os import path

class myMainWindow(QtGui.QMainWindow):

    _dictsounds = {}
    """
    _dictsounds: a dictionary of all the sounds in the application.
    Entry format: u'soundname': u'/path/to/sound/file'.
    """

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
    _autosoundcount = 0
    _autoprofcount = 0

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # TODO: add profiles
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        #appconf = appconfig(appname, appver)
        #config = appconf.config
        #self.dict_loadConfig(config)
        ##self.dict_updateActiveProfileUi()

        self.dict_initSlots()

    def dict_wipeOutConfig(self):
        """Cleanly destroys all existent sounds, profiles and sound controls"""
        self._dictsounds = {}
        self._currentprofilename = None
        self.dict_wipeOutProfiles()

    def dict_wipeOutProfiles(self):
        for up in self._dictprofiles.keys():
            for us in self._dictprofiles[up].keys():
                soundctl = self._dictprofiles[up][us]['ctl']
                if soundctl:
                    del soundctl
                del self._dictprofiles[up][us]

    def dict_loadSounds(self, cfgsounds):
        files = {}
        for k, v in cfgsounds:
            uv = v.decode(osencoding)
            uk = k.decode(osencoding)
            if uv in files:
                # TODO: warn about dup; files[uv] returns the name of the sound
                continue
            if path.isfile(uv):
                files[uv] = uk
                self._dictsounds[uk] = uv
            else:
                # TODO: warn about non-existent file
                pass

    def dict_loadCfgProfile(self, profile, cfgprofile):
        up = profile.decode(osencoding)
        if up in self._dictprofiles:
            # TODO: warn
            return
        self._dictprofiles[up] = {}
        for enabled in [ False, True ]:
            for s in cfgprofile[enabled]:
                us = s.decode(osencoding)
                if us in self._dictsounds:
                    self._dictprofiles[up][us] = {'state': enabled, 'ctl': None}

    def dict_loadProfiles(self, cfgprofiles):
        for p in cfgprofiles.keys():
            dict_loadCfgProfile(p, cfgprofiles[p])

    def dict_loadActiveProfile(self, activeprofile):
        uap = activeprofile.decode(osencoding)
        if uap in self._dictprofiles:
            self._currentprofilename = uap
        else:
            # TODO: warn about inconsistency
            plist = self._dictprofiles.keys()
            if len(plist)>0:
                self._currentprofilename = plist[0]
            else:
                self._currentprofilename = None

    def dict_loadConfig(self, config):
        """
        Loads into the interface the configuration defined by 'config'.
        'config' must be a dictionary in the format provided by appconfig.
        """

        self.dict_wipeOutConfig()

        self.dict_loadSounds(config['sounds'])
        self.dict_loadProfiles(config['profiles'])
        self.dict_loadActiveProfile(config['active_profile'])

    def hasSound(self, name):
        return (name in self._dictsounds)

    def dict_hasProfile(self, name):
        return (name in self._dictprofiles)

    def getSoundNameOfFile(self, file):
        if file == None:
            return None
        fn = file
        if type(file) != unicode:
            fn = file.decode(osencoding)
        fndict = dict([ [v, k] for k, v in self._dictsounds.items()])
        # we don't delete fndict[None] since we'd never get here if file==None
        return fndict.get(fn, None)

    def dict_addSound(self, name=None, file=None):
        """
        Adds a sound to the application and returns the name under which the
        sound was really added.
        If 'file' is already in the application under a different name, the
        existent sound name is returned.
        If 'name' is not given, then a unique name is chosen.

        Returns: the name under which it was really added in the application.
        """
        if file:
            # avoid duplicates
            cname = self.getSoundNameOfFile(file)
            if cname:
                return cname
        if name==None:
            name = self.getNewSoundName()
        self._dictsounds[name] = file
        return name

    def getNewSoundName(self):
        name = None
        while True:
            name = u'Sound' + str(self._autosoundcount)
            self._autosoundcount += 1
            if not self.hasSound(name):
                break
        return name

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
        if profile == None:
            pn = self._currentprofilename
            if pn == None:
                raise Exception, "No active profile exists to add sound to."
        # get the real name of the sound
        sname = self.dict_addSound(name, file)
        if sname in self._dictprofiles[pn]:
            # TODO: warn about overwrite
            raise Exception,  "Trying to add the same sound (%s) twice in profile" % sname
        self._dictprofiles[pn][sname] = { 'state': active, 'ctl': None }
        return sname

    def dict_updateActiveProfileUi(self):
        raise NotImplementedError("updating the profile UI is not implemented")

    def addProfile(self, profilename=None):
        pn = profilename
        if pn == None:
            pn = self.dict_getNewProfileName()
        if self.dict_hasProfile(pn):
            raise Exception, u"Profile %s is already in the application" % pn

    def uiAddSound2profile(self, soundName=None, soundFile=None, active=False, profile=None):
        if profile == None:
            profile = self._currentprofilename
        sname = self.addSound2Profile(soundName, soundFile, active, profile)

        uiProfileScrollArea = self.ui.soundsScrollArea
        uiProfileVerticalLayout = self.ui.verticalLayout_profile
        ctl = soundControl(uiProfileScrollArea, self, sname, self._dictsounds[sname], active)
        self._dictprofiles[profile][sname]['ctl'] = ctl
        # TODO: delete spacer add again later
        uiProfileVerticalLayout.addWidget(ctl)

    def dict_initSlots(self):
        QtCore.QObject.connect(self.ui.soundAddButton, \
                               QtCore.SIGNAL("clicked()"), \
                               self.uiAddSound2profile
                              )

    def updateSound(self, oldname, oldfile, newname, newfile):
        """
        Updates sound oldname:oldfile to be newname:newfile.
        If successfull, returns True; False otherwise.
        """
        if not self.hasSound(oldname):
            return False
        if self._dictsounds[oldname] != oldfile:
            return False
        if (oldname == newname) and (oldfile == newfile):
            return True
        self._dictsounds[newname] = newfile
        if oldname != newname:
            self.updateSoundInProfiles(oldname, newname)
            del self._dictsounds[oldname]
            return True

    def updateSoundInProfiles(self, oldsound, newsound):
        if oldsound == newsound:
            return
        for p in self._dictprofiles:
            if oldsound in p:
                p[newsound] = p[oldsound]
                p[newsound]['ctl'].rename(newsound)
                del p[oldsound]

    def register(self, qsndctl, name, profile=None):
        print "Missing implementation of %s" % __name__
        # TODO: implement profile based
        return

        #if not self.hasSound(name):
            #self._sounds.append(name)
            #self.qsndctls.append( {'name': name, 'ctl': qsndctl} )
        #else:
            #raise AttributeError("Name %s already exists" % name)

    def unregister(self, soundctl, name):
        print "Missing implementation of %s" % __name__
        # TODO: implement profile-based
        return

        if self.hasSound(name):
            del self._dictsounds[name]
            #self.qsndctls.remove( {'name': name, 'ctl': soundctl} )
        #else:
            ##TODO: warning about inconsistency
            #pass


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = myMainWindow()
    myapp.show()
    sys.exit(app.exec_())
