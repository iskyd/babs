Chord
================================

.. py:class:: Chord(*notes, **kwargs)

    Return a Chord, an harmonic set of pitches consisting of two or more notes
    If strict is True (default) raise ChordException if chord has less then two notes or
    if Notes are not valid Note.

   .. py:method:: is_valid()

        Return True if the current chord is valid, False otherwise

   .. py:method:: add_note(note[, strict=True])

        Add a note to the current chord. If strict is True raise a ChordException if Note is not a valid note.

   .. py:method:: remove_note(note=None, freq=None, name=None, octave=None[, strict=True])

        Remove a note from the current chord by Note, freq, name or octave.
        If strict is True raise ChordException if Note is not found or
        if Chord has less then two notes after remove

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

    # G4
    # E4
    # C4

So here come the first important thing, why the first note is a G4 and not a C4?
Because notes is an unordered collections of unique elements (note) even if it is a list.
So we can't add the same Note multiple times, let's take a try.

.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C'))

    print(len(c.notes))  # 3

    for n in c.notes:
        print(n)

    # G4
    # E4
    # C4

Remember that Note(name='C') is not equal to Note(name='C', octave=5)

.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))

    print(len(c.notes))  # 4

    for n in c.notes:
        print(n)

    # G4
    # E4
    # C5
    # C4


strict
--------------------------------

As we said a Chord consists of two or more note. So what happen if we create a one Note or an empty Chord?

.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'))


Boooom!!! ChordException (Chords must have at least two notes, 1 given.)
If you need to create an "invalid" Chord you can use strict!

.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'))
    print(len(c.notes))  # 1


If you set strict to False you also disable Note check so this will be valid.

.. code-block:: python

    from babs import Note, Chord

    c = Chord('a', 'b', 'c')
    print(len(c.notes))  # 3


notes attribute
--------------------------------

You can only get the notes attribute but not set it!

.. code-block:: python

    from babs import Note, Chord

    c = Chord(strict=False)

    c.notes = [Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5)]

    # AttributeError: can't set attribute


add note
--------------------------------

You can use this method if you need to add a Note to the current chord. As we said before
a chord is an unordered collections of unique elements so you can't add the same note.


.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))

    c.add_note(note=Note(name='B'))

    print(len(c.notes))  # 4

    for n in c.notes:
        print(n)

    # G4
    # E4
    # C4
    # B4

    c.add_note(note=Note(name='C'))  # Add an existing Note

    print(len(c.notes))  # 4

By default strict is set to True, so if you add an invalid Note you will get a ChordException

.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G')).add_note(note='c')  # Add a string instead of a Note

    # ChordException: Instance of Note expected, str given.

    c = Chord('a', 'b', strict=False)
    c.add_note(note='c', strict=False)

    print(len(c.notes))  # 3


Otherwise if you try to add an invalid Note to a valid Chord you will get a AttributeError because of Note hash() function.

.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))
    c.add_note(note='c', strict=False)

    # AttributeError: 'str' object has no attribute 'freq'


remove note
--------------------------------
If you need to remove a Note you can use the remove_note() method.
You can remove a note by Note(), name, frequency or octave.

.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))
    c.remove_note(note=Note(name='G'))

    print(len(c.notes))  # 2

    for n in c.notes:
        print(n)

    # E4
    # C4

By default, as before, strict is set to True, so if a Note is not found or if the Chord will have less the two notes after remove
you will have a ChordException.

.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'), Note(name='E'))
    c.remove_note(note=Note(name='G'))
    # ChordException: Invalid request. Note not found in Chord.

    print(len(c.notes))  # 2

    c.remove_note(note=Note(name='E'))
    # Invalid request. Chords must have at least two notes.

    print(len(c.notes))  # 2


Removing a Note by octave or name can remove multiple notes.

.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))

    print(len(c.notes))  # 4

    c.remove_note(name='C')
    print(len(c.notes))  # 2

    for n in c.notes:
        print(n)

    # G4
    # E4

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

