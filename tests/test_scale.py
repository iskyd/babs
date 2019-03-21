import pytest

from babs import Note, Scale, NoteList

from babs.exceptions import ScaleException


def test_create():
    s = Scale(Note(name='C'), Note(name='D'), Note(name='E'))
    assert s.notes[0] == Note(name='C') 
    assert s.notes[1] == Note(name='D')
    assert s.notes[2] == Note(name='E')
    assert len(s.notes) == 3

    s = Scale(Note(name='C'), Note(name='Bb', octave=3), Note(name='D'), Note(name='E'))
    assert s.notes[0] == Note(name='Bb', octave=3) 
    assert s.notes[1] == Note(name='C')
    assert s.notes[2] == Note(name='D')
    assert s.notes[3] == Note(name='E')
    assert len(s.notes) == 4

    s = Scale(Note(name='C'), Note(name='C'), Note(name='D'), Note(name='E'))
    assert s.notes[0] == Note(name='C')
    assert s.notes[1] == Note(name='D')
    assert s.notes[2] == Note(name='E')
    assert len(s.notes) == 3

    s = Scale(Note(name='C'), Note(name='C', octave=5), Note(name='D'), Note(name='E'))
    assert s.notes[0] == Note(name='C')
    assert s.notes[1] == Note(name='D')
    assert s.notes[2] == Note(name='E')
    assert s.notes[3] == Note(name='C', octave=5)
    assert len(s.notes) == 4

    s = Scale(Note(name='C', octave=5), Note(name='D', octave=3), Note(name='D'))
    assert s.notes[0] == Note(name='D', octave=3) 
    assert s.notes[1] == Note(name='D')
    assert s.notes[2] == Note(name='C', octave=5)
    assert len(s.notes) == 3

    s = Scale(Note(name='C'), Note(name='Bb', octave=3), Note(name='D'), order=Scale.ASCENDING_SCALE_TYPE)
    assert s.notes[0] == Note(name='Bb', octave=3) 
    assert s.notes[1] == Note(name='C')
    assert s.notes[2] == Note(name='D')
    assert len(s.notes) == 3

    s = Scale(Note(name='C', octave=5), Note(name='D', octave=3), Note(name='D'), Note(name='G'), order=Scale.ASCENDING_SCALE_TYPE)
    assert s.notes[0] == Note(name='D', octave=3) 
    assert s.notes[1] == Note(name='D')
    assert s.notes[2] == Note(name='G')
    assert s.notes[3] == Note(name='C', octave=5)
    assert len(s.notes) == 4

    s = Scale(Note(name='C'), Note(name='Bb', octave=3), Note(name='D'), Note(name='E'), order=Scale.DESCENDING_SCALE_TYPE)
    assert s.notes[0] == Note(name='E')
    assert s.notes[1] == Note(name='D') 
    assert s.notes[2] == Note(name='C')
    assert s.notes[3] == Note(name='Bb', octave=3)
    assert len(s.notes) == 4

    s = Scale(Note(name='C', octave=5), Note(name='D', octave=3), Note(name='D'), order=Scale.DESCENDING_SCALE_TYPE)
    assert s.notes[0] == Note(name='C', octave=5) 
    assert s.notes[1] == Note(name='D')
    assert s.notes[2] == Note(name='D', octave=3)
    assert len(s.notes) == 3    

    with pytest.raises(ScaleException) as exc:
        Scale()

    assert 'Invalid Scale.' == str(exc.value)

    with pytest.raises(ScaleException) as exc:
        Scale('invalid')

    assert 'Invalid Scale.' == str(exc.value)

    with pytest.raises(ScaleException) as exc:
        Scale('invalid', 'invalid')

    assert 'Invalid Scale.' == str(exc.value)

    try:
        Scale(Note(name='C'), 'invalid', strict=False)
        Scale('invalid', strict=False)
        Scale(strict=False)
    except ScaleException:
        pytest.fail("Unexpected NoteListException")


