# -*- coding: utf-8 -*-
import pytest
from conftest import *


def test_loadinexistent(tmpdir, monkeypatch):
    tcfg = str(tmpdir) + 'inexistent'
    monkeypatch.syspath_prepend('.')
    import appconfig
    appconf = appconfig.appconfig('TestApp', '0.1', tcfg)
    from ConfigParser import NoSectionError
    pytest.raises(IOError, "appconf.readconfig()")


@pytest.mark.parametrize(("sound"), [
                        {'name':u'S0', 'file':'s0.mp3'},
                        {'name':u'S1', 'file':'s1.mp3'}
                        ])
def test_saveload(tmpdir, monkeypatch, sound):
    import copy
    import os
    tcfg = xindir(tmpdir, 'new.cfg')

    monkeypatch.syspath_prepend('.')

    import appconfig
    appconf = appconfig.appconfig('TestApp', '0.1', tcfg)
    conf = appconf.config

    assert equaldicts(conf,
                      {'sounds': {}, 'profiles': {}, 'active_profile': None})

    sfile = xindir(tmpdir, sound['file'])
    conf['sounds'][sound['name']] = sfile
    # every sound file has to exist for the load to happen
    touch(sfile)
    assert os.path.isfile(sfile)

    refconf = copy.deepcopy(conf)

    appconf.writeconfig()
    assert os.path.isfile(tcfg)

    appconf2 = appconfig.appconfig('TestApp', '0.1', tcfg)
    appconf2.readconfig()
    newconf = appconf2.config

    assert equaldicts(newconf, refconf)
    assert newconf['sounds'][sound['name']] == sfile

    del newconf, refconf, appconf, appconf2, conf, tcfg


def soundlines(sdict):
    sl = []

    for k, v in sdict.items():
        line = u'%s = %s\n' % (k, v)
        sl.append(line)

    return sl


def profilelines(pdict):
    pl = []
    strs = {True: 'on', False: 'off'}

    for pn, dp in pdict.items():
        pl.append('[Profile.%s]\n' % pn)
        for state in [False, True]:
            if state in dp.keys():
                for sound in dp[state]:
                    pl.append('%s = %s\n' % (sound, strs[state]))
    return pl


@pytest.mark.parametrize(("cfg"), [
        {
        'sounds': {u's0':'S0.mp3', u's1':'S1.flac'},
        'profiles': {u'p0':{True: [u's0'], False: [u's1']}},
        'active_profile': None
        }
        ,
        {
        'sounds': {u'sună0':'S0.mp3', u'șuier1':'S1.flac'},
        'profiles': { u'p0':{ True: [u'sună0']}, u'p1': {True:[u'șuier1']} },
        'active_profile': None
        }
        ])
def test_saveconfig(tmpdir, cfg):
    import appconfig as apc
    appconfig = apc.appconfig
    import copy

    tcfg = xindir(tmpdir, 'save.cfg')

    print cfg
    ncfg = copy.deepcopy(cfg)
    ncfg['sounds'] = makesoundsindir(tmpdir, cfg['sounds'])
    print ncfg

    ac = appconfig('TestApp', '0.1', tcfg)
    ac.setconfig(ncfg)
    assert equaldicts(ac.config, ncfg)

    ac.writeconfig()

    # test expected lines are present
    expect = ['[Sounds]\n', '[Profiles]\n', '[General]\n']
    expect.extend(soundlines(ncfg['sounds']))
    expect.extend(profilelines(ncfg['profiles']))

    f = open(tcfg)
    for line in f:
        dline = line.decode(cfgenc)
        if dline in expect:
            expect.remove(dline)
    f.close()
    assert expect == []


@pytest.mark.parametrize(("cfg"), [
        {
        'sounds': {u's0':'S0.mp3', u's1':'S1.flac'},
        'profiles': {u'p0':{True: [u's0'], False: [u's1']}},
        'active_profile': None
        }
        ])
def test_cfgfromXDG(tmpdir, monkeypatch, cfg):
    """test config is correctly loaded if XDG_CONFIG_HOME is set"""
    import appconfig as apc
    appconfig = apc.appconfig
    import os
    import copy

    ncfg = copy.deepcopy(cfg)
    ncfg['sounds'] = makesoundsindir(tmpdir, cfg['sounds'])

    monkeypatch.setenv("XDG_CONFIG_HOME", tmpdir)
    testappname = 'TestApp'
    expectcfgdir = xindir(tmpdir, testappname)

    ac = appconfig(testappname, '0.1')
    ac.setconfig(ncfg)
    ac.writeconfig()

    expectcfg = xindir(expectcfgdir, 'config.ini')
    assert os.path.isfile(expectcfg) is True

    monkeypatch.undo()


# def test_setdefaultcfg():
#     # TODO: test default setCfgFilename
#     assert 0
#
#
# def test_badcfgversion():
#     assert 0
#
#
# def test_writeconfigincustomfile():
#     # TODO: proper save when calling writeconfig("some.file.cfg")
#     assert 0
#
#
# def test_validactiveprofile():
#     assert 0
#
#
# def test_wipeoutsections():
#     assert 0
#
#
# def test_relativefilnames():
#     assert 0
#
#
# def test_inexistentanddupsounds():
#     assert 0
#
#
# def test_profilescfg():
#     assert 0
#
#
# def test_readActiveProfile():
#     assert 0
