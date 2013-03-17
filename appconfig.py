from ConfigParser import SafeConfigParser as scp
import os

# configuration file format:
#===========================
# [General]
# version = 1.0
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
# [NameProfile1]
# <soundname> = on
# <soundname> = on
# <soundname> = off
# ...
#===========================

class appconfig():
    _conf = {
             'sounds': {},
             'active_profile':None,
             'profiles':{}
             }
    _configfile = None
    _configparser = None


    def appconfig(self, appname, appver, sounds, profiles, cprofile):
        if self._conf:
            return self._conf

        # TODO: use xdg-based config
        self._configfile = os.path.expanduser('~/.config/' + appname + 'cfg.ini')
        self._configparser = scp()
        if len(self._configparser.read(self._configfile)):
            self.readconfig()

        # TODO: copy self._conf subfields to params
        return self._conf


    def readconfig(self):
        cfgversion = self._configparser.get('General', 'version')
        if cfgversion <> '1.0':
            raise ValueError, "Unknown file format configuration version %s" % (cfgversion)

        self._conf['sounds'] = self._getsounds()

        profiles, cprofile = self._getprofiles()
        self._conf['profiles'] = profiles
        self._conf['active_profile'] = cprofile


    def _getsounds(self):

        sounds = {}
        if self._configparser.has_section('Sounds'):
            soundnames = self._configparser.options('Sounds')
            for s in soundnames:
                v = self._configparser.get('Sounds', s)
                sounds[s] = v
                # TODO: validate sound file; check no duplicates
        return sounds


    def _getprofiles(self):

        if self._configparser.has_section('Profiles'):
            try:
                profiles_list = self._configparser.options('Profiles')
            except NoSectionError:
                # TODO: no active_profile, no profiles
                return {}, None
            profiles = {}
            profilenames = [ self._configparser.get('Profiles', x) for x in profiles_list ]

            # get active profile
            active_profile = None
            try:
                active_profile = self._configparser.get('General', 'active_profile')
            except NoOptionError:
                active_profile = profilenames[0]
            if not active_profile in profilenames:
                active_profile = profilenames[0]

            for p in profilenames:
                if self._configparser.has_section(p):
                    p_sounds = self._configparser.options(p)
                    pd_sounds = { True: [],  False: [] }
                    if len(p_sounds) > 0 :
                        for s in p_sounds:
                            state = self._configparser.getboolean(p, s)
                            try:
                                self._conf['sounds'][s]
                                pd_sounds[state].append(s)
                            except KeyError:
                                # XXX: referred sound does not exist. what next?
                                pass
                    profiles[p] = pd_sounds
                else:
                    # XXX: what should be the right thing to do?
                    # create an empty section? remove the profile? ask the user?
                    pass
            return profiles, active_profile

        else:
            return {},  None

