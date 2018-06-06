import pytest

from babs import Note, Chord
from babs.exceptions import ChordException


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

    assert "Chords must have at least two notes, 0 given." == str(exc.value)

    with pytest.raises(ChordException) as exc:
        Chord(Note(name='C'))

    assert "Chords must have at least two notes, 1 given." == str(exc.value)

    with pytest.raises(ChordException) as exc:
        Chord('a', 'b')

    assert "Invalid Chord, instance of note expected but str given." == str(exc.value)


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


def test_add_note():
    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))
    c.add_note(note=Note(name='B'))
    assert len(c.notes) == 4
    assert Note(name='B') in c.notes

    c.add_note(note=Note(name='C'))
    assert len(c.notes) == 4

    c.add_note(note=Note(name='C', octave=5))
    assert len(c.notes) == 5
    assert Note(name='C', octave=5) in c.notes

    with pytest.raises(ChordException) as exc:
        Chord('a', 'b', strict=False).add_note('c')

    assert "Instance of Note expected, str given." == str(exc.value)


def test_add_note_not_strict():
    c = Chord('a', 'b', strict=False)
    c.add_note('c', strict=False)

    assert len(c.notes) == 3

    c.add_note('d', strict=False)

    assert len(c.notes) == 4


def test_remove_note_by_note():
    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))
    c.remove_note(note=Note(name='C', octave=5))

    assert len(c.notes) == 3
    assert Note(name='C') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='C', octave=5) not in c.notes

    c.remove_note(note=Note(name='E'))
    assert len(c.notes) == 2
    assert Note(name='G') in c.notes
    assert Note(name='C') in c.notes
    assert Note(name='E') not in c.notes

    with pytest.raises(ChordException) as exc:
        c.remove_note(note=Note(name='D'))

    assert len(c.notes) == 2
    assert Note(name='G') in c.notes
    assert Note(name='C') in c.notes
    assert "Invalid request. Note not found in Chord." == str(exc.value)

    with pytest.raises(ChordException) as exc:
        c.remove_note(note=Note(name='C'))

    assert len(c.notes) == 2
    assert Note(name='G') in c.notes
    assert Note(name='C') in c.notes
    assert "Invalid request. Chords must have at least two notes." == str(exc.value)

    with pytest.raises(ChordException) as exc:
        c.remove_note(note='a')

    assert "Instance of Note expected, str given." == str(exc.value)

    with pytest.raises(AttributeError) as exc:
        Chord('a', 'b', strict=False).remove_note(note=Note(name='A'))

    assert "'str' object has no attribute 'freq'" == str(exc.value)


def remove_note_by_note_not_strict():
    c = Chord('a', 'b', strict=False)
    c.remove_note(note='a', strict=False)

    assert len(c.notes) == 1
    assert 'b' in c.notes
    assert 'a' not in c.notes

    c = Chord(Note(name='C'), Note(name='E'))
    c.remove_note(note=Note(name='C'), strict=False)

    assert len(c.notes) == 1
    assert Note(name='E') in c.notes

    c.remove_note(name='G', strict=False)
    assert len(c.notes) == 1
    assert Note(name='E') in c.notes


def test_remove_note_by_freq():
    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))
    c.remove_note(freq=523.25)  # C5

    assert len(c.notes) == 3
    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='C', octave=5) not in c.notes

    c.remove_note(freq=329.63)

    assert len(c.notes) == 2
    assert Note(name='C') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='E') not in c.notes
    assert Note(name='C', octave=5) not in c.notes

    with pytest.raises(ChordException) as exc:
        c.remove_note(freq=261.63)

    assert len(c.notes) == 2
    assert Note(name='C') in c.notes
    assert Note(name='G') in c.notes
    assert "Invalid request. Chords must have at least two notes." == str(exc.value)

    with pytest.raises(ChordException) as exc:
        c.remove_note(freq='a')

    assert "Invalid request. Note not found in Chord." == str(exc.value)

    c = Chord('a', 'b', strict=False)
    with pytest.raises(AttributeError) as exc:
        c.remove_note(freq=261.63)

    assert len(c.notes) == 2
    assert "'str' object has no attribute 'freq'" == str(exc.value)


def remove_note_by_freq_not_strict():
    c = Chord(Note(name='C'), Note(name='E'))
    c.remove_note(freq=261.63, strict=False)

    assert len(c.notes) == 1
    assert Note(name='E') in c.notes

    c.remove_note(freq=440, strict=False)
    assert len(c.notes) == 1
    assert Note(name='E') in c.notes