def test_create_from_root():
    s = Scale.create_from_root(root=Note(name='C'))
    assert s.notes[0] == Note(name='C')
    assert s.notes[1] == Note(name='D')
    assert s.notes[2] == Note(name='E')
    assert s.notes[3] == Note(name='F')
    assert s.notes[4] == Note(name='G')
    assert s.notes[5] == Note(name='A')
    assert s.notes[6] == Note(name='B')

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT, order=Scale.ASCENDING_SCALE_TYPE)
    assert s.notes[0] == Note(name='C')
    assert s.notes[1] == Note(name='D')
    assert s.notes[2] == Note(name='Eb')
    assert s.notes[3] == Note(name='F')
    assert s.notes[4] == Note(name='G')
    assert s.notes[5] == Note(name='Ab')
    assert s.notes[6] == Note(name='Bb')

    s = Scale.create_from_root(root=Note(name='C'), order=Scale.DESCENDING_SCALE_TYPE)
    assert s.notes[0] == Note(name='B')
    assert s.notes[1] == Note(name='A')
    assert s.notes[2] == Note(name='G')
    assert s.notes[3] == Note(name='F')
    assert s.notes[4] == Note(name='E')
    assert s.notes[5] == Note(name='D')
    assert s.notes[6] == Note(name='C')

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT, order=Scale.DESCENDING_SCALE_TYPE)
    assert s.notes[0] == Note(name='Bb')
    assert s.notes[1] == Note(name='Ab')
    assert s.notes[2] == Note(name='G')
    assert s.notes[3] == Note(name='F')
    assert s.notes[4] == Note(name='Eb')
    assert s.notes[5] == Note(name='D')
    assert s.notes[6] == Note(name='C')

    assert Scale.create_from_root(root=Note(name='C')).strict is True
    assert Scale.create_from_root(root=Note(name='C'), strict=True).strict is True
    assert Scale.create_from_root(root=Note(name='C'), strict=False).strict is False


