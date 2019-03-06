import pytest

from babs import Note, Chord
from babs.exceptions import ChordException, NoteListException


def test_create():
    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))
    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert len(c.notes) == 3

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C'))
    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert len(c.notes) == 3

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))
    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='C', octave=5) in c.notes
    assert len(c.notes) == 4

    with pytest.raises(ChordException) as exc:
        Chord()

    assert 'Chords must have at least two notes, 0 given.' == str(exc.value)

    with pytest.raises(ChordException) as exc:
        Chord(Note(name='C'))

    assert 'Chords must have at least two notes, 1 given.' == str(exc.value)


def test_create_not_strict():
    assert len(Chord(strict=False).notes) == 0
    assert len(Chord(Note(name='C'), strict=False).notes) == 1

    c = Chord('a', 'b', strict=False)
    assert len(c.notes) == 2
    assert 'a' in c.notes
    assert 'b' in c.notes


def test_set_notes_attribute():
    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))
    with pytest.raises(AttributeError) as exc:
        c.notes = [Note(name='B')]

    assert "can't set attribute" == str(exc.value)


def test_is_valid():
    assert Chord(strict=False).is_valid() is False
    assert Chord(Note(name='C'), strict=False).is_valid() is False
    assert Chord('a', 'b', strict=False).is_valid() is False

    assert Chord(Note(name='C'), Note(name='E')).is_valid() is True

    c = Chord(Note(name='C'), Note(name='E'))
    assert c.is_valid() is True

    assert Chord(Note(name='C'), strict=False).is_valid() is False


def test_repr():
    c = eval(repr(Chord(Note(name='C'), Note(name='E'), Note(name='G'))))
    assert c == Chord(Note(name='C'), Note(name='E'), Note(name='G'))
    assert c.strict is True

    c = eval(repr(Chord(
        Note(name='C'),
        strict=False
    )))

    assert c == Chord(Note(name='C'), strict=False)
    assert c.strict is False


def test_create_from_root():
    c = Chord.create_from_root(root=Note(name='C'))

    assert len(c.notes) == 3
    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes

    c = Chord.create_from_root(root=Note(name='G'))

    assert len(c.notes) == 3
    assert Note(name='G') in c.notes
    assert Note(name='B') in c.notes
    assert Note(name='D') in c.notes

    c = Chord.create_from_root(root=Note(name='G', octave=3))

    assert Note(name='G', octave=3) in c.notes
    assert Note(name='B', octave=3) in c.notes
    assert Note(name='D', octave=3) in c.notes


def test_create_from_root_with_chord_type():
    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MAJOR_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MAJOR_SEVEN_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='B') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MINOR_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='Eb') in c.notes
    assert Note(name='G') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MINOR_SEVEN_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='Eb') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='Bb') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.DOMINANT_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='Bb') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MINOR_MAJOR_SEVEN_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='Eb') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='B') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.HALF_DIMINISHED_SEVEN_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='Eb') in c.notes
    assert Note(name='Gb') in c.notes
    assert Note(name='Bb') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.DIMINISHED_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='Eb') in c.notes
    assert Note(name='Gb') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.DIMINISHED_SEVEN_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='Eb') in c.notes
    assert Note(name='Gb') in c.notes
    assert Note(name='A') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.AUGMENTED_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G#') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.AUGMENTED_SEVEN_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G#') in c.notes
    assert Note(name='Bb') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.AUGMENTED_MAJOR_SEVEN_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G#') in c.notes
    assert Note(name='B') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MAJOR_SIXTH_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='A') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MINOR_SIXTH_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='Eb') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='A') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.SUS4_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='F') in c.notes
    assert Note(name='G') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.SUS4_SEVEN_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='F') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='Bb') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.SUS4_MAJOR_SEVEN_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='F') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='B') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.SUS2_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='D') in c.notes
    assert Note(name='G') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.SUS2_SEVEN_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='D') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='Bb') in c.notes

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.SUS2_MAJOR_SEVEN_TYPE)

    assert Note(name='C') in c.notes
    assert Note(name='D') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='B') in c.notes


def test_create_from_root_with_alt():
    c = Chord.create_from_root(root=Note(name='C', alt=Note.SHARP), chord_type=Chord.MINOR_TYPE)

    assert 'D#4' in str(c).split(',')

    c = Chord.create_from_root(root=Note(name='C', alt=Note.FLAT), chord_type=Chord.MINOR_TYPE, alt=Note.FLAT)

    assert 'Eb4' in str(c).split(',')


def test_create_from_root_with_from_root_octave():
    c = Chord.create_from_root(root=Note(name='G', octave=3), octave='from_root')

    assert Note(name='G', octave=3) in c.notes
    assert Note(name='B', octave=3) in c.notes
    assert Note(name='D', octave=4) in c.notes

    c = Chord.create_from_root(root=Note(name='F', octave=4), octave='from_root')

    assert Note(name='F', octave=4) in c.notes
    assert Note(name='A', octave=4) in c.notes
    assert Note(name='C', octave=5) in c.notes


def test_create_from_root_with_int_octave():
    c = Chord.create_from_root(root=Note(name='G', octave=3), octave=4)

    assert Note(name='G', octave=3) in c.notes
    assert Note(name='B', octave=4) in c.notes
    assert Note(name='D', octave=4) in c.notes

    c = Chord.create_from_root(root=Note(name='F', octave=4), octave=3)

    assert Note(name='F', octave=4) in c.notes
    assert Note(name='A', octave=3) in c.notes
    assert Note(name='C', octave=3) in c.notes


def test_create_from_root_with_callable_octave():
    c = Chord.create_from_root(root=Note(name='G', octave=3), octave=lambda root_octave, i, distance: i + 1)

    assert Note(name='G', octave=3) in c.notes
    assert Note(name='B', octave=1) in c.notes
    assert Note(name='D', octave=2) in c.notes

    c = Chord.create_from_root(root=Note(name='F', octave=4), octave=lambda root_octave, i, distance: root_octave + i + 1)

    assert Note(name='F', octave=4) in c.notes
    assert Note(name='A', octave=5) in c.notes
    assert Note(name='C', octave=6) in c.notes

    with pytest.raises(TypeError):
        Chord.create_from_root(root=Note(name='F', octave=4), octave=lambda: 'invalid')


def test_create_from_root_with_invalid_octave():
    c = Chord.create_from_root(root=Note(name='C'), octave='invalid')

    assert Note(name='C', octave=4) in c.notes
    assert Note(name='E', octave=4) in c.notes
    assert Note(name='G', octave=4) in c.notes
