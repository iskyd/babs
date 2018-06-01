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


Create your first chord
--------------------------------

.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'))

Now you have create the C chord and you can access to the notes attribute.

.. code-block:: python

    for n in c.notes:
        print(str(n))

    # G4
    # E4
    # C4

So this come the first important thing, why the first note is a G4 and not a C4?
Because notes is an unordered collections of unique elements (note) even if it is a list.
So we can't add the same Note multiple times, let's take a try.

.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C'))

    print(len(c.notes))  # 3

    for n in c.notes:
        print(str(n))

    # G4
    # E4
    # C4

Remember that Note(name='C') is not equal to Note(name='C', octave=5)

.. code-block:: python

    from babs import Note, Chord

    c = Chord(Note(name='C'), Note(name='E'), Note(name='G'), Note(name='C', octave=5))

    print(len(c.notes))  # 4

    for n in c.notes:
        print(str(n))

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
