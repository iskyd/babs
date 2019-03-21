Scale
================================

.. py:class:: Scale(*notes, **kwargs)

    Return a Scale, a set of musical notes ordered by fundamental frequency or pitch.
    Scale is an ordered list of unique notes.
    If strict is True (default) raise ScaleException if Notes are not valid Note object.
    
    Scale extends NoteList so it inherits all methods from NoteList: is_valid(), add_note(note[, strict=True]), remove_note(note=None, freq=None, name=None, octave=None[, strict=True]).

   .. py:classmethod:: create_from_root(root[, scale_type=None, octave='root', alt='sharp'])
        Create and return a Scale from the root note



Create your first scale
--------------------------------

.. code-block:: python

    from babs import Note, Scale

    s = Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F'), Note(name='G'), Note(name='A'), Note(name='B'))

Now you have create the C major scale and you can access to the notes attribute.

.. code-block:: python

    for n in s.notes:
        print(n)

    # C4
    # D4
    # E4
    # F4
    # G4
    # A4
    # B4


Scale is an ordered list of unique notes. Scale could be ascending (from lower to higher) or descending (from higher to lower), by default is ascending.
The order in which you pass the notes in the constructor is not relevant, 
the list will always be from lower to higher (frequency) or from higher to lower (frequency) note.

.. code-block:: python

    s = Scale(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='A'), Note(name='F'), Note(name='D'), Note(name='B'))

    for n in s.notes:
        print(n)

    # C4
    # D4
    # E4
    # F4
    # G4
    # A4
    # B4

    s = Scale(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='A'), Note(name='F'), Note(name='D'), Note(name='B'), order=Scale.DESCENDING_SCALE_TYPE)

    for n in s.notes:
        print(n)
    
    # B4
    # A4
    # G4
    # F4
    # E4
    # D4
    # C4



strict
--------------------------------

As we said a Scale is a set of unique notes. So what happen if we create an empty Scale?

.. code-block:: python

    s = Scale()


ScaleException (Invalid Scale.)
You can disable is_valid() control passing strict=False.
In this way you will also disable the ordering, because order() works with Note object (using the attribute freq of the note)
and will raise AttributeError if the object is not a valid Note.

.. code-block:: python

    s = Scale(strict=False)
    print(len(s.notes))  # 0


If you set strict to False you also disable Note check so this will not raise an exception.

.. code-block:: python

    s = Scale('a', 'b', 'c', strict=False)
    print(len(c.notes))  # 3


notes attribute
--------------------------------

You can only get the notes attribute but not set it!

