#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 01.08.2013

@author: eddy
'''

osencoding = 'utf8'

import copy

from soundcontainer import soundContainer

class profileContainer(object):
    """
    Stores and handles all profile-related data storage and update API.
    """

    _soundcontainer = None

    _currentprofilename = u'Profil'
    _dictprofiles = {
                    u'Profil': {}
                    }
    """
    __dictprofiles: a dictionary of profiles.
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

    def __init__(self, soundcontainer, dictprofiles=None, activeprofile=None):

        self.__soundcontainer = soundcontainer
        if dictprofiles is not None:
            raise NotImplementedError("dictprofiles based initalization")
        else:
            self.__dictprofiles = copy.deepcopy(self._dictprofiles)
        self.__setActiveProfile(activeprofile)

    @property
    def activeprofile(self):
        return self.__currentprofilename

    @activeprofile.setter
    def activeprofile(self, prof):
        self.__setActiveProfile(prof)

    def dict_wipeOutProfiles(self):
        for up in self.__dictprofiles.keys():
            for us in self.__dictprofiles[up].keys():
                soundctl = self.__dictprofiles[up][us]['ctl']
                if soundctl:
                    del soundctl
                del self.__dictprofiles[up][us]

    def dict_loadCfgProfile(self, profile, cfgprofile):
        up = profile.decode(osencoding)
        if up in self.__dictprofiles:
            # TODO: warn
            return
        self.__dictprofiles[up] = {}
        for enabled in [False, True]:
            for s in cfgprofile[enabled]:
                us = s.decode(osencoding)
                if self.__soundcontainer.hasSound(us):
                    self.__dictprofiles[up][us] = {'state': enabled, 'ctl': None}

    def dict_loadProfiles(self, cfgprofiles):
        for p in cfgprofiles.keys():
            self.dict_loadCfgProfile(p, cfgprofiles[p])

    def __setActiveProfile(self, activeprofile):
        #print "Active profile: >%s< type: %s\n" % (activeprofile, type(activeprofile))
        if activeprofile is not None:
            uap = activeprofile.decode(osencoding)
            if uap in self.__dictprofiles:
                self.__currentprofilename = uap
                return
            else:
                # TODO: warn about inconsistency
                pass
        if len(self.__dictprofiles) > 0:
            self.__currentprofilename = self.__dictprofiles.keys()[0]
        else:
            self.__currentprofilename = None

    def dict_hasProfile(self, name):
        """Checks if the profile 'name' exists already"""
        return (name in self.__dictprofiles)

    def dict_getNewProfileName(self):
        """
        Return a new unique profile name.
        """
        name = None
        while True:
            name = u'Profile' + str(self._autoprofcount)
            self._autoprofcount += 1
            if not self.dict_hasProfile(name):
                break
        return name

    def addProfile(self, profilename=None):
        pn = profilename
        if pn is None:
            pn = self.dict_getNewProfileName()
        if self.dict_hasProfile(pn):
            raise Exception(u"Profile %s is already in the application" % pn)

    def addSound2Profile(self, name=None, file=None, active=False, profile=None):
        """
        Updates the internal data structures for the profile 'profile'
        (current, if None selected) with the sound 'name' which has the sound
        file with the filename 'file' and is in the state 'active'.

        If the sound 'name' exists already in the profile,
        an exception is raised.

        The sound control is NOT populated by this method.
        """

        # TODO: move this in a profile class
        pn = profile
        if profile is None:
            pn = self.__currentprofilename
            if pn is None:
                raise Exception, "No active profile exists to add sound to."
        # get the real name of the sound
        sname = self.__soundcontainer.addSound(name, file)
        if sname in self.__dictprofiles[pn]:
            # TODO: warn about overwrite
            raise Exception(
                "Trying to add the same sound (%s) twice in profile" % sname)
        self.__dictprofiles[pn][sname] = {'state': active, 'ctl': None}
        return sname

    def getProfile(self, pn):
        if pn is None:
            if self.activeprofile is not None:
                prof = self.activeprofile
            else:
                raise Exception("No profile exists to operate on")
        else:
            prof = pn
        return prof

    def delAllSoundCtrlsInProfile(self, pn = None):
        """
        Unlinks all sound controls in the given profile or the active one.
        This is useful on profile destruction or reloading.
        """
        prof = self.getProfile(pn)
        for s in self.__dictprofiles[prof].keys():
            octl = self.__dictprofiles[prof][s]['ctl']
            if octl is not None:
                del octl
            self.__dictprofiles[prof][s] = {'state': False, 'ctl': None}

    def linkSoundCtlInProfile(self, handler, ctl,  pn=None):
        """
        Links the soundContrl 'ctl' to the sound 'handler' in profile 'pn'
        """
        prof = self.getProfile(pn)
        self.__dictprofiles[prof][handler]['ctl'] = ctl

    def getSoundsInProfile(self, pn=None):
        prof = self.getProfile(pn)
        return self.__dictprofiles[prof].keys()

    def getSoundState(self, handler, pn=None):
        prof = self.getProfile(pn)
        return self.__dictprofiles[prof][handler]['state']