def test_remove_note_by_name():
    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='B'), Note(name='C', octave=5))
    c.remove_note(name='C')

    assert len(c.notes) == 3
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='B') in c.notes
    assert Note(name='C') not in c.notes

    c.remove_note(name='B')
    assert len(c.notes) == 2
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='B') not in c.notes

    with pytest.raises(ChordException) as exc:
        c.remove_note(name='E')

    assert len(c.notes) == 2
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert "Invalid request. Chords must have at least two notes." == str(exc.value)

    with pytest.raises(ChordException) as exc:
        c.remove_note(name='F')

    assert len(c.notes) == 2
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert "Invalid request. Note not found in Chord." == str(exc.value)


def test_remove_note_by_name_not_strict():
    c = Chord(Note(name='C'), Note(name='E'))
    c.remove_note(name='C', strict=False)

    assert len(c.notes) == 1
    assert Note(name='E') in c.notes

    c.remove_note(name='G', strict=False)
    assert len(c.notes) == 1
    assert Note(name='E') in c.notes


def test_remove_note_by_octave():
    c = Chord(Note(name='B', octave=3), Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))
    c.remove_note(octave=5)

    assert len(c.notes) == 4
    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='B', octave=3) in c.notes
    assert Note(name='C', octave=5) not in c.notes

    c.remove_note(octave=3)

    assert len(c.notes) == 3
    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='B', octave=3) not in c.notes

    with pytest.raises(ChordException) as exc:
        c.remove_note(octave=3)

    assert len(c.notes) == 3
    assert "Invalid request. Note not found in Chord." == str(exc.value)

    with pytest.raises(ChordException) as exc:
        c.remove_note(octave=4)

    assert len(c.notes) == 3
    assert "Invalid request. Chords must have at least two notes." == str(exc.value)


def test_remove_note_by_octave_not_strict():
    c = Chord(Note(name='C'), Note(name='C', octave=5))
    c.remove_note(octave=4, strict=False)

    assert len(c.notes) == 1
    assert Note(name='C', octave=5) in c.notes

    c.remove_note(octave=3, strict=False)
    assert len(c.notes) == 1
    assert Note(name='C', octave=5) in c.notes


def test_remove_note_no_args():
    with pytest.raises(ChordException) as exc:
        Chord(Note(name='C'), Note(name='E'), Note(name='G')).remove_note()

    assert "Invalid request. Note not found in Chord." == str(exc.value)

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))
    c.remove_note(strict=False)
    assert len(c.notes) == 3
    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes


def test_eq():
    assert \
        Chord(Note(name='C'), Note(name='E'), Note(name='G')) == \
        Chord(Note(name='C'), Note(name='E'), Note(name='G'))

    assert \
        Chord(Note(name='G'), Note(name='C'), Note(name='E')) == \
        Chord(Note(name='C'), Note(name='E'), Note(name='G'))

    assert not \
        Chord(Note(name='G'), Note(name='C'), Note(name='E'), Note(name='C', octave=5)) == \
        Chord(Note(name='C'), Note(name='E'), Note(name='G'))


def test_neq():
    assert \
        Chord(Note(name='G'), Note(name='C'), Note(name='E'), Note(name='C', octave=5)) != \
        Chord(Note(name='C'), Note(name='E'), Note(name='G'))

    assert not \
        Chord(Note(name='C'), Note(name='E'), Note(name='G')) != \
        Chord(Note(name='C'), Note(name='E'), Note(name='G'))

    assert not \
        Chord(Note(name='G'), Note(name='E'), Note(name='C')) != \
        Chord(Note(name='C'), Note(name='E'), Note(name='G'))


def test_str():
    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))
    assert 'C4' in str(c).split(',')
    assert 'E4' in str(c).split(',')
    assert 'G4' in str(c).split(',')

    c.add_note(note=Note(name='C', octave=5))
    assert 'C4' in str(c).split(',')
    assert 'E4' in str(c).split(',')
    assert 'G4' in str(c).split(',')
    assert 'C5' in str(c).split(',')


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
    c = Chord.create_from_root(root=Note(name='C', alt='sharp'), chord_type=Chord.MINOR_TYPE)

    for n in c.notes:
        assert n.alt == 'sharp'
        if n == Note(name='D#'):
            assert str(n) == 'D#4'

    c = Chord.create_from_root(root=Note(name='C', alt='flat'), chord_type=Chord.MINOR_TYPE, alt='flat')

    for n in c.notes:
        assert n.alt == 'flat'
        if n == Note(name='Eb'):
            assert str(n) == 'Eb4'


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
