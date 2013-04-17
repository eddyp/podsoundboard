#!/usr/bin/env python
# -*- coding: utf-8 -*-

osencoding = 'utf8'

from os import path


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
    __idcnt = 1
    __handlers = {}

    def init(dictsound={}):
        self.loadSounds(dictsound)

    def wipeOutSounds(self):
        self.__sounds = {}
        self.__handlers = {}
        self.__users = {}
        self.__idcnt = 1

    def loadSounds(self, cfgsounds):
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
        Adds a sound to the application and returns a handler for the sound.
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
        if name is None or self.hasSound(name):
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
        if file is None:
            return None
        fn = file
        if type(file) != unicode:
            fn = file.decode(osencoding)
        fndict = dict([[v, k] for k, v in self.__sounds.items()])
        # we don't delete fndict[None] since we'd never get here if file==None
        return fndict.get(fn, None)

    def soundName(self, handler):
        return self.__handlers.get(handler, None)

    def renameSound(self, handler, newname):
        oname = self.__handlers[handler]
        if type(newname) != unicode:
            newname = newname.decode(osencoding)
        if oname == newname:
            return handler
        if self.hasSound(newname):
            return None

        for k, v in self.__handlers.items():
            if v == oname:
                self.__handlers[k] = newname
        self.__sounds[newname] = self.__sounds[oname]
        del self.__sounds[oname]
        self.__users[newname] = self.__users[oname]
        del self.__users[oname]
        for u in self.__users[newname]:
            u.renamedCB()
        return handler

    def changeFile(self, handler, file):
        if not self.validHandler(handler):
            return False
        if self.__sounds[self.__handlers[handler]] == file:
            return True
        cname = self.getSoundNameOfFile(file)
        if cname is not None:
                # file already exists
                return False
        self.__sounds[self.__handlers[handler]] = file
        return True

    def validHandler(self, handler):
        if not handler in self.__handlers:
            return False
        if not self.hasSound(self.__handlers[handler]):
            return False
        return True

    def updateNameAndFile(self, handler, name, file):
        """
        Updates sound with given handler to be newname:newfile.
        If successfull, returns True; False otherwise.
        """
        if not self.validHandler(handler):
            return False
        oname = self.__handlers[handler]
        if (oname == name) and (self.fileOfSound(oname) == file):
            return True

        # validate new data
        if self.hasSound(name):
            # new name is already used
            return False
        sname = self.getSoundNameOfFile(file)
        if sname is not None and sname != self.__handlers[handler]:
            # file already exists
            return False

        # everything checks out
        if self.changeFile(handler, file) and \
                    self.renameSound(handler, name) is not None:
            return True
        else:
            #raise Exception, "Unexpected file update fail"
            return False

    def fileOfSound(self, sound):
        if sound in self.__handlers:
            sound = self.__handlers[sound]
        return self.__sounds.get(sound, None)

    def register(self, handler, ui):
        if not self.validHandler(handler):
            return
        sname = self.__handlers[handler]
        if not ui in self.__users[sname]:
            self.__users[sname].append(ui)

    def unregister(self, handler, ui):
        if not self.validHandler(handler):
            return False
        sname = self.__handlers[handler]
        if ui in self.__users[sname]:
            self.__users[sname].remove(ui)
            return True
        else:
            return False

    def dump(self):
        for o in (self.__handlers, self.__sounds, self.__users):
            print ("%s\n%s\n" % (o.__str__, str(o)))
        return
