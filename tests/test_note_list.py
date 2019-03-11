import pytest

from babs import NoteList, Note
from babs.exceptions import NoteListException

class Mock(NoteList):
    pass


def test_create():
    m = Mock(Note(name='C'), Note(name='D'), Note(name='E'))
    assert Note(name='C') in m.notes
    assert Note(name='D') in m.notes
    assert Note(name='E') in m.notes
    assert len(m.notes) == 3

    m = Mock(Note(name='C'), Note(name='C'), Note(name='D'), Note(name='C'))
    assert len(m.notes) == 4
    assert Note(name='C') in m.notes
    assert Note(name='D') in m.notes

    with pytest.raises(NoteListException) as exc:
        Mock('invalid')
    
    assert 'Invalid notes given.' == str(exc.value)

    with pytest.raises(NoteListException) as exc:
        Mock(Note(name='C'), 'invalid')
    
    assert 'Invalid notes given.' == str(exc.value)

    with pytest.raises(NoteListException) as exc:
        Mock()
    
    assert 'Invalid notes given.' == str(exc.value)

    try:
        Mock(Note(name='C'), 'invalid', strict=False)
        Mock('invalid', strict=False)
        Mock(strict=False)
    except NoteListException:
        pytest.fail("Unexpected NoteListException")


def test_order_notes():
    m = Mock(Note(name='C'), Note(name='D'))
    assert m.notes[0] == Note(name='C')
    assert m.notes[1] == Note(name='D')

    m = Mock(Note(name='E'), Note(name='D', octave=3), strict=True)
    assert m.notes[0] == Note(name='E')
    assert m.notes[1] == Note(name='D', octave=3)


def test_eq():
    assert \
        Mock(Note(name='C'), Note(name='D'), Note(name='C')) == \
        Mock(Note(name='C'), Note(name='D'), Note(name='C'))
    
    assert \
        Mock(Note(name='C'), Note(name='D'), Note(name='E')) == \
        Mock(Note(name='C'), Note(name='D'), Note(name='E'))
    
    assert not \
        Mock(Note(name='C'), Note(name='D'), Note(name='C')) == \
        Mock(Note(name='C'), Note(name='C'), Note(name='D'))

    assert not \
        Mock(Note(name='C'), Note(name='D'), Note(name='C')) == \
        Mock(Note(name='C', octave=5), Note(name='D'), Note(name='C'))


def test_neq():
    assert \
        Mock(Note(name='C'), Note(name='D'), Note(name='D')) != \
        Mock(Note(name='C'), Note(name='D'), Note(name='C'))
    
    assert \
        Mock(Note(name='C'), Note(name='E'), Note(name='G')) != \
        Mock(Note(name='C'), Note(name='D'), Note(name='E'))

    assert \
        Mock(Note(name='C'), Note(name='E'), Note(name='G')) != \
        Mock(Note(name='C', octave=5), Note(name='E'), Note(name='G'))

    assert not \
        Mock(Note(name='C'), Note(name='D'), Note(name='C')) != \
        Mock(Note(name='C'), Note(name='D'), Note(name='C'))


def test_str():
    m = Mock(Note(name='C'), Note(name='E'), Note(name='G'))
    assert 'C4' in str(m).split(',')
    assert 'E4' in str(m).split(',')
    assert 'G4' in str(m).split(',')

    m.add_note(note=Note(name='C', octave=5))
    assert 'C4' in str(m).split(',')
    assert 'E4' in str(m).split(',')
    assert 'G4' in str(m).split(',')
    assert 'C5' in str(m).split(',')


def test_repr():
    m = eval(repr(Mock(Note(name='C'), Note(name='D'), Note(name='E'))))
    assert m == Mock(Note(name='C'), Note(name='D'), Note(name='E'))
    assert m.notes[0] == Note(name='C')
    assert m.notes[1] == Note(name='D')
    assert m.notes[2] == Note(name='E')

    m = eval(repr(Mock(Note(name='A'), Note(name='Bb'), Note(name='C', octave=3))))
    assert m == Mock(Note(name='A'), Note(name='Bb'), Note(name='C', octave=3))
    assert m.notes[0] == Note(name='A')
    assert m.notes[1] == Note(name='Bb')
    assert m.notes[2] == Note(name='C', octave=3)

    m = eval(repr(Mock(Note(name='C'), Note(name='G'), Note(name='C'), Note(name='C', octave=5))))
    assert m == Mock(Note(name='C'), Note(name='G'), Note(name='C'), Note(name='C', octave=5))
    assert m.notes[0] == Note(name='C')
    assert m.notes[1] == Note(name='G')
    assert m.notes[2] == Note(name='C')
    assert m.notes[3] == Note(name='C', octave=5)

    m = eval(repr(Mock(Note(name='C'), Note(name='D'), strict=True)))
    assert m.strict is True

    m = eval(repr(Mock(Note(name='C'), Note(name='D'), strict=False)))
    assert m.strict is False





