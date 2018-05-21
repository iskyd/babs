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

    n = Note(freq=493.88)
    assert n.name == 'B'
    assert n.freq == 493.88
    assert n.octave == 4

    n = Note(freq=1174.72)
    assert n.name == 'D'
    assert n.freq == 1174.72
    assert n.octave == 6

    n = Note(freq=261.64)
    assert n.name == 'C'
    assert n.freq == 261.64
    assert n.octave == 4

    n = Note(freq=220)
    assert n.name == 'A'
    assert n.freq == 220
    assert n.octave == 3

    n = Note(freq=466.16, alt='flat')
    assert n.name == 'Bb'
    assert n.freq == 466.16
    assert n.octave == 4

    n = Note(freq=466.16)
    assert n.name == 'A#'
    assert n.freq == 466.16
    assert n.octave == 4

    n = Note(freq=466.16, alt='sharp')
    assert n.name == 'A#'
    assert n.freq == 466.16
    assert n.octave == 4


def test_compare():
    assert Note(freq=440) == Note(freq=440)

    assert Note(freq=440) != Note(freq=880)

    assert Note(freq=440) < Note(freq=880)

    assert Note(freq=440) <= Note(freq=440)
    assert Note(freq=440) <= Note(freq=880)

    assert Note(freq=880) > Note(freq=440)

    assert Note(freq=440) >= Note(freq=440)
    assert Note(freq=880) >= Note(freq=440)


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

    n.freq = 466.16
    assert n.name == 'A#'
    assert n.freq == 466.16
    assert n.octave == 4

    n.freq = 622.25
    assert n.name == 'D#'
    assert n.freq == 622.25
    assert n.octave == 5

    with pytest.raises(ValueError):
        n.freq = 'string'


def test_pitch_shift():
    n = Note(freq=440)
    n.pitch_shift(val=53.88)
    assert n.name == 'B'
    assert n.freq == 493.88
    assert n.octave == 4

    n = Note(freq=440)
    n.pitch_shift(val=2, half_step=True)
    assert n.name == 'B'
    assert n.freq == 493.88
    assert n.octave == 4

    n = Note(freq=440)
    n.pitch_shift(val=1, octave=True)
    assert n.name == 'A'
    assert n.freq == 880
    assert n.octave == 5

    n = Note(freq=440)
    n.pitch_shift(val=2, octave=True)
    assert n.name == 'A'
    assert n.freq == 1760
    assert n.octave == 6

    n = Note(freq=440)
    n.pitch_shift(val=2, half_step=True, octave=True)
    assert n.name == 'B'
    assert n.freq == 493.88
    assert n.octave == 4

    n = Note(freq=440)
    n.pitch_shift(val=1, half_step=True)
    assert n.name == 'A#'
    assert n.freq == 466.16
    assert n.octave == 4

    n = Note(freq=440, alt='flat')
    n.pitch_shift(val=1, half_step=True, alt='sharp')
    assert n.name == 'A#'
    assert n.freq == 466.16
    assert n.octave == 4

    n = Note(freq=466.16, alt='sharp')
    n.pitch_shift(val=0, half_step=True, alt='flat')
    assert n.name == 'Bb'
    assert n.freq == 466.16
    assert n.octave == 4

    n = Note(freq=466.16, alt='sharp')
    n.pitch_shift(val=-1, half_step=True, octave=True)
    assert n.name == 'A'
    assert n.freq == 440
    assert n.octave == 4

    n = Note(freq=440)
    n.pitch_shift(val=-1, octave=True)
    assert n.name == 'A'
    assert n.freq == 220
    assert n.octave == 3

    with pytest.raises(TypeError):
        Note(freq=440).pitch_shift(val='string')

    with pytest.raises(TypeError):
        Note(freq=440).pitch_shift(val='string', half_step=True)

    with pytest.raises(TypeError):
        Note(freq=440).pitch_shift(val='string', octave=True)


def test_str():
    assert Note(freq=440).__str__() == 'A4'
    assert Note(freq=466.16).__str__() == 'A#4'
    assert Note(freq=466.16, alt='flat').__str__() == 'Bb4'
    assert Note(name='A').__str__() == 'A4'


def test_repr():
    n = eval(Note(name='A').__repr__())
    assert n.freq == 440
    assert n.name == 'A'
    assert n.octave == 4

    n = eval(Note(freq=466.16, alt='flat').__repr__())
    assert n.freq == 466.16
    assert n.name == 'Bb'
    assert n.octave == 4


def test_value():
    n = Note(name='A')
    assert n.value == 1/4

    n.value = 1/8
    assert n.value == 1/8

    assert Note(name='A', value=1/16).value == 1/16
