#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser as scp
import os

# configuration file format:
#===========================
# [General]
# cfgversion = 1
# active_profile = <ActiveProfileName>
# [Sounds]
# <soundname> = <sound_filename>
# <soundname> = <sound_filename>
# <soundname> = <sound_filename>
# ...
# [Profiles]
# Profile.1 = NameProfile1
# Profile.2 = NameProfile2
# Profile.3 = NameProfile3
# ...
# [Profile.NameProfile1]
# <soundname> = on
# <soundname> = on
# <soundname> = off
# ...
#===========================

# TODO: use appdirs from Pypi
def user_config_dir(appname=None):
    path = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
    if appname:
        path = os.path.join(path, appname)
    return path

def user_data_dir(appname=None):
    path = os.getenv('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
    if appname:
        path = os.path.join(path, appname)
    return path

import logging


class appconfig(object):

    __GEN = 'General'
    __SNDS = 'Sounds'
    __PROFS = 'Profiles'
    __PRPREF = 'Profile.'



    def __init__(self, appname, appver, cfgfile=None):

        self._conf = {
                 'sounds': {},
                 'active_profile':None,
                 'profiles':{}
                 }
        self._configfile = None
        self._configparser = None

        self._appname = appname
        self._appver = appver
        self.setCfgFilename(cfgfile)

        self._configparser = scp()
        self._configparser.optionxform = str

    @property
    def config(self):
        u"""
        Config data structure has the following format:
            {
            'sounds' :
                        {
                        u'SName0' : u'/path/to/sname0/file',
                        u'SName1' : u'/path/to/sname1/file'
                        ...
                        },
            'profiles':
                        {
                        u'Profile0' :{
                            True  : [ u'EnabledSound0' , u'EnabledSound1' , ... ],
                            False : [ u'DisabledSoundA', u'DisabledSoundB', ... ]
                            },
                        ...
                        },
            'active_profile' : u'ProfileName'
            }
        """
        return self._conf

    def setCfgFilename(self, cfgfile=None):
        if cfgfile is None:
            dir = user_config_dir(self._appname)
            self._configfile = os.path.join(dir + 'config.ini')
        else:
            self._configfile = cfgfile

    def readconfig(self):
        self._configparser.read([self._configfile])
        cfgversion = self._configparser.getint(self.__GEN, 'cfgversion')
        # XXX: when more versions appear, the correct handling is to
        #      import the old version and ask the user if the migration is done
        if cfgversion <> self._getdefaultcfgver():
            raise ValueError, "Unknown file format configuration version %s" % (cfgversion)

        self._conf['sounds'] = self._getsounds()

        profiles, cprofile = self._getprofiles()
        self._conf['profiles'] = profiles
        self._conf['active_profile'] = cprofile

    def setconfig(self, conf):
        self._conf = conf

    def writeconfig(self, cfgfilename=None, appver='0.1', cfgver=None):
        if cfgver is None:
            cfgver = self._getdefaultcfgver(appver)
        if cfgfilename is not None:
            self.setCfgFilename(cfgfilename)

        self._wipeOutSections()
        self._check_and_add_section(self.__GEN)
        self._configparser.set(self.__GEN, 'cfgversion', str(cfgver))

        self._check_and_add_section(self.__SNDS)
        for k, v in self._conf['sounds'].items():
            logging.info("Writing sound >%s< = >%s<" % (k, v))
            self._configparser.set(self.__SNDS, k, v)

        self._set_profiles(self._conf['profiles'])

        if 'active_profile' in self._conf:
            if self._conf['active_profile'] is not None:
                if self._conf['active_profile'] in self._conf['profiles']:
                    self._configparser.set(self.__GEN,
                                            'active_profile',
                                            self._conf['active_profile']
                                            )

        # Writing our configuration file to 'example.cfg'
        with open(self._configfile, 'wb') as configfile:
            self._configparser.write(configfile)

    def _wipeOutSections(self):
        for s in self._configparser.sections():
            self._configparser.remove_section(s)

    def _set_profiles(self, profiles):
        self._check_and_add_section(self.__PROFS)

        for p in profiles:
            self._set_profile(p, profiles[p])

    def _set_profile(self, profname, profcfg):
        secname = self.__PRPREF + profname
        self._check_and_add_section(secname)

        statestr = { True: 'on',  False: 'off'}

        for state in (True, False):
            sstate = statestr[state]
            for s in profcfg[state]:
                self._configparser.set(secname, s, sstate)

    def _check_and_add_section(self, section):
        if not self._configparser.has_section(section):
            self._configparser.add_section(section)

    def _getdefaultcfgver(self, appver=None):
        expectver = {'0.1': 1}
        if appver is None:
            appver = self._appver
        # XXX: there should be an association between all
        #      appver-s and a cfgversion, without a huge dictionary
        ecv = expectver.get(appver, 1)
        return ecv

    def _getsounds(self):

        sounds = {}
        if self._configparser.has_section(self.__SNDS):
            soundnames = self._configparser.options(self.__SNDS)
            datadir = user_data_dir(self._appname)
            for s in soundnames:
                if not s in sounds.keys():
                    v = os.path.normpath(self._configparser.get(self.__SNDS, s))
                    if os.path.isabs(v):
                        fn = v
                    else:
                        fn = os.path.join(datadir, v)
                    # TODO: validate is a true sound file
                    if os.path.isfile(fn):
                        sounds[s] = fn
                        logging.info("Sound %s: Found file %s", s, fn)
                    else:
                        logging.warning("Sound %s: Inexistent file %s", s, fn)
                else:
                    logging.warning("Duplicate sound detected %s", s)
                    # XXX: report duplicate sound name
                    pass
        return sounds


    def _getprofiles(self):

        if self._configparser.has_section(self.__PROFS):
            # note that options in Profiles section are meaningless
            # only the values contain the actual profile names

            # TODO: make the options be the names, and values be boolean
            #       representing their visibility (which are open)

            profiles_list = self._configparser.options(self.__PROFS)
            if len(profiles_list) == 0:
                logging.warning("'%s' section is empty" % (self.__PROFS))
                return {}, None
            profiles = {}
            profilenames = [ self._configparser.get(self.__PROFS, x)
                                            for x in profiles_list ]

            if len(profilenames) == 0:
                logging.warning(
                    "The list of values in the '%s' section is empty",
                    self.__PROFS
                    )
                return {},  None

            # get active profile
            active_profile = self._readActiveProfile(profilenames)

            for p in profilenames:
                cfgp = self.__PRPREF + p
                if self._configparser.has_section(cfgp):
                    p_sounds = self._configparser.options(cfgp)
                    pd_sounds = { True: [],  False: [] }
                    if len(p_sounds) > 0 :
                        for s in p_sounds:
                            state = self._configparser.getboolean(cfgp, s)
                            try:
                                self._conf['sounds'][s]
                                pd_sounds[state].append(s)
                            except KeyError:
                                # XXX: referred sound does not exist. what next?
                                logging.warning("Found unknown sound %s in profile %s", s, p)
                                pass
                    profiles[p] = pd_sounds
                else:
                    # XXX: what should be the right thing to do?
                    # create an empty section? remove the profile? ask the user?
                    logging.warning("No section found for profile %s", p)
                    pass
            return profiles, active_profile

        else:
            logging.error("Mandatory configuration section '%s' not found"
                                % self.__PROFS)
            return {}, None

    def _readActiveProfile(self, profilenames):
        active_profile = None
        try:
            active_profile = self._configparser.get(self.__GEN,
                                                     'active_profile')
        except NoOptionError:
            logging.warning("No active profile specified in config, using first")
            active_profile = profilenames[0]
        if not active_profile in profilenames:
            logging.warning("The active profile specified in config doesn't exist, using first")
            active_profile = profilenames[0]
        return active_profile
