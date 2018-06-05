from __future__ import division

import pytest

from babs import Note
from babs.exceptions import NoteException


def test_create_with_no_arguments():
    with pytest.raises(NoteException) as exc:
        Note()

    assert "Can't create a note without frequency or name." == str(exc.value)


def test_create_with_invalid_note_name():
    with pytest.raises(NoteException) as exc:
        Note(name='S')

    assert "Invalid note." == str(exc.value)

    with pytest.raises(NoteException) as exc:
        Note(name=3)

    assert "Invalid note." == str(exc.value)


def test_create_with_invalid_freq():
    with pytest.raises(ValueError):
        Note(freq='string')


def test_create_with_name():
    n = Note(name='A')
    assert n.name == 'A'
    assert n.freq == 440
    assert n.octave == 4

    n = Note(name='B')
    assert n.name == 'B'
    assert n.freq == 493.88
    assert n.octave == 4

    n = Note(name='B', octave=3)
    assert n.name == 'B'
    assert n.freq == 246.94
    assert n.octave == 3

    n = Note(name='D#', octave=5)
    assert n.name == 'D#'
    assert n.freq == 622.25
    assert n.octave == 5


def test_create_with_freq():
    n = Note(freq=440)
    assert n.name == 'A'
    assert n.freq == 440
    assert n.octave == 4

    n = Note(freq=246.94)
    assert n.name == 'B'
    assert n.freq == 246.94
    assert n.octave == 3

    n = Note(freq=466.16)
    assert n.name == 'A#'
    assert n.freq == 466.16
    assert n.octave == 4

    n = Note(freq=466.16, alt='flat')
    assert n.name == 'Bb'
    assert n.freq == 466.16
    assert n.octave == 4

    n = Note(freq=466.16, alt='sharp')
    assert n.name == 'A#'
    assert n.freq == 466.16
    assert n.octave == 4

    n = Note(freq=440, name='B', octave=2)
    assert n.name == 'A'
    assert n.freq == 440
    assert n.octave == 4


def test_eq():
    assert Note(freq=440) == Note(freq=440)
    assert not Note(freq=440) == Note(freq=440, value=1/8)
    assert Note(freq=440, value=1/8) == Note(freq=440, value=1/8)
    assert not Note(freq=440) == Note(freq=880)


def test_neq():
    assert Note(freq=440) != Note(freq=880)
    assert Note(freq=440) != Note(freq=440, value=1/8)
    assert not Note(freq=440) != Note(freq=440)
    assert not Note(freq=440, value=1/8) != Note(freq=440, value=1/8)


def test_change_alt():
    n = Note(freq=466.16, alt='sharp')

    assert n.name == 'A#'
    assert n.freq == 466.16
    assert n.octave == 4

    n.alt = 'flat'
    assert n.name == 'Bb'
    assert n.freq == 466.16
    assert n.octave == 4

    n.alt = 'random string'
    assert n.name == 'A#'
    assert n.freq == 466.16
    assert n.octave == 4


def test_change_freq():
    n = Note(freq=440)

    n.freq = 220
    assert n.name == 'A'
    assert n.freq == 220
    assert n.octave == 3

    n.freq = 622.25
    assert n.name == 'D#'
    assert n.freq == 622.25
    assert n.octave == 5

    with pytest.raises(ValueError):
        n.freq = 'string'


def test_pitch_shift():
    n = Note(freq=440)

    n.pitch_shift(value=53.88)
    assert n.name == 'B'
    assert n.freq == 493.88
    assert n.octave == 4

    n.pitch_shift(value=-53.88)
    assert n.name == 'A'
    assert n.freq == 440
    assert n.octave == 4

    n.pitch_shift(value=0)
    assert n.name == 'A'
    assert n.freq == 440
    assert n.octave == 4

    # Half step #

    n = Note(freq=440)

    n.pitch_shift(value=2, half_step=True)
    assert n.name == 'B'
    assert n.freq == 493.88
    assert n.octave == 4

    n.pitch_shift(value=-2, half_step=True)
    assert n.name == 'A'
    assert n.freq == 440
    assert n.octave == 4

    n.pitch_shift(value=0, half_step=True)
    assert n.name == 'A'
    assert n.freq == 440
    assert n.octave == 4

    n.alt = 'sharp'
    n.pitch_shift(value=1, half_step=True, alt='flat')
    assert n.name == 'Bb'
    assert n.freq == 466.16
    assert n.octave == 4

    n.pitch_shift(value=0, half_step=True, alt='sharp')
    assert n.name == 'A#'
    assert n.freq == 466.16
    assert n.octave == 4

    # Octave #

    n = Note(freq=440)
    n.pitch_shift(value=1, octave=True)
    assert n.name == 'A'
    assert n.freq == 880
    assert n.octave == 5

    n.pitch_shift(value=-2, octave=True)
    assert n.name == 'A'
    assert n.freq == 220
    assert n.octave == 3

    n.pitch_shift(value=0, octave=True)
    assert n.name == 'A'
    assert n.freq == 220
    assert n.octave == 3

    n = Note(freq=466.16)
    n.pitch_shift(value=1, octave=True, alt='flat')
    assert n.name == 'Bb'
    assert n.freq == 932.32
    assert n.octave == 5

    n.pitch_shift(value=-1, octave=True, alt='sharp')
    assert n.name == 'A#'
    assert n.freq == 466.16
    assert n.octave == 4

    with pytest.raises(TypeError):
        Note(freq=440).pitch_shift()

    with pytest.raises(TypeError):
        Note(freq=440).pitch_shift(value='string')

    with pytest.raises(TypeError):
        Note(freq=440).pitch_shift(value='string', half_step=True)

    with pytest.raises(TypeError):
        Note(freq=440).pitch_shift(value='string', octave=True)


def test_str():
    assert str(Note(freq=440)) == 'A4'
    assert str(Note(freq=932.32, alt='flat')) == 'Bb5'


def test_repr():
    n = eval(repr(Note(name='A')))
    assert n.freq == 440
    assert n.name == 'A'
    assert n.octave == 4
    assert n.value == 4/4

    n = eval(repr(Note(freq=932.32, alt='flat', value=1/8)))
    assert n.freq == 932.32
    assert n.name == 'Bb'
    assert n.octave == 5
    assert n.value == 1/8


def test_value():
    n = Note(name='A')
    assert n.value == 4/4

    n.value = 1/8
    assert n.value == 1/8

    assert Note(name='A', value=1/16).value == 1/16
