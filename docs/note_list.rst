NoteList
================================

.. py:abstractclass:: NoteList(*notes, **kwargs)

    Abstract class that define an ordered list of notes.
    If strict is True (default) raise NoteListException if notes are not valid Note object
    or if list contains less than one note.

   .. py:method:: is_valid()

        Return True if the current note list is valid, False otherwise.
        NoteList is valid if it has at least one note and all note in list are valid Note object.

   .. py:method:: add_note(note[, strict=True])

        Add a note to the current list. If strict is True raise a NoteListException if Note is not a valid note.

   .. py:method:: remove_note(note=None, freq=None, name=None, octave=None[, strict=True])

        Remove a note from the current list by Note, freq, name or octave.
        If strict is True raise NoteListException if Note is not found or
        if NoteList is not valid after remove.

   .. py:classmethod:: get_notes_from_root(root[, note_list_type=None, octave='root', alt=Note.SHARP])
        Return a list of note created from root based on note_list_type



Create your first NoteList
--------------------------------

NoteList is an abstract class, so you can't instantiate it.
We create a Mock class that extends NoteList in order to instantiate it.

.. code-block:: python

    from babs import Note, NoteList

    class Mock(NoteList):
        pass

    m = Mock(Note(name='C'), Note(name='D'), Note(name='E'))

Now you have create the C chord and you can access to the notes attribute.

.. code-block:: python

    print(len(m.notes)
    for n in m.notes:
        print(n)

    # 3
    # C4
    # D4
    # E4

strict
--------------------------------

As we said a NoteList consists of one or more note. 
So if we create an empty NoteList we'll get a NoteListException.

.. code-block:: python

    from babs import Note, NoteList

    class Mock(NoteList):
        pass

    m = Mock()

    # NoteListException "Invalid notes given."


If you need to create an "invalid" NoteList you can use strict parameter.

.. code-block:: python

    m = Mock(strict=False)
    print(len(m.notes))  # 0


If you set strict to False you can also pass an invalid Note to NoteList.

.. code-block:: python

    m = Mock('invalid', 'notes', strict=False)
    print(len(m.notes))  # 3


notes attribute
--------------------------------

You can only get the notes attribute but you can't set it!

.. code-block:: python

    m = Mock(strict=False)

    m.notes = [Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5)]

    # AttributeError: can't set attribute


add note
--------------------------------

You can use this method if you need to add a Note to the current list.


.. code-block:: python

    m = Mock(Note(name='C'), Note(name='D'), Note(name='C'))

    c.add_note(note=Note(name='E'))

    print(len(c.notes))  # 4

    for n in c.notes:
        print(n)

    # C4
    # D4
    # C4
    # E4

By default strict is set to True, so if you try to add an invalid Note you will get a NoteListException

.. code-block:: python

    m.add_note('invalid')  # Add a string instead of a Note

    # NoteListException: Instance of Note expected, str given.

    m = Mock(Note(name='C'), Note(name='D'))
    m.add_note('invalid', strict=False)

    print(len(m.notes))  # 3

remove note
--------------------------------
If you need to remove a Note you can use the remove_note() method.
You can remove a note by Note(), name, frequency or octave.

.. code-block:: python

    m = Mock(Note(name='C'), Note(name='E'), Note(name='G'))
    c.remove_note(note=Note(name='G'))

    print(len(m.notes))  # 2

    for n in m.notes:
        print(n)

    # C4
    # E4

By default, as before, strict is set to True, so if the list will be invalid after remove you will have a NoteListException.
If a NoteListException is raised the notes in the list will be restored as they were before the remove.

.. code-block:: python

    m = Mock(Note(name='C'))

    m.remove_note(note=Note(name='C'))
    # Invalid Mock.

    print(len(c.notes))  # 1


Removing a Note by octave or name can remove multiple notes.

.. code-block:: python

    m = Mock(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))

    print(len(m.notes))  # 4

    m.remove_note(name='C')
    print(len(m.notes))  # 2

    for n in m.notes:
        print(n)

    # E4
    # G4

    m = Mock(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))
    m.remove_note(octave=4)

    print(len(m.notes))  # 1

    for n in m.notes:
        print(n)

    # C5