def test_is_valid():
    assert Mock(strict=False).is_valid() is False
    assert Mock(Note(name='C'), strict=False).is_valid() is True
    assert Mock('a', 'b', strict=False).is_valid() is False
    assert Mock(Note(name='C'), Note(name='E')).is_valid() is True

    assert Mock(Note(name='C'), Note(name='E'), strict=False).is_valid() is True
    assert Mock(strict=False).is_valid() is False


def test_add_note():
    m = Mock(Note(name='C'), Note(name='D'), Note(name='E'))
    m.add_note(note=Note(name='G'))
    assert len(m.notes) == 4
    assert Note(name='G') in m.notes

    m.add_note(note=Note(name='C'))
    assert len(m.notes) == 5

    m.add_note(note=Note(name='A', octave=5))
    assert len(m.notes) == 6
    assert Note(name='A', octave=5) in m.notes


def test_add_invalid_note():
    m = Mock(Note(name='C'), Note(name='D'), Note(name='E'))
    with pytest.raises(NoteListException) as exc:
        m.add_note(note=1)
    
    assert 'Invalid note given.' == str(exc.value)

    with pytest.raises(NoteListException) as exc:
        m.add_note(note='invalid')
    
    assert 'Invalid note given.' == str(exc.value)

    m.add_note(note='invalid', strict=False)

    assert len(m.notes) == 4

    with pytest.raises(AttributeError) as exc:
        assert "'str' object has no attribute 'freq'" in m.notes


def test_remove_note_by_note():
    m = Mock(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))
    m.remove_note(note=Note(name='C', octave=5))

    assert len(m.notes) == 3
    assert Note(name='C') in m.notes
    assert Note(name='G') in m.notes
    assert Note(name='E') in m.notes
    assert Note(name='C', octave=5) not in m.notes

    m.remove_note(note=Note(name='E'))
    assert len(m.notes) == 2
    assert Note(name='G') in m.notes
    assert Note(name='C') in m.notes
    assert Note(name='E') not in m.notes

    with pytest.raises(NoteListException) as exc:
        m.remove_note(note=Note(name='D'))

    assert len(m.notes) == 2
    assert Note(name='G') in m.notes
    assert Note(name='C') in m.notes
    assert 'Invalid request. Note not found in list.' == str(exc.value)

    with pytest.raises(AttributeError) as exc:
        m.remove_note(note='a')

    assert "'str' object has no attribute 'freq'" == str(exc.value)

    with pytest.raises(NoteListException) as exc:
        Mock(Note(name='C')).remove_note(note=Note(name='C'))

    assert 'Invalid notes.' == str(exc.value)


def remove_note_by_note_not_strict():
    m = Mock('a', 'b')
    m.remove_note(note='a', strict=False)

    assert len(m.notes) == 1
    assert 'b' in m.notes
    assert 'a' not in m.notes

    m = Mock(Note(name='C'), Note(name='E'))
    m.remove_note(note=Note(name='C'), strict=False)

    assert len(m.notes) == 1
    assert Note(name='E') in m.notes

    m.remove_note(name='G', strict=False)
    assert len(m.notes) == 1
    assert Note(name='E') in m.notes

    try:
        Mock(Note(name='C')).remove_note(note=Note(name='C'), strict=False)
    except:
        pytest.fail("Unexpected NoteListException")


def test_remove_note_by_freq():
    m = Mock(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))
    m.remove_note(freq=523.25)  # C5

    assert len(m.notes) == 3
    assert Note(name='C') in m.notes
    assert Note(name='E') in m.notes
    assert Note(name='G') in m.notes
    assert Note(name='C', octave=5) not in m.notes

    m.remove_note(freq=329.63)

    assert len(m.notes) == 2
    assert Note(name='C') in m.notes
    assert Note(name='G') in m.notes
    assert Note(name='E') not in m.notes
    assert Note(name='C', octave=5) not in m.notes

    with pytest.raises(NoteListException) as exc:
        m.remove_note(freq=250)

    assert 'Invalid request. Note not found in list.' == str(exc.value)

    m = Mock('a', 'b', strict=False)
    with pytest.raises(AttributeError) as exc:
        m.remove_note(freq=261.63)

    assert len(m.notes) == 2
    assert "'str' object has no attribute 'freq'" == str(exc.value)

    with pytest.raises(NoteListException) as exc:
        Mock(Note(name='A')).remove_note(freq=440)

    assert 'Invalid notes.' == str(exc.value)


