import pytest

def test_loadinexistent(tmpdir, monkeypatch):
    tcfg = str(tmpdir) + 'inexistent'
    monkeypatch.syspath_prepend('.')
    import appconfig
    appconf = appconfig.appconfig('TestApp', '0.1', tcfg)
    from ConfigParser import NoSectionError
    pytest.raises(NoSectionError, "appconf.readconfig()")
