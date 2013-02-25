from ConfigParser import SafeConfigParser as scp
import os

class appconfig():
    _conf = None
    _configfile = None
    _configparser = None

    def appconfig(self, appname, appver, sounds, profiles, cprofile):
        if self._conf:
            return self._conf

        # TODO: use xdg-based config
        self._configfile = os.path.expanduser('~/.config/' + appname)
        self._configparser = scp()
        if len(self._configparser.read(self._configfile)):
            self.readconfig()

        # TODO: copy self._conf subfields to params
        return self._conf


    def readconfig(self):
        # TODO: check config format version
        # TODO: read sounds
        # TODO: read profiles
        # TODO: set default profile
        pass