def test_remove_note_by_freq_not_strict():
    m = Mock(Note(name='C'), Note(name='E'))
    m.remove_note(freq=261.63, strict=False)

    assert len(m.notes) == 1
    assert Note(name='E') in m.notes

    m.remove_note(freq=440, strict=False)
    assert len(m.notes) == 1
    assert Note(name='E') in m.notes

    try:
        Mock(Note(freq=440)).remove_note(freq=440, strict=False)
    except:
        pytest.fail("Unexpected NoteListException")


def test_remove_note_by_name():
    m = Mock(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='B'), Note(name='C', octave=5))
    m.remove_note(name='C')

    assert len(m.notes) == 3
    assert Note(name='E') in m.notes
    assert Note(name='G') in m.notes
    assert Note(name='B') in m.notes
    assert Note(name='C') not in m.notes

    m.remove_note(name='B')
    assert len(m.notes) == 2
    assert Note(name='E') in m.notes
    assert Note(name='G') in m.notes
    assert Note(name='B') not in m.notes

    with pytest.raises(NoteListException) as exc:
        m.remove_note(name='F')

    assert len(m.notes) == 2
    assert Note(name='E') in m.notes
    assert Note(name='G') in m.notes
    assert 'Invalid request. Note not found in list.' == str(exc.value)

    with pytest.raises(NoteListException) as exc:
        Mock(Note(name='A')).remove_note(name='A')

    assert 'Invalid notes.' == str(exc.value)


def test_remove_note_by_name_not_strict():
    m = Mock(Note(name='C'), Note(name='E'))
    m.remove_note(name='C', strict=False)

    assert len(m.notes) == 1
    assert Note(name='E') in m.notes

    m.remove_note(name='G', strict=False)
    assert len(m.notes) == 1
    assert Note(name='E') in m.notes

    try:
        Mock(Note(name='A')).remove_note(name='A', strict=False)
    except:
        pytest.fail("Unexpected NoteListException")


def test_remove_note_by_octave():
    m = Mock(Note(name='B', octave=3), Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))
    m.remove_note(octave=5)

    assert len(m.notes) == 4
    assert Note(name='C') in m.notes
    assert Note(name='E') in m.notes
    assert Note(name='G') in m.notes
    assert Note(name='B', octave=3) in m.notes
    assert Note(name='C', octave=5) not in m.notes

    m.remove_note(octave=3)

    assert len(m.notes) == 3
    assert Note(name='C') in m.notes
    assert Note(name='E') in m.notes
    assert Note(name='G') in m.notes
    assert Note(name='B', octave=3) not in m.notes

    with pytest.raises(NoteListException) as exc:
        m.remove_note(octave=3)

    assert len(m.notes) == 3
    assert 'Invalid request. Note not found in list.' == str(exc.value)

    with pytest.raises(NoteListException) as exc:
        Mock(Note(name='A'), Note(name='B')).remove_note(octave=4)

    assert 'Invalid notes.' == str(exc.value)


def test_remove_note_by_octave_not_strict():
    m = Mock(Note(name='C'), Note(name='C', octave=5))
    m.remove_note(octave=4, strict=False)

    assert len(m.notes) == 1
    assert Note(name='C', octave=5) in m.notes

    m.remove_note(octave=3, strict=False)
    assert len(m.notes) == 1
    assert Note(name='C', octave=5) in m.notes

    try:
        Mock(Note(name='A'), Note(name='B')).remove_note(octave=4, strict=False)
    except:
        pytest.fail("Unexpected NoteListException")


def test_remove_note_no_args():
    with pytest.raises(NoteListException) as exc:
        Mock(Note(name='C'), Note(name='E'), Note(name='G')).remove_note()

    assert 'Invalid request. Note not found in list.' == str(exc.value)

    m = Mock(Note(name='C'), Note(name='E'), Note(name='G'))
    m.remove_note(strict=False)
    assert len(m.notes) == 3
    assert Note(name='C') in m.notes
    assert Note(name='E') in m.notes
    assert Note(name='G') in m.notes