is valid
--------------------------------

If you need to know if the actual list is valid you can use is_valid method.
A NoteList is valid if has one or more notes and if all notes are valid Note object (instance of Note)


Comparison
--------------------------------

NoteList support equal and not equal comparison operator. 
Two NoteList are the same if they have the same notes (check note comparison for more details).
The strict attribute in create doesn't affect the list comparison.

.. code-block:: python

    Mock(Note(name='A'), Note(name='C')) == Mock(Note(name='A'), Note(name='C'))  # True
    Mock(Note(name='A'), Note(name='C'), strict=True) == Mock(Note(name='A'), Note(name='C'), strict=False)  # True
    Mock(Note(name='A'), Note(name='C')) == Mock(Note(name='A'), Note(name='C'), Note(name='E'))  # False
    Mock(Note(name='A'), Note(name='C')) != Mock(Note(name='A'), Note(name='C'))  # False


get_notes_from_root
--------------------------------

You can easily get a list of notes from a root chord using the get_notes_from_root classmethod.
Suppose you want to get a basic list of note C - E - G.

.. code-block:: python

    notes = Mock.get_notes_from_root(root=Note(name='C'), note_list_type=[4, 7])
    for n in c.notes:
        print(n)

    # C4
    # E4
    # G4

That's it, you've got a C - E - G list.
So how it works? get_notes_from_root use a note_list_type, which is a list of notes distance from root note.
So the [4, 7]. 4 is the distance between root from 3d and between the root and the 5th.
The distance is based on the Note.NOTES list: NOTES = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
So let's say we want a major seven chord.

.. code-block:: python

    notes = Mock.get_notes_from_root(root=Note(name='C'), note_list_type=[4, 7, 11])
    for n in notes:
        print(n)

    # C4
    # E4
    # G4
    # B4

This works because the index the E is distant 4 elements from the root (C) in the Note.NOTES list, 
the G is distant 7 elements and the B is distant 11 elements
By default the octave of other notes will be the same as the root note. To change that behaviour
you can use the octave param.
**The root note will not be affected by the octave param.**
octave could be :

- an integer, so that every note will have that specific octave.

.. code-block:: python

    notes = Mock.get_notes_from_root(root=Note(name='C'), note_list_type=[2, 4], octave=3)

    for n in notes:
        print(n)

    # C4
    # D3
    # E3

- a string 'root' NoteList.OCTAVE_TYPE_ROOT or 'from_root' NoteList.OCTAVE_TYPE_FROM_ROOT:
    - 'root', the default behaviour, use the root.octave.
    - 'from_root' use the root.octave as the starting octave. So if you have a G-B-D, the starting octave is 4 so we have a G4, then we have a B4 and at least the D Note goes to the next octave so it is a D5.

.. code-block:: python

    notes = NoteList.get_notes_from_root(root=Note(name='G'), note_list_type=[4, 7], octave=NoteList.OCTAVE_TYPE_FROM_ROOT)

    for n in notes:
        print(n)

    # G4
    # B4
    # D5

- a callable, that must return an integer.
  In the callable you have access to root_octave, i (the idx of list distance iteration, starting from 0) and the distance between the current note and the root note.
  So suppose you want to have a list that looks like G4, B5, D6.

.. code-block:: python

    notes = NoteList.get_notes_from_root(
            root=Note(name='G'),
            note_list_type=[4, 7], octave=lambda root_octave, i, distance: root_octave + i + 1
        )

    for n in notes:
        print(n)

    # G4
    # B5
    # D6

If the octave is invalid, for example a string different from 'root' and 'from_root' or a float number, it will be set to 4.

You can also specify the alteration of the notes using the alt param (by default is 'sharp' Note.SHARP) that works in the same way as for single note.

.. code-block:: python

    notes = NoteList.get_notes_from_root(root=Note(name='G'), note_list_type=[4, 7, 11], alt=Note.SHARP)

    for n in notes:
        print(n)

    # G4
    # B4
    # D4
    # F#4

    notes = NoteList.get_notes_from_root(root=Note(name='G'), note_list_type=[4, 7, 11], alt=Note.FLAT)

    for n in notes:
        print(n)

    # G4
    # D4
    # B4
    # Gb4


