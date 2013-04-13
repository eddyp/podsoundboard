#!/usr/bin/env python
# -*- coding: utf-8 -*-

class soundContainer(object):
    """
    Stores and handles all sound-related lookup and updates.
    """

    __sounds = {}
    """
    __sounds: a dictionary of all the sounds in the application.
    Entry format: u'soundname': u'/path/to/sound/file'.
    """
    _autosoundcount = 0
    _soundids = {}

    def init(dictsound = {}):
        self._soundids = dict(zip(range(len(dictsound)), dictsound.keys()))
        self._autosoundcount = len(dictsound)
        self.__sounds = dictsound

    def dict_wipeOutSounds(self):
        self.__sounds = {}
        self._soundids = {}
        self._autosoundcount = 0

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
                self.__sounds[uk] = uv
            else:
                # TODO: warn about non-existent file
                pass

    def hasSound(self, name):
        return (name in self.__sounds)

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
        self.__sounds[name] = file
        return name

    def getNewSoundName(self):
        name = None
        while True:
            name = u'Sound' + str(self._autosoundcount)
            self._autosoundcount += 1
            if not self.hasSound(name):
                break
        return name

    def getSoundNameOfFile(self, file):
        if file == None:
            return None
        fn = file
        if type(file) != unicode:
            fn = file.decode(osencoding)
        fndict = dict([ [v, k] for k, v in self.__sounds.items()])
        # we don't delete fndict[None] since we'd never get here if file==None
        return fndict.get(fn, None)

    def updateSound(self, oldname, oldfile, newname, newfile):
        """
        Updates sound oldname:oldfile to be newname:newfile.
        If successfull, returns True; False otherwise.
        """
        if not self.hasSound(oldname):
            return False
        if self.__sounds[oldname] != oldfile:
            return False
        if (oldname == newname) and (oldfile == newfile):
            return True
        self.__sounds[newname] = newfile
        if oldname != newname:
            self.updateSoundInProfiles(oldname, newname)
            del self.__sounds[oldname]
            return True

    def fileOfSound(self, sound):
        return self.__sounds.get(sound, None)
