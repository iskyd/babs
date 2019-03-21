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
    assert len(c.notes) == 4

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))
    assert Note(name='C') in c.notes
    assert Note(name='E') in c.notes
    assert Note(name='G') in c.notes
    assert Note(name='C', octave=5) in c.notes
    assert len(c.notes) == 4

    with pytest.raises(ChordException) as exc:
        Chord()

    assert 'Invalid Chord.' == str(exc.value)

    with pytest.raises(ChordException) as exc:
        Chord(Note(name='C'))

    assert 'Invalid Chord.' == str(exc.value)

    with pytest.raises(ChordException) as exc:
        Chord('invalid')

    assert 'Invalid Chord.' == str(exc.value)

    with pytest.raises(ChordException) as exc:
        Chord('invalid', 'invalid')

    assert 'Invalid Chord.' == str(exc.value)

def test_order_notes():
    c = Chord(Note(name='C'), Note(name='E'))
    assert c.notes[0] == Note(name='C')
    assert c.notes[1] == Note(name='E')

    c = Chord(Note(name='C'), Note(name='E', octave=3), strict=True)
    assert c.notes[0] == Note(name='E', octave=3)
    assert c.notes[1] == Note(name='C')

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), strict=True)
    assert c.notes[0] == Note(name='C')
    assert c.notes[1] == Note(name='E')
    assert c.notes[2] == Note(name='G')

    c = Chord(Note(name='A', octave=3), Note(name='F'), Note(name='C', octave=3), Note(name='E', octave=2), Note(name='E'))
    assert c.notes[0] == Note(name='E', octave=2)
    assert c.notes[1] == Note(name='C', octave=3)
    assert c.notes[2] == Note(name='A', octave=3)
    assert c.notes[3] == Note(name='E')
    assert c.notes[4] == Note(name='F')


def test_create_not_strict():
    try:
        assert len(Chord(strict=False).notes) == 0
        assert len(Chord(Note(name='C'), strict=False).notes) == 1

        c = Chord('a', 'b', strict=False)
        assert len(c.notes) == 2
        assert 'a' in c.notes
        assert 'b' in c.notes
    except ChordException:
        pytest.fail("Unexpected ChordException")


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

    assert Chord.create_from_root(root=Note(name='C')).strict is True
    assert Chord.create_from_root(root=Note(name='C'), strict=True).strict is True
    assert Chord.create_from_root(root=Note(name='C'), strict=False).strict is False


