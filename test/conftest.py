def equaldicts(d1, d2):
    assert type(d1) == type(d2)
    assert type(d1) == type({})
    assert d1.keys().sort() == d2.keys().sort()
    if d1 == {}:
        return True
    for k, v in d1.items():
        if type(v) == type({}):
            assert equaldicts(v, d2[k])
        else:
            assert v == d2[k]

    return True

def xindir(dir, x):
    from os import sep
    return str(dir) + sep + str(x)

def touch(fn):
    f = open(fn, 'w+')
    f.close()

def makesoundsindir(dir, sdict):
    nd = {}
    for k, v in sdict.items():
        sfile = xindir(dir, v)
        nd[k] = sfile
        touch(sfile)
    return nd
