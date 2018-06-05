from __future__ import division

from babs import Rest


def test_create():
    assert Rest().value == 4/4
    assert Rest(value=1/4).value == 1/4


def test_repr():
    assert eval(repr(Rest())).value == 4 / 4
    assert eval(repr(Rest(value=3/4))).value == 3/4


def test_eq():
    assert Rest() == Rest()
    assert Rest(value=1/8) == Rest(value=1/8)
    assert not Rest() == Rest(value=1/8)


def test_neq():
    assert not Rest() != Rest()
    assert not Rest(value=1/8) != Rest(value=1/8)
    assert Rest() != Rest(value=1/8)


def test_lt():
    assert Rest(value=1/8) < Rest()
    assert Rest(value=1/16) < Rest(value=1/8)
    assert not Rest() < Rest()
    assert not Rest(value=1/4) < Rest(value=1/8)


def test_lte():
    assert Rest() <= Rest()
    assert Rest(value=1 / 8) <= Rest(value=1 / 8)
    assert Rest(value=1/16) <= Rest(value=1/8)
    assert not Rest(value=1/4) <= Rest(value=1/8)


def test_gt():
    assert Rest() > Rest(value=1/8)
    assert Rest(value=1/8) > Rest(value=1/16)
    assert not Rest() > Rest()
    assert not Rest(value=1/8) > Rest(value=1/4)


def test_gte():
    assert Rest() >= Rest()
    assert Rest(value=1/8) >= Rest(value=1/8)
    assert Rest(value=1/8) >= Rest(value=1/16)
    assert not Rest(value=1/8) >= Rest(value=1/4)