def test_create_from_root_with_chord_type():
    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MAJOR_TYPE)
    assert c == Chord(Note(name='C'), Note(name='E'), Note(name='G'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MAJOR_SEVEN_TYPE)
    assert c == Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='B'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MINOR_TYPE)
    assert c == Chord(Note(name='C'), Note(name='Eb'), Note(name='G'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MINOR_SEVEN_TYPE)
    assert c == Chord(Note(name='C'), Note(name='Eb'), Note(name='G'), Note(name='Bb'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.DOMINANT_TYPE)
    assert c == Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='Bb'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MINOR_MAJOR_SEVEN_TYPE)
    assert c == Chord(Note(name='C'), Note(name='Eb'), Note(name='G'), Note(name='B'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.HALF_DIMINISHED_SEVEN_TYPE)
    assert c == Chord(Note(name='C'), Note(name='Eb'), Note(name='Gb'), Note(name='Bb'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.DIMINISHED_TYPE)
    assert c == Chord(Note(name='C'), Note(name='Eb'), Note(name='Gb'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.DIMINISHED_SEVEN_TYPE)
    assert c == Chord(Note(name='C'), Note(name='Eb'), Note(name='Gb'), Note(name='A'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.AUGMENTED_TYPE)
    assert c == Chord(Note(name='C'), Note(name='E'), Note(name='G#'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.AUGMENTED_SEVEN_TYPE)
    assert c == Chord(Note(name='C'), Note(name='E'), Note(name='G#'), Note(name='Bb'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.AUGMENTED_MAJOR_SEVEN_TYPE)
    assert c == Chord(Note(name='C'), Note(name='E'), Note(name='G#'), Note(name='B'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MAJOR_SIXTH_TYPE)
    assert c == Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='A'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MINOR_SIXTH_TYPE)
    assert c == Chord(Note(name='C'), Note(name='Eb'), Note(name='G'), Note(name='A'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.SUS4_TYPE)
    assert c == Chord(Note(name='C'), Note(name='F'), Note(name='G'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.SUS4_SEVEN_TYPE)
    assert c == Chord(Note(name='C'), Note(name='F'), Note(name='G'), Note(name='Bb'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.SUS4_MAJOR_SEVEN_TYPE)
    assert c == Chord(Note(name='C'), Note(name='F'), Note(name='G'), Note(name='B'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.SUS2_TYPE)
    assert c == Chord(Note(name='C'), Note(name='D'), Note(name='G'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.SUS2_SEVEN_TYPE)
    assert c == Chord(Note(name='C'), Note(name='D'), Note(name='G'), Note(name='Bb'))

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.SUS2_MAJOR_SEVEN_TYPE)
    assert c == Chord(Note(name='C'), Note(name='D'), Note(name='G'), Note(name='B'))


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


def test_add_note_order():
    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))
    c.add_note(note=Note(name='Bb'))
    assert len(c.notes) == 4
    assert c.notes[0] == Note(name='C')
    assert c.notes[1] == Note(name='E')
    assert c.notes[2] == Note(name='G')
    assert c.notes[3] == Note(name='Bb')
    
    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))
    c.add_note(note=Note(name='C', octave=3))
    assert len(c.notes) == 4
    assert c.notes[0] == Note(name='C', octave=3)
    assert c.notes[1] == Note(name='C')
    assert c.notes[2] == Note(name='E')
    assert c.notes[3] == Note(name='G')

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))
    c.add_note(note=Note(name='C', octave=3))
    c.add_note(note=Note(name='G', octave=3))
    assert len(c.notes) == 5
    assert c.notes[0] == Note(name='C', octave=3)
    assert c.notes[1] == Note(name='G', octave=3)
    assert c.notes[2] == Note(name='C')
    assert c.notes[3] == Note(name='E')
    assert c.notes[4] == Note(name='G')


def test_add_note_strict():
    with pytest.raises(ChordException) as exc:
        Chord(Note(name='C'), Note(name='E'), Note(name='G')).add_note(note='invalid')
    
    assert 'Invalid note given.' == str(exc.value)

    with pytest.raises(ChordException) as exc:
        Chord(strict=False).add_note(note='invalid')

    assert 'Invalid note given.' == str(exc.value)

def test_add_note_strict_false():
    try:
        Chord(Note(name='C'), Note(name='E'), Note(name='G')).add_note(note='invalid', strict=False)
        Chord(strict=False).add_note(note='invalid', strict=False)
    except ChordException:
        pytest.fail('Unexpected ChordException')


def test_remove_note():
    c = Chord.create_from_root(root=Note(name='C'))
    c.remove_note(note=Note(name='E'))
    assert len(c.notes) == 2 
    assert c.notes[0] == Note(name='C')
    assert c.notes[1] == Note(name='G')

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MINOR_TYPE)
    c.remove_note(note=Note(name='Eb'))
    assert len(c.notes) == 2 
    assert c.notes[0] == Note(name='C')
    assert c.notes[1] == Note(name='G')


def test_remove_note_strict():
    c = Chord(Note(name='C'), Note(name='D'))
    with pytest.raises(ChordException) as exc:
        c.remove_note(note=Note(name='D'))
    
    assert len(c.notes) == 2
    assert c.notes[0] == Note(name='C')
    assert c.notes[1] == Note(name='D')
    assert 'Invalid Chord.' == str(exc.value)

    c = Chord(Note(name='C'), Note(name='E'))
    with pytest.raises(ChordException) as exc:
        c.remove_note(note=Note(name='C'))
    
    assert len(c.notes) == 2
    assert c.notes[0] == Note(name='C')
    assert c.notes[1] == Note(name='E')
    assert 'Invalid Chord.' == str(exc.value)

    with pytest.raises(AttributeError) as exc:
        Chord(Note(name='C'), Note(name='E'), Note(name='G')).remove_note(note='invalid')
    
    assert "'str' object has no attribute 'freq'" == str(exc.value)

    with pytest.raises(ChordException) as exc:
        Chord(strict=False).remove_note(note='invalid')

    assert 'Invalid Chord.' == str(exc.value)


def test_remove_note_strict_false():
    c = Chord(Note(name='C'), Note(name='D'))
    c.remove_note(note=Note(name='D'), strict=False)
    assert len(c.notes) == 1
    assert c.notes[0] == Note(name='C')

    c = Chord(Note(name='C'), Note(name='E'))
    c.remove_note(note=Note(name='C'), strict=False)
    assert len(c.notes) == 1
    assert c.notes[0] == Note(name='E')

    try:
        Chord(Note(name='C'), Note(name='E'), Note(name='G')).remove_note(note=Note(name='A'), strict=False)
        Chord(Note(name='C'), Note(name='E'), Note(name='G')).remove_note(octave=3, strict=False)
        Chord(Note(name='C'), Note(name='E'), Note(name='G')).remove_note(octave=4, strict=False)
        Chord(Note(name='C'), Note(name='E'), Note(name='G')).remove_note(freq=12, strict=False)
    except ChordException:
        pytest.fail('Unexpected ChordException')

    with pytest.raises(AttributeError) as exc:
        Chord(Note(name='C'), Note(name='E'), Note(name='G')).remove_note(note='invalid', strict=False)
    
    assert "'str' object has no attribute 'freq'" == str(exc.value)


def test_str():
    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))
    assert 'C4,E4,G4' == str(c)

    c.add_note(note=Note(name='C', octave=5))
    assert 'C4,E4,G4,C5' == str(c)


def test_repr():
    c = eval(repr(Chord(Note(name='C'), Note(name='E'), Note(name='G'))))
    assert c == Chord(Note(name='C'), Note(name='E'), Note(name='G'))

    c = eval(repr(Chord(Note(name='A', octave=3), Note(name='C'), Note(name='E'))))
    assert c == Chord(Note(name='A', octave=3), Note(name='C'), Note(name='E'))

    c = eval(repr(Chord(Note(name='C'), Note(name='G'), Note(name='C'), Note(name='C', octave=5))))
    assert c == Chord(Note(name='C'), Note(name='G'), Note(name='C'), Note(name='C', octave=5))

    c = eval(repr(Chord(Note(name='C'), Note(name='E'), strict=True)))
    assert c.strict is True

    c = eval(repr(Chord(Note(name='C'), Note(name='E'), strict=False)))
    assert c.strict is False