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
