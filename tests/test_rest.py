from __future__ import division

from babs import Rest


def test_create():
    assert Rest().value == 4/4
    assert Rest(value=1/4).value == 1/4


def test_repr():
    assert eval(repr(Rest())).value == 4 / 4
    assert eval(repr(Rest(value=3/4))).value == 3/4
