Chord
================================

.. py:class:: Chord(*notes, **kwargs)

    Return a Chord, an harmonic set of pitches consisting of two or more notes.
    Chord is an ordered list of notes from lower to higher.
    If strict is True (default) raise ChordException if chord has less then two notes or
    if Notes are not valid Note object.
    
    Chord extends NoteList so it inherits all methods from NoteList: is_valid(), add_note(note[, strict=True]), remove_note(note=None, freq=None, name=None, octave=None[, strict=True]).

   .. py:classmethod:: create_from_root(root[, chord_type=None, octave='root', alt='sharp'])
        Create and return a Chord from the root note



Create your first chord
--------------------------------

.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))

Now you have create the C chord and you can access to the notes attribute.

.. code-block:: python

    for n in c.notes:
        print(n)

    # C4
    # E4
    # G4

Chord is an ordered list of notes from lower to higher.
So the order in which you pass the notes in the constructor is not relevand, the list will always be from lower note (lower frequency)
to the higher note (higher frequency).

.. code-block:: python

    c = Chord(Note(name='E'), Note(name='G'), Note(name='C'))

    for n in c.notes:
        print(n)

    # C4
    # E4
    # G4

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=3))

    for n in c.notes:
        print(n)
    
    # C3
    # C4
    # E4
    # G4


strict
--------------------------------

As we said a Chord consists of two or more note. So what happen if we create a one Note or an empty Chord?

.. code-block:: python

    c = Chord(Note(name='C'))


ChordException (Invalid Chord.)
You can disable is_valid() control passing strict=False.
In this way you will also disable the ordering, because order() works with Note object (using the attribute freq of the note)
and will throw AttributeError if the object is not a valid Note.

.. code-block:: python

    c = Chord(Note(name='C'), strict=False)
    print(len(c.notes))  # 1


If you set strict to False you also disable Note check so this will be valid.

.. code-block:: python

    c = Chord('a', 'b', 'c')
    print(len(c.notes))  # 3


notes attribute
--------------------------------

You can only get the notes attribute but not set it!

.. code-block:: python

    c = Chord(Note(name='C'), Note(name='E'))

    c.notes = [Note(name='C'), Note(name='E'), Note(name='G'), Note(name='Bb')]

    # AttributeError: can't set attribute


add note
--------------------------------

This method use the add_note() method of NoteList abstract class but re-order the notes (if Chord is valid) after the note is added.

.. code-block:: python

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))

    c.add_note(note=Note(name='Bb'))

    print(len(c.notes))  # 4

    for n in c.notes:
        print(n)

    # C4
    # E4
    # G4
    # Bb4

    c.add_note(note=Note(name='C', octave=3))

    print(len(c.notes))  # 5

    for n in c.notes:
        print(n)

    # C3
    # C4
    # E4
    # G4
    # Bb4

You can add the same note multiple times:

.. code-block:: python

    c = Chord(Note(name='A', octave=3), Note(name='C'), Note(name='E'))
    
    c.add_note(note=Note(name='E'))

    print(len(c.notes))

    for n in c.notes:
        print(n)

    # A3
    # C4
    # E4
    # E4

By default strict is set to True, so if you add an invalid Note you will get a ChordException

.. code-block:: python

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G')).add_note(note='c')  # Add a string instead of a Note

    # ChordException: Instance of Note expected, str given.

    c = Chord(strict=False)
    c.add_note(note='c', strict=False)

    print(len(c.notes))  # 1

remove note
--------------------------------
This method use the remove_note() method of NoteList abstract class but re-order the notes (if Chord is valid) after the note is added.

.. code-block:: python

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))
    c.remove_note(note=Note(name='G'))

    print(len(c.notes))  # 2

    for n in c.notes:
        print(n)

    # C4
    # E4

By default, as before, strict is set to True, so if the Chord will be invalid after remove
you will have a ChordException.
If a ChordException is raised the notes in the chord will be restored as they were before the remove.

.. code-block:: python

    c = Chord(Note(name='C'), Note(name='E'))

    c.remove_note(note=Note(name='E'))
    # Invalid Chord.

    print(len(c.notes))  # 2

    for n in c.notes:
        print(n)

    # C4
    # E4


Removing a Note by octave or name can remove multiple notes.

.. code-block:: python

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))

    print(len(c.notes))  # 4

    c.remove_note(name='C')
    print(len(c.notes))  # 2

    for n in c.notes:
        print(n)

    # E4
    # G4

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))
    c.remove_note(octave=4, strict=False)

    print(len(c.notes))  # 1

    for n in c.notes:
        print(n)

    # C5


is valid
--------------------------------

If you need to know if the actual Chord is valid you can use is_valid method.
A chord is valid if has two or more Note and if all notes are instance of Note()


Comparison
--------------------------------

Chord support equal and not equal comparison operator. 
Check NoteList documentation for more information


Create from root Note
--------------------------------

You can easily create a Chord from root note using the create_from_root classmethod.
Suppose you want create a C major chord.

.. code-block:: python

    c = Chord.create_from_root(root=Note(name='C'))
    for n in c.notes:
        print(n)

    # C4
    # E4
    # G4

That's it, you've got a C major chord.
create_from_root use the classmethod get_notes_from_root of NoteList.
Check NoteList documentation for more information.

babs come with some of pre-defined chord_type so that the previous example could be the same as

.. code-block:: python

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MAJOR_SEVEN_TYPE)

You can use a custom list or use some of the pre-defined chord type.


List of pre-defined chord type
--------------------------------

+----------------------------+
| Chord type                 |
+============================+
| MAJOR_TYPE                 |
+----------------------------+
| MAJOR_SEVEN_TYPE           |
+----------------------------+
| MINOR_TYPE                 |
+----------------------------+
| MINOR_SEVEN_TYPE           |
+----------------------------+
| DOMINANT_TYPE              |
+----------------------------+
| MINOR_MAJOR_SEVEN_TYPE     |
+----------------------------+
| HALF_DIMINISHED_SEVEN_TYPE |
+----------------------------+
| DIMINISHED_TYPE            |
+----------------------------+
| DIMINISHED_SEVEN_TYPE      |
+----------------------------+
| AUGMENTED_TYPE             |
+----------------------------+
| AUGMENTED_SEVEN_TYPE       |
+----------------------------+
| AUGMENTED_MAJOR_SEVEN_TYPE |
+----------------------------+
| MAJOR_SIXTH_TYPE           |
+----------------------------+
| MINOR_SIXTH_TYPE           |
+----------------------------+
| SUS4_TYPE                  |
+----------------------------+
| SUS4_SEVEN_TYPE            |
+----------------------------+
| SUS4_MAJOR_SEVEN_TYPE      |
+----------------------------+
| SUS2_TYPE                  |
+----------------------------+
| SUS2_SEVEN_TYPE            |
+----------------------------+
| SUS2_MAJOR_SEVEN_TYPE      |
+----------------------------+