def test_get_notes_from_root():
    notes = Mock.get_notes_from_root(root=Note(name='C'), note_list_type=[3, 5, 7, 10])
    assert Note(name='C') in notes
    assert Note(name='Eb') in notes
    assert Note(name='F') in notes
    assert Note(name='G') in notes
    assert Note(name='Bb') in notes

    notes = Mock.get_notes_from_root(root=Note(name='C'), note_list_type=[2, 4, 7, 9])
    assert Note(name='C') in notes
    assert Note(name='D') in notes
    assert Note(name='E') in notes
    assert Note(name='G') in notes
    assert Note(name='A') in notes


def test_get_notes_from_root_with_none_note_list_type():
    with pytest.raises(NoteListException) as exc:
        Mock.get_notes_from_root(root=Note(name='C'))
    
    assert 'Invalid note list type' == str(exc.value)

    with pytest.raises(NoteListException) as exc:
        Mock.get_notes_from_root(root=Note(name='C'), alt=Note.FLAT, octave=4)
    
    assert 'Invalid note list type' == str(exc.value)


def test_get_notes_from_root_with_alt():
    m = Mock(*Mock.get_notes_from_root(root=Note(name='C'), note_list_type=[3, 5, 7, 10], alt=Note.FLAT))
    assert 'Eb4' in str(m).split(',')
    assert 'Bb4' in str(m).split(',')

    m = Mock(*Mock.get_notes_from_root(root=Note(name='C'), note_list_type=[3, 5, 7, 10], alt=Note.SHARP))
    assert 'D#4' in str(m).split(',')
    assert 'A#4' in str(m).split(',')


def test_get_notes_from_root_with_from_root_octave():
    notes = Mock.get_notes_from_root(root=Note(name='C', octave=4), note_list_type=[3, 5, 7, 10], octave='from_root')

    assert Note(name='C', octave=4) in notes
    assert Note(name='Eb', octave=4) in notes
    assert Note(name='F', octave=4) in notes
    assert Note(name='G', octave=4) in notes
    assert Note(name='Bb', octave=4) in notes

    notes = Mock.get_notes_from_root(root=Note(name='F', octave=3), note_list_type=[3, 5, 7, 10], octave='from_root')

    assert Note(name='F', octave=3) in notes
    assert Note(name='Ab', octave=3) in notes
    assert Note(name='Bb', octave=3) in notes
    assert Note(name='C', octave=4) in notes
    assert Note(name='Eb', octave=4) in notes


def test_get_notes_from_root_with_int_octave():
    notes = Mock.get_notes_from_root(root=Note(name='C', octave=4), note_list_type=[3, 5, 7, 10], octave=4)

    assert Note(name='C', octave=4) in notes
    assert Note(name='Eb', octave=4) in notes
    assert Note(name='F', octave=4) in notes
    assert Note(name='G', octave=4) in notes
    assert Note(name='Bb', octave=4) in notes

    notes = Mock.get_notes_from_root(root=Note(name='C', octave=3), note_list_type=[3, 5, 7, 10], octave=4)

    assert Note(name='C', octave=3) in notes
    assert Note(name='Eb', octave=4) in notes
    assert Note(name='F', octave=4) in notes
    assert Note(name='G', octave=4) in notes
    assert Note(name='Bb', octave=4) in notes


def test_get_notes_from_root_with_callable_octave():
    notes = Mock.get_notes_from_root(root=Note(name='C', octave=3), note_list_type=[3, 7], octave=lambda root_octave, i, distance: root_octave + 1)

    assert Note(name='C', octave=3) in notes
    assert Note(name='Eb', octave=4) in notes
    assert Note(name='G', octave=4) in notes

    notes = Mock.get_notes_from_root(root=Note(name='C', octave=3), note_list_type=[3, 7], octave=lambda root_octave, i, distance: i + 1)

    assert Note(name='C', octave=3) in notes
    assert Note(name='Eb', octave=1) in notes
    assert Note(name='G', octave=2) in notes

    with pytest.raises(TypeError):
        notes = Mock.get_notes_from_root(root=Note(name='C', octave=3), note_list_type=[3, 7], octave=lambda: 'invalid')


def test_get_notes_from_root_with_invalid_octave():
    notes = Mock.get_notes_from_root(root=Note(name='C'), note_list_type=[3, 5, 7, 10], octave='invalid')

    assert Note(name='C', octave=4) in notes
    assert Note(name='Eb', octave=4) in notes
    assert Note(name='F', octave=4) in notes
    assert Note(name='G', octave=4) in notes
    assert Note(name='Bb', octave=4) in notes
