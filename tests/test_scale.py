import pytest

from babs import Note, Scale


def test_create():
    s = Scale(Note(name='C'), Note(name='D'), Note(name='E'))
    assert Note(name='C') in s.notes
    assert Note(name='D') in s.notes
    assert Note(name='E') in s.notes
    assert len(s.notes) == 3

    s = Scale(Note(name='C'), Note(name='D'), Note(name='D'))
    assert Note(name='C') in s.notes
    assert Note(name='D') in s.notes
    assert len(s.notes) == 2

    s = Scale(Note(name='C'), Note(name='D'), Note(name='D', octave=5))
    assert Note(name='C') in s.notes
    assert Note(name='D') in s.notes
    assert Note(name='D', octave=5) in s.notes
    assert len(s.notes) == 3


def test_create_from_root():
    s = Scale.create_from_root(root=Note(name='C'))
    assert Note(name='C') in s.notes
    assert Note(name='D') in s.notes
    assert Note(name='E') in s.notes
    assert Note(name='F') in s.notes
    assert Note(name='G') in s.notes
    assert Note(name='A') in s.notes
    assert Note(name='B') in s.notes

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT)
    assert Note(name='C') in s.notes
    assert Note(name='D') in s.notes
    assert Note(name='Eb') in s.notes
    assert Note(name='F') in s.notes
    assert Note(name='G') in s.notes
    assert Note(name='Ab') in s.notes
    assert Note(name='Bb') in s.notes


def test_create_from_root_with_from_root_octave():
    s = Scale.create_from_root(root=Note(name='C', octave=3), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT, octave='from_root')
    assert Note(name='C', octave=3) in s.notes
    assert Note(name='D', octave=3) in s.notes
    assert Note(name='Eb', octave=3) in s.notes
    assert Note(name='F', octave=3) in s.notes
    assert Note(name='G', octave=3) in s.notes
    assert Note(name='Ab', octave=3) in s.notes
    assert Note(name='Bb', octave=3) in s.notes

    s = Scale.create_from_root(root=Note(name='F', octave=3), scale_type=Scale.MAJOR_TYPE, alt=Note.FLAT, octave='from_root')
    assert Note(name='F', octave=3) in s.notes
    assert Note(name='G', octave=3) in s.notes
    assert Note(name='A', octave=3) in s.notes
    assert Note(name='Bb', octave=3) in s.notes
    assert Note(name='C', octave=4) in s.notes
    assert Note(name='D', octave=4) in s.notes
    assert Note(name='E', octave=4) in s.notes


def test_create_from_root_with_callable_octave():
    s = Scale.create_from_root(root=Note(name='C', octave=3), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT, octave=lambda root_octave, i, distance: root_octave + 1)
    assert Note(name='C', octave=3) in s.notes
    assert Note(name='D', octave=4) in s.notes
    assert Note(name='Eb', octave=4) in s.notes
    assert Note(name='F', octave=4) in s.notes
    assert Note(name='G', octave=4) in s.notes
    assert Note(name='Ab', octave=4) in s.notes
    assert Note(name='Bb', octave=4) in s.notes


def test_create_from_root_with_int_octave():
    s = Scale.create_from_root(root=Note(name='C', octave=2), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT, octave=2)
    assert Note(name='C', octave=2) in s.notes
    assert Note(name='D', octave=2) in s.notes
    assert Note(name='Eb', octave=2) in s.notes
    assert Note(name='F', octave=2) in s.notes
    assert Note(name='G', octave=2) in s.notes
    assert Note(name='Ab', octave=2) in s.notes
    assert Note(name='Bb', octave=2) in s.notes


def test_create_from_root_with_none_octave():
    s = Scale.create_from_root(root=Note(name='C', octave=4), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT, octave=None)
    assert Note(name='C', octave=4) in s.notes
    assert Note(name='D', octave=4) in s.notes
    assert Note(name='Eb', octave=4) in s.notes
    assert Note(name='F', octave=4) in s.notes
    assert Note(name='G', octave=4) in s.notes
    assert Note(name='Ab', octave=4) in s.notes
    assert Note(name='Bb', octave=4) in s.notes
