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
    __users = {}
    """
    lists all the registered UI elements of any sound
    Entry format:
        u'soundname': [ list, of, ui, objs, that, use, it ]
    """
    __idcnt = 0
    __handlers = {}

    def init(dictsound = {}):
        self.dict_loadSounds(dictsound)

    def dict_wipeOutSounds(self):
        self.__sounds = {}
        self.__handlers = {}
        self.__idcnt = 0

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
                self.__users[uk] = []
            else:
                # TODO: warn about non-existent file
                pass

    def hasSound(self, name):
        return (name in self.__sounds)

    def addSound(self, name=None, file=None):
        """
        Adds a sound to the application and returns the a handler for the sound.
        If 'file' is already in the application under a different name, a
        handler to the existent sound is returned.
        If 'name' is not given, then a unique name is chosen.
        If the 'name' already exists, a new unique name is chosen instead.

        Returns: a handler of the sound
        """
        if file:
            # avoid duplicates
            cname = self.getSoundNameOfFile(file)
            if cname:
                self.__handlers[self.__idcnt] = cname
                self.__idcnt += 1
                return self.__idcnt - 1
        if name==None or self.hasSound(name):
            name = self.getNewSoundName()
        self.__sounds[name] = file
        self.__users[name] = []
        self.__handlers[self.__idcnt] = name
        self.__idcnt += 1
        return self.__idcnt - 1

    def getNewSoundName(self):
        name = None
        autocount = 0
        while True:
            name = u'Sound' + str(autocount)
            autocount += 1
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
        if sound in self.__handlers:
            sound = self.__handlers[sound]
        return self.__sounds.get(sound, None)
