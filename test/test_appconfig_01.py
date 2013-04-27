import pytest
from conftest import *

def test_loadinexistent(tmpdir, monkeypatch):
    tcfg = str(tmpdir) + 'inexistent'
    monkeypatch.syspath_prepend('.')
    import appconfig
    appconf = appconfig.appconfig('TestApp', '0.1', tcfg)
    from ConfigParser import NoSectionError
    pytest.raises(NoSectionError, "appconf.readconfig()")

@pytest.mark.parametrize(("sound"), [
                        {'name':u'S0', 'file':'s0.mp3'},
                        {'name':u'S1', 'file':'s1.mp3'}
                        ])
def test_saveload(tmpdir, monkeypatch, sound):
    import copy, os
    monkeypatch.syspath_prepend('.')
    import appconfig
    tcfg = xindir(tmpdir, 'new.cfg')
    appconf = appconfig.appconfig('TestApp', '0.1', tcfg)
    conf = appconf.config
    assert equaldicts(conf,
                      {'sounds': {}, 'profiles':{}, 'active_profile':None})

    sfile = xindir(tmpdir, sound['file'])
    conf['sounds'][sound['name']] = sfile
    # every sound file has to exist for the load to happen
    touch(sfile)
    assert os.path.isfile(sfile)

    refconf = copy.deepcopy(conf)

    appconf.writeconfig()
    assert os.path.isfile(tcfg)
    appconf.readconfig()
    newconf = appconf.config

    assert equaldicts(newconf, refconf)
