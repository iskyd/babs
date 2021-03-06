from __future__ import division

from babs import Rest


def test_create():
    assert Rest().duration == 4/4
    assert Rest(duration=1/4).duration == 1/4


def test_repr():
    assert eval(repr(Rest())).duration == 4 / 4
    assert eval(repr(Rest(duration=3/4))).duration == 3/4


def test_eq():
    assert Rest() == Rest()
    assert Rest(duration=1/8) == Rest(duration=1/8)
    assert not Rest() == Rest(duration=1/8)


def test_neq():
    assert not Rest() != Rest()
    assert not Rest(duration=1/8) != Rest(duration=1/8)
    assert Rest() != Rest(duration=1/8)


def test_lt():
    assert Rest(duration=1/8) < Rest()
    assert Rest(duration=1/16) < Rest(duration=1/8)
    assert not Rest() < Rest()
    assert not Rest(duration=1/4) < Rest(duration=1/8)


def test_lte():
    assert Rest() <= Rest()
    assert Rest(duration=1 / 8) <= Rest(duration=1 / 8)
    assert Rest(duration=1/16) <= Rest(duration=1/8)
    assert not Rest(duration=1/4) <= Rest(duration=1/8)


def test_gt():
    assert Rest() > Rest(duration=1/8)
    assert Rest(duration=1/8) > Rest(duration=1/16)
    assert not Rest() > Rest()
    assert not Rest(duration=1/8) > Rest(duration=1/4)


def test_gte():
    assert Rest() >= Rest()
    assert Rest(duration=1/8) >= Rest(duration=1/8)
    assert Rest(duration=1/8) >= Rest(duration=1/16)
    assert not Rest(duration=1/8) >= Rest(duration=1/4)