Chord support equal and not equal comparison operator. Two chords are the same if they have the same notes (check note comparison for more details).
The strict attribute doesn't affect the chord comparison.

.. code-block:: python

    from babs import Note, Chord

    Chord(Note(name='A'), Note(name='C')) == Chord(Note(name='A'), Note(name='C'))  # True
    Chord(Note(name='A'), Note(name='C'), strict=True) == Chord(Note(name='A'), Note(name='C'), strict=False)  # True
    Chord(Note(name='A'), Note(name='C')) == Chord(Note(name='A'), Note(name='C'), Note(name='E'))  # False
    Chord(Note(name='A'), Note(name='C')) != Chord(Note(name='A'), Note(name='C'))  # False


Create from root Note
--------------------------------

You can easily create a Chord from root note using the create_from_root classmethod.
Suppose you want create a C major chord.

.. code-block:: python

    from babs import Note, Chord

    c = Chord.create_from_root(root=Note(name='C'))
    for n in c.notes:
        print(n)

    # G4
    # E4
    # C4

That's it, you've got a C major chord.
So how it works? create_from_root use a chord_type, that is a list of notes distance from root note.
By default chord_type is the MAJOR_TYPE that has a major 3d and the 5th.
So the MAJOR_TYPE is simply a list [4, 7]. 4 is the distance between root from 3d and 7 between the root and the 5th.
The distance is based on the Note.NOTES list: NOTES = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
So let's say we want a major seven chord.

.. code-block:: python

    from babs import Note, Chord

    c = Chord.create_from_root(root=Note(name='C'), chord_type=[4, 7, 11])
    for n in c.notes:
        print(n)

    # G4
    # E4
    # C4
    # B4

babs come with some of pre-defined chord_type so that the previous example could be the same as

.. code-block:: python

    from babs import Note, Chord

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MAJOR_SEVEN_TYPE)

So you can use a custom list or use some of the pre-defined chord type.

By default the octave of other notes will be the same as the root note. To change that behaviour
you can use the octave param.
**The root note will not be affected by the octave param.**
octave could be :

- an integer, so that every note will have that specific octave.

.. code-block:: python

    from babs import Note, Chord

    c = Chord.create_from_root(root=Note(name='C'), chord_type=Chord.MAJOR_SEVEN_TYPE, octave=3)

    for n in c.notes:
        print(n)

    # G3
    # E3
    # C4
    # B3

- a string 'root' or 'from_root':
    - 'root', the default behaviour, use the root.octave.
    - 'from_root' use the root.octave as the starting octave. So if you have a G chord, G-B-D, the starting octave is 4 so we have a G4, then we have a B4 and at least the D Note goes to the next octave so is a D5

.. code-block:: python

    from babs import Note, Chord

    c = Chord.create_from_root(root=Note(name='G'), chord_type=Chord.MAJOR_TYPE, octave='from_root')

    for n in c.notes:
        print(n)

    # G4
    # D5
    # B4

- a callable, that must return an integer.
  In the callable you have access to root_octave, i (the idx of list distance iteration, starting from 0) and the distance between the current note and the root note.
  So suppose you want to have a Chord that looks like G4, B5, D6.

.. code-block:: python

    from babs import Note, Chord

    c = Chord.create_from_root(
            root=Note(name='G'),
            chord_type=Chord.MAJOR_TYPE, octave=lambda root_octave, i, distance: root_octave + i + 1
        )

    for n in c.notes:
        print(n)

    # G4
    # B5
    # D6



You can also specify the alteration of the notes using the alt param (by default is 'sharp') that works in the same way as for single note.

.. code-block:: python

    from babs import Note, Chord

    c = Chord.create_from_root(root=Note(name='G'), chord_type=Chord.MAJOR_SEVEN_TYPE)

    for n in c.notes:
        print(n)

    # G4
    # F#4
    # D4
    # B4

    c = Chord.create_from_root(root=Note(name='G'), chord_type=Chord.MAJOR_SEVEN_TYPE, alt='flat')

    for n in c.notes:
        print(n)

    # G4
    # Gb4
    # D4
    # B4


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