.. code-block:: python

    s = Scale(Note(name='C'))

    s.notes = [Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F'), Note(name='G'), Note(name='A'), Note(name='B')]

    # AttributeError: can't set attribute


add note
--------------------------------

This method use the add_note() method of NoteList abstract class but re-order the notes (if Scale is valid) after the note is added.
It also checks if the note alredy exists in the scale and raise an exception if it alredy exists.

.. code-block:: python

    s = Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F'), Note(name='G'), Note(name='A'))

    s.add_note(note=Note(name='B'))

    print(len(s.notes))  # 7

    for n in s.notes:
        print(n)

    # C4
    # D4
    # E4
    # F4
    # G4
    # A4
    # B4

    s.add_note(note=Note(name='B'))

    # babs.exceptions.scale_exception.ScaleException: Note B4 is alredy in Scale.

By default strict is set to True, so if you add an invalid Note or a note that alredy exists in the scale you will get a ScaleException

.. code-block:: python

    s = Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F'), Note(name='G'), Note(name='A'))
    
    s.add_note(note='c')  # Add a string instead of a Note

    # ScaleException: AttributeError: 'str' object has no attribute 'freq'

remove note
--------------------------------
This method use the remove_note() method of NoteList abstract class but re-order the notes (if Scale is valid) after the note is added.

.. code-block:: python

    s = Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F'), Note(name='G'), Note(name='A'), Note(name='B'))
    s.remove_note(note=Note(name='B'))

    print(len(s.notes))  # 6

    for n in s.notes:
        print(n)

    # C4
    # D4
    # E4
    # F4
    # G4
    # A4

By default, as before, strict is set to True, so if the Scale will be invalid after remove
you will have a ScaleException.
If ScaleException is raised the notes in the scale will be restored as they were before the remove.

.. code-block:: python

    s = Scale(Note(name='C'))

    s.remove_note(note=Note(name='C'))
    # Invalid Scale.

    print(len(s.notes))  # 1

    for n in s.notes:
        print(n)

    # C4


Removing a Note by octave or name can remove multiple notes.

.. code-block:: python

    s = Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F'), Note(name='G'), Note(name='A'), Note(name='B'), Note(name='C', octave=5))
    # C4 and C5 are different note

    print(len(s.notes))  # 8

    s.remove_note(name='C')
    print(len(s.notes))  # 6

    for n in s.notes:
        print(n)

    # D4
    # E4
    # F4
    # G4
    # A4
    # B4

    s = Scale(Note(name='C'), Note(name='D'), Note(name='E'), Note(name='F'), Note(name='G'), Note(name='A'), Note(name='B'), Note(name='C', octave=5), Note(name='C', octave=6))
    s.remove_note(octave=5)

    print(len(s.notes))  # 7

    for n in s.notes:
        print(n)

    # C4
    # D4
    # E4
    # F4
    # G4
    # A4
    # B4


is valid
--------------------------------

If you need to know if the actual Scale is valid you can use is_valid method.
A scale is valid if has one or more Note and if all notes are instance of Note()


Comparison
--------------------------------

Scale support equal and not equal comparison operator. 
Check NoteList documentation for more information


Create Scale from root Note
--------------------------------

You can easily create a Scale from root note using the create_from_root classmethod.
Suppose you want create a C major scale.

.. code-block:: python

    s = Scale.create_from_root(root=Note(name='C'))
    for n in s.notes:
        print(n)

    # C4
    # D4
    # E4
    # F4
    # G4
    # A4
    # B4

    s = Scale.create_from_root(root=Note(name='C'), scale_type=Scale.MINOR_TYPE, alt=Note.FLAT)
    for n in s.notes:
        print(n)

    # C4
    # D4
    # Eb4
    # F4
    # G4
    # Ab4
    # Bb4

That's it, you've got a C major scale and then a C minor scale.
create_from_root use the classmethod get_notes_from_root of NoteList.
Check NoteList documentation for more information.

babs come with some of pre-defined scale_type so that the previous example could be the same as

.. code-block:: python

    s = Scale.create_from_root(root=Note(name='C'), chord_type=Scale.DORIAN_TYPE)

You can use a custom list or use some of the pre-defined chord type.


List of pre-defined scale type
--------------------------------

+----------------------------+
| Scale type                 |
+============================+
| MAJOR_TYPE                 |
+----------------------------+
| MINOR_TYPE                 |
+----------------------------+
| IONIAN_TYPE                |
+----------------------------+
| DORIAN_TYPE                |
+----------------------------+
| PHRIGIAN_TYPE              |
+----------------------------+
| LIDYAN_TYPE                |
+----------------------------+
| DOMINANT_TYPE              |
+----------------------------+
| AEOLIAN_TYPE               |
+----------------------------+
| LOCRIAN_TYPE               |
+----------------------------+
| PENTATONIC_TYPE            |
+----------------------------+
| PENTATONIC_MINOR_TYPE      |
+----------------------------+
| BLUES_TYPE                 |
+----------------------------+
| BLUES_MINOR_TYPE           |
+----------------------------+
| MELODIC_MINOR_TYPE         |
+----------------------------+
| HARMONIC_MINOR_TYPE        |
+----------------------------+
| HARMONIC_MAJOR_TYPE        |
+----------------------------+

