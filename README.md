PodSoundBoard
=============

PodSoundBoard - a sound effects board useful for live podcast mixing

This application is meant as a helper for podcasters who want to mix in pre-configured sounds directly into their recording or broadcasting. It does NOT apply any special effects over your input sound, it allows you to configure various profiles which can contain various prerecorded sounds and simply plays those on your default sound card.

The app doesn't do any mixing of its own, it is assumed the default sound card's output is connected (via software - e.g. jackd, or hardware) to a sound mixer.


Licensing
---------
Copyright: Eddy Petrișor \<eddy.petrisor+podsoundboard@gmail.com\>, 2013

License is GPLv3 or later. For the text of the GNU GPL version 3, see the Freesoftware Foundation site.


Features
--------

Implemented features
____________________

 * Import existing audio files as named sounds into the application
 * Enable/disable unused sounds in profile

Planned features
________________

 * Define/save/reuse sound set profiles
   * Application can have multiple profiles, one profile/podcast
 * Hide/show unused sounds
 * Extract clips from existing sounds, import as new sounds
    * think 'THAT single line from the whole movie'

All these are planned features for the basic version (the first usable version) and will be implemented roughly in the order presented above.

Extra features might include:
 * Configurable Stopwatch/timer for the entire broadcast and for each segment
    - think: show with timed segments of arbitrary durations;
    - e.g.: 30 min show with 4 segments of: 5, 10, 10 and 5 minutes
 * optionally, a custom icon/image for each of the sounds can be set
 * portable to Windows
 * accessible via a web interface

Typical layout of a studio using PodSoundBoard
----------------------------------------------


    +------------------+
    | computer running |      +-------+
    |                  +----->|       |
    |  PodSoundBoard   |      |       |
    +------------------+      |       |
                              | mixer +------->(recorder/broadcast)
           (microphone)------>|       |
           (microphone)------>|       |
                ...           |       |
           (microphone)------>|       |
                              +-------+


Installation
------------

PodSoundBoard is:
* written in Python
* uses PySide bindings for Qt4 as a portable GUI library
* going to use Phonon or gstreamer for playback (and sound extraction)
* Although PodSoundBoard uses Qt4, is **NOT** a KDE application!

Installation is not yet necessary, just 'make' to generate the ui_*.py code.

Run with 'python mainwindow.py' or 'make run'.


Dependencies
- - - - - - 
Application was developed on Debian GNU/Linux using:
* Python 2.7
* Pyside 1.1.1
* Qt 4.8.2



Known issues
------------

* PodSoundBoard is currently in prealpha stage, it doesn't do much, yet.
* Icons, although visible in QtDesigner, do not load; all icons are empty
* Menus and tooltips are in Romanian
  * I am writing this to be used on the podcast 'Sceptici în România'
     * http://podcast.sceptici.ro
  * there will be an English translation when the app is at least useful
* PodSoundBoard uses mplayer to play sounds
* Internal data structures are redundant/uncleanly separated and code is not pythonic enough


Contact
-------
Suggestions, ideas and patches are welcome.

E-mail: eddy.petrisor+podsoundboard@gmail.com