def test_create_from_root_with_scale_type():
    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.MAJOR_TYPE)
    assert s == Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F'), Note(name='G'), Note(name='A'), Note(name='B'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.MINOR_TYPE)
    assert s == Scale(Note(name='C'), Note(name='D'), Note(name='Eb'), Note(name='F'), Note(name='G'), Note(name='Ab'), Note(name='Bb'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.IONIAN_TYPE)
    assert s == Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F'), Note(name='G'), Note(name='A'), Note(name='B'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.DORIAN_TYPE)
    assert s == Scale(Note(name='C'), Note(name='D'), Note(name='Eb'), Note(name='F'), Note(name='G'), Note(name='A'), Note(name='Bb'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.PHRIGIAN_TYPE)
    assert s == Scale(Note(name='C'), Note(name='Db'), Note(name='Eb'), Note(name='F'), Note(name='G'), Note(name='Ab'), Note(name='Bb'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.LIDYAN_TYPE)
    assert s == Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F#'), Note(name='G'), Note(name='A'), Note(name='B'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.DOMINANT_TYPE)
    assert s == Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F'), Note(name='G'), Note(name='A'), Note(name='Bb'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.AEOLIAN_TYPE)
    assert s == Scale(Note(name='C'), Note(name='D'), Note(name='Eb'), Note(name='F'), Note(name='G'), Note(name='Ab'), Note(name='Bb'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.LOCRIAN_TYPE)
    assert s == Scale(Note(name='C'), Note(name='Db'), Note(name='Eb'), Note(name='F'), Note(name='Gb'), Note(name='Ab'), Note(name='Bb'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.PENTATONIC_TYPE)
    assert s == Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='G'), Note(name='A'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.PENTATONIC_MINOR_TYPE)
    assert s == Scale(Note(name='C'), Note(name='Eb'), Note(name='F'), Note(name='G'), Note(name='Bb'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.BLUES_TYPE)
    assert s == Scale(Note(name='C'), Note(name='D'), Note(name='Eb'), Note(name='E'), Note(name='G'), Note(name='A'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.BLUES_MINOR_TYPE)
    assert s == Scale(Note(name='C'), Note(name='Eb'), Note(name='F'), Note(name='Gb'), Note(name='G'), Note(name='Bb'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.MELODIC_MINOR_TYPE)
    assert s == Scale(Note(name='C'), Note(name='D'), Note(name='Eb'), Note(name='F'), Note(name='G'), Note(name='A'), Note(name='B'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.HARMONIC_MINOR_TYPE)
    assert s == Scale(Note(name='C'), Note(name='D'), Note(name='Eb'), Note(name='F'), Note(name='G'), Note(name='Ab'), Note(name='B'))

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.HARMONIC_MAJOR_TYPE)
    assert s == Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F'), Note(name='G'), Note(name='Ab'), Note(name='B'))


def test_create_from_root_with_from_root_octave():
    s = Scale.create_from_root(root=Note(name='C', octave=3), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT, octave=NoteList.OCTAVE_TYPE_FROM_ROOT)
    assert s.notes[0] == Note(name='C', octave=3)
    assert s.notes[1] == Note(name='D', octave=3)
    assert s.notes[2] == Note(name='Eb', octave=3)
    assert s.notes[3] == Note(name='F', octave=3)
    assert s.notes[4] == Note(name='G', octave=3)
    assert s.notes[5] == Note(name='Ab', octave=3)
    assert s.notes[6] == Note(name='Bb', octave=3)

    s = Scale.create_from_root(root=Note(name='F', octave=3), scale_type=Scale.MAJOR_TYPE, alt=Note.FLAT, octave=NoteList.OCTAVE_TYPE_FROM_ROOT, order=Scale.ASCENDING_SCALE_TYPE)
    assert s.notes[0] == Note(name='F', octave=3)
    assert s.notes[1] == Note(name='G', octave=3)
    assert s.notes[2] == Note(name='A', octave=3)
    assert s.notes[3] == Note(name='Bb', octave=3)
    assert s.notes[4] == Note(name='C', octave=4)
    assert s.notes[5] == Note(name='D', octave=4)
    assert s.notes[6] == Note(name='E', octave=4)

    s = Scale.create_from_root(root=Note(name='C', octave=3), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT, octave=NoteList.OCTAVE_TYPE_FROM_ROOT, order=Scale.DESCENDING_SCALE_TYPE)
    assert s.notes[0] == Note(name='Bb', octave=3)
    assert s.notes[1] == Note(name='Ab', octave=3)
    assert s.notes[2] == Note(name='G', octave=3)
    assert s.notes[3] == Note(name='F', octave=3)
    assert s.notes[4] == Note(name='Eb', octave=3)
    assert s.notes[5] == Note(name='D', octave=3)
    assert s.notes[6] == Note(name='C', octave=3)

    s = Scale.create_from_root(root=Note(name='F', octave=3), scale_type=Scale.MAJOR_TYPE, alt=Note.FLAT, octave=NoteList.OCTAVE_TYPE_FROM_ROOT, order=Scale.DESCENDING_SCALE_TYPE)
    assert s.notes[0] == Note(name='E', octave=4)
    assert s.notes[1] == Note(name='D', octave=4)
    assert s.notes[2] == Note(name='C', octave=4)
    assert s.notes[3] == Note(name='Bb', octave=3)
    assert s.notes[4] == Note(name='A', octave=3)
    assert s.notes[5] == Note(name='G', octave=3)
    assert s.notes[6] == Note(name='F', octave=3)


def test_create_from_root_with_callable_octave():
    s = Scale.create_from_root(root=Note(name='C', octave=3), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT, octave=lambda root_octave, i, distance: root_octave + 1)
    assert s.notes[0] == Note(name='C', octave=3)
    assert s.notes[1] == Note(name='D', octave=4)
    assert s.notes[2] == Note(name='Eb', octave=4)
    assert s.notes[3] == Note(name='F', octave=4)
    assert s.notes[4] == Note(name='G', octave=4)
    assert s.notes[5] == Note(name='Ab', octave=4)
    assert s.notes[6] == Note(name='Bb', octave=4)

    s = Scale.create_from_root(root=Note(name='C', octave=3), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT, order=Scale.DESCENDING_SCALE_TYPE, octave=lambda root_octave, i, distance: root_octave + 1)
    assert s.notes[0] == Note(name='Bb', octave=4)
    assert s.notes[1] == Note(name='Ab', octave=4)
    assert s.notes[2] == Note(name='G', octave=4)
    assert s.notes[3] == Note(name='F', octave=4)
    assert s.notes[4] == Note(name='Eb', octave=4)
    assert s.notes[5] == Note(name='D', octave=4)
    assert s.notes[6] == Note(name='C', octave=3)


def test_create_from_root_with_int_octave():
    s = Scale.create_from_root(root=Note(name='C', octave=2), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT, octave=2)
    assert s.notes[0] == Note(name='C', octave=2)
    assert s.notes[1] == Note(name='D', octave=2)
    assert s.notes[2] == Note(name='Eb', octave=2)
    assert s.notes[3] == Note(name='F', octave=2)
    assert s.notes[4] == Note(name='G', octave=2)
    assert s.notes[5] == Note(name='Ab', octave=2)
    assert s.notes[6] == Note(name='Bb', octave=2) in s.notes

    s = Scale.create_from_root(root=Note(name='C', octave=2), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT, octave=2, order=Scale.DESCENDING_SCALE_TYPE)
    assert s.notes[0] == Note(name='Bb', octave=2)
    assert s.notes[1] == Note(name='Ab', octave=2)
    assert s.notes[2] == Note(name='G', octave=2)
    assert s.notes[3] == Note(name='F', octave=2)
    assert s.notes[4] == Note(name='Eb', octave=2)
    assert s.notes[5] == Note(name='D', octave=2)
    assert s.notes[6] == Note(name='C', octave=2)


def test_create_from_root_with_none_octave():
    s = Scale.create_from_root(root=Note(name='C', octave=4), scale_type=Scale.MAJOR_TYPE, alt=Note.FLAT, octave=None)
    assert s.notes[0] == Note(name='C', octave=4)
    assert s.notes[1] == Note(name='D', octave=4)
    assert s.notes[2] == Note(name='E', octave=4)
    assert s.notes[3] == Note(name='F', octave=4)
    assert s.notes[4] == Note(name='G', octave=4)
    assert s.notes[5] == Note(name='A', octave=4)
    assert s.notes[6] == Note(name='B', octave=4)

    s = Scale.create_from_root(root=Note(name='C'), order=Scale.DESCENDING_SCALE_TYPE)
    assert s.notes[0] == Note(name='B')
    assert s.notes[1] == Note(name='A')
    assert s.notes[2] == Note(name='G')
    assert s.notes[3] == Note(name='F')
    assert s.notes[4] == Note(name='E')
    assert s.notes[5] == Note(name='D')
    assert s.notes[6] == Note(name='C')


def test_add_note():
    s = Scale(Note(name='C'), Note(name='D'))
    s.add_note(Note(name='E'))

    assert len(s.notes) == 3
    assert s.notes[2] == Note(name='E')

    s.add_note(Note(name='Bb', octave=3))
    assert s.notes[0] == Note(name='Bb', octave=3)
    assert s.notes[1] == Note(name='C')
    assert s.notes[2] == Note(name='D')
    assert s.notes[3] == Note(name='E')

    s = Scale.create_from_root(root=Note(name='C'))

    s.add_note(Note(name='C', octave=5))
    assert len(s.notes) == 8
    assert s.notes[7] == Note(name='C', octave=5)

    with pytest.raises(ScaleException) as exc:
        s.add_note(note=Note(name='C'))
    
    assert len(s.notes) == 8
    assert 'Note C4 is alredy in Scale.' == str(exc.value)

    with pytest.raises(ScaleException) as exc:
        s.add_note(note=Note(name='E'))
    
    assert len(s.notes) == 8
    assert 'Note E4 is alredy in Scale.' == str(exc.value)

    s.add_note(note=Note(name='E'), strict=False)
    assert len(s.notes) == 8

    s.add_note(note=Note(name='C'), strict=False)
    assert len(s.notes) == 8


def test_remove_note():
    s = Scale.create_from_root(root=Note(name='C'))
    s.remove_note(note=Note(name='B'))
    assert len(s.notes) == 6
    assert s.notes[0] == Note(name='C')
    assert s.notes[1] == Note(name='D')
    assert s.notes[2] == Note(name='E')
    assert s.notes[3] == Note(name='F')
    assert s.notes[4] == Note(name='G')
    assert s.notes[5] == Note(name='A')

    s = Scale.create_from_root(root=Note(name='C'))
    s.remove_note(note=Note(name='A'))
    assert len(s.notes) == 6
    assert s.notes[0] == Note(name='C')
    assert s.notes[1] == Note(name='D')
    assert s.notes[2] == Note(name='E')
    assert s.notes[3] == Note(name='F')
    assert s.notes[4] == Note(name='G')
    assert s.notes[5] == Note(name='B')


def test_remove_note_strict():
    s = Scale.create_from_root(root=Note(name='C'))
    with pytest.raises(ScaleException) as exc:
        s.remove_note(octave=4)

    assert 'Invalid Scale.' == str(exc.value)
    assert len(s.notes) == 7
    assert s.notes[0] == Note(name='C')
    assert s.notes[1] == Note(name='D')
    assert s.notes[2] == Note(name='E')
    assert s.notes[3] == Note(name='F')
    assert s.notes[4] == Note(name='G')
    assert s.notes[5] == Note(name='A')
    assert s.notes[6] == Note(name='B')

    s = Scale(Note(name='C'))
    with pytest.raises(ScaleException) as exc:
        s.remove_note(name='C')

    assert 'Invalid Scale.' == str(exc.value)
    assert len(s.notes) == 1
    assert s.notes[0] == Note(name='C')

    with pytest.raises(AttributeError) as exc:
        Scale(Note(name='C'), Note(name='E'), Note(name='G')).remove_note(note='invalid')
    
    assert "'str' object has no attribute 'freq'" == str(exc.value)

    with pytest.raises(ScaleException) as exc:
        Scale(strict=False).remove_note(note='invalid')

    assert 'Invalid Scale.' == str(exc.value)


def test_remove_note_strict_false():
    s = Scale(Note(name='C'))
    s.remove_note(note=Note(name='C'), strict=False)
    assert len(s.notes) == 0

    c = Scale(Note(name='E'))
    c.remove_note(note=Note(name='E'), strict=False)
    assert len(c.notes) == 0

    try:
        Scale(Note(name='C'), Note(name='D'), Note(name='E')).remove_note(note=Note(name='A'), strict=False)
        Scale(Note(name='C'), Note(name='D'), Note(name='E')).remove_note(octave=3, strict=False)
        Scale(Note(name='C'), Note(name='D'), Note(name='E')).remove_note(octave=4, strict=False)
        Scale(Note(name='C'), Note(name='D'), Note(name='E')).remove_note(freq=12, strict=False)
    except ScaleException:
        pytest.fail('Unexpected ScaleException')

    with pytest.raises(AttributeError) as exc:
        Scale(Note(name='C'), Note(name='E'), Note(name='G')).remove_note(note='invalid', strict=False)
    
    assert "'str' object has no attribute 'freq'" == str(exc.value)


def test_str():
    s = Scale.create_from_root(root=Note(name='C'))
    assert 'C4,D4,E4,F4,G4,A4,B4' == str(s)

    s = Scale.create_from_root(root=Note(name='C'), order=Scale.DESCENDING_SCALE_TYPE)
    assert 'B4,A4,G4,F4,E4,D4,C4' == str(s)


def test_repr():
    s = eval(repr(Scale.create_from_root(root=Note(name='C'))))
    assert s == Scale.create_from_root(root=Note(name='C'))

    s = eval(repr(Scale.create_from_root(root=Note(name='F'))))
    assert s == Scale.create_from_root(root=Note(name='F'))

    s = eval(repr(Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F#'), Note(name='G#'), Note(name='A#'))))
    assert s == Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F#'), Note(name='G#'), Note(name='A#'))

    s = eval(repr(Scale.create_from_root(root=Note(name='C'), strict=True)))
    assert s.strict is True

    s = eval(repr(Scale.create_from_root(root=Note(name='C'), strict=False)))
    assert s.strict is False