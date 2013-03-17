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
# [NameProfile1]
# <soundname> = on
# <soundname> = on
# <soundname> = off
# ...
#===========================

class appdirs:

    def user_config_dir(appname=None):
        path = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
        if appname:
            path = os.path.join(path, appname)
        return path


class appconfig():
    _conf = {
             'sounds': {},
             'active_profile':None,
             'profiles':{}
             }
    _configfile = None
    _configparser = None

    def appconfig(self, appname, appver, cfgfile=None):
        if self._conf:
            return self._conf

        if not cfgfile:
            dir = appdirs.user_config_dir(appname)
            self._configfile = os.path.join(dir + 'cfg.ini')
        else:
            self._configfile = cfgfile
        self._configparser = scp()
        if len(self._configparser.read(self._configfile)):
            self.readconfig(appver)

        # TODO: copy self._conf subfields to params
        return self._conf


    def readconfig(self, appver):
        cfgversion = self._configparser.get('General', 'cfgversion')
        # XXX: when more versions appear, the correct handling is to
        #      import the old version and ask the user if the migration is done
        if cfgversion <> self._getdefaultcfgver(appver):
            raise ValueError, "Unknown file format configuration version %s" % (cfgversion)

        self._conf['sounds'] = self._getsounds()

        profiles, cprofile = self._getprofiles()
        self._conf['profiles'] = profiles
        self._conf['active_profile'] = cprofile


    def _getdefaultcfgver(self, appver):
        expectver = {'0.1': 1}
        # XXX: there should be an association between all
        #      appver-s and a cfgversion, without a huge dictionary
        ecv = expectver.get(appver, 1)
        return ecv

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

