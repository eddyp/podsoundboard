# -*- coding: utf-8 -*-
import pytest
from conftest import *

simple_cfg = {
                'sounds': {u's0': 'S0.mp3', u's1': 'S1.flac'},
                'profiles': {u'p0': {True: [u's0'], False: [u's1']}},
                'active_profile': u'p0'
             }
diacr_cfg = {
            'sounds': {u'sună0':'S0.mp3', u'șuier1':'S1.flac'},
            'profiles': { u'p0':{ True: [u'sună0']}, u'p1': {True:[u'șuier1']} },
            'active_profile': u'p0'
            }

TESTAPPNAME = 'TestApp'
TESTAPPVER = '0.1'


def test_loadinexistent(tmpdir, monkeypatch):
    tcfg = str(tmpdir) + 'inexistent'
    monkeypatch.syspath_prepend('.')
    import appconfig
    appconf = appconfig.appconfig('TestApp', TESTAPPVER, tcfg)
    from ConfigParser import NoSectionError
    pytest.raises(IOError, "appconf.readconfig()")
    monkeypatch.undo()


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
    appconf = appconfig.appconfig(TESTAPPNAME, TESTAPPVER, tcfg)
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

    appconf2 = appconfig.appconfig(TESTAPPNAME, TESTAPPVER, tcfg)
    appconf2.readconfig()
    newconf = appconf2.config

    assert equaldicts(newconf, refconf)
    assert newconf['sounds'][sound['name']] == sfile

    del newconf, refconf, appconf, appconf2, conf, tcfg
    monkeypatch.undo()


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


@pytest.mark.parametrize(("cfg"), [simple_cfg, diacr_cfg])
def test_saveconfig(tmpdir, cfg):
    import appconfig as apc
    appconfig = apc.appconfig
    import copy

    tcfg = xindir(tmpdir, 'save.cfg')

    print cfg
    ncfg = copy.deepcopy(cfg)
    ncfg['sounds'] = makesoundsindir(tmpdir, cfg['sounds'])
    print ncfg

    ac = appconfig(TESTAPPNAME, TESTAPPVER, tcfg)
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


@pytest.mark.parametrize(("cfg"), [simple_cfg])
def test_cfgfromXDG(tmpdir, monkeypatch, cfg):
    """test config is correctly loaded if XDG_CONFIG_HOME is set"""
    import appconfig as apc
    appconfig = apc.appconfig
    import os
    import copy
    writtencfg = copy.deepcopy(cfg)
    writtencfg['sounds'] = makesoundsindir(tmpdir, writtencfg['sounds'])
    monkeypatch.setenv("XDG_CONFIG_HOME", tmpdir)
    expectcfgdir = xindir(tmpdir, TESTAPPNAME)

    ac = appconfig(TESTAPPNAME, TESTAPPVER)
    ac.setconfig(writtencfg)
    ac.writeconfig()

    expectcfg = xindir(expectcfgdir, 'config.ini')
    assert os.path.isfile(expectcfg) is True

    readac = appconfig(TESTAPPNAME, TESTAPPVER)
    readac.readconfig()
    readconf = readac.config
    assert equaldicts(writtencfg, readconf)

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


@pytest.mark.parametrize(("cfg"), [simple_cfg])
def test_setActiveProfileWhenMissing(tmpdir, cfg):
    import appconfig as apc
    appconfig = apc.appconfig
    import os
    import copy
    writtencfg = copy.deepcopy(cfg)
    writtencfg['sounds'] = makesoundsindir(tmpdir, writtencfg['sounds'])
    writtencfg['active_profile'] = None
    cfgfile = xindir(tmpdir, 'cfg.ini')

    ac = appconfig(TESTAPPNAME, TESTAPPVER, cfgfile)
    ac.setconfig(writtencfg)
    ac.writeconfig()
    ac.readconfig()

    assert ac.config['active_profile'] == u'p0'
