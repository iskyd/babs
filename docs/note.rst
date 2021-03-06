Note
================================

.. py:class:: Note(freq, name, octave=4, alt='sharp', duration=4/4)

    Return a musical Note representation from frequency or name

    .. py:method:: pitch_shift(val[, half_step=False, octave=False, alt=None])

        change the frequency of the current note

    .. py:method:: get_note_index()

        return the note index in Note.NOTES or False if not found

    .. py:classmethod:: get_note_name_by_index(idx[, alt=None])

        return the name of the note at specified idx in Note.NOTES.
        idx could be any number so that you don't have to worry about idx > len(Note.NOTES)

Create your first note
--------------------------------

.. code-block:: python

    from babs import Note

    n = Note(freq=440)


Now you have create a Note with 440Hz of frequency (the A at 4th octave).
So you now have access to attribute's note.

.. code-block:: python

    print(n.freq)  # 440
    print(n.name)  # 'A'
    print(n.octave)  # 4
    print(n.duration)  # 1.0 (4/4)

You can also create a note starting from it name.

.. code-block:: python

    n = Note(name='A')

    print(n.freq)  # 440
    print(n.name)  # 'A'
    print(n.octave)  # 4
    print(n.duration)  # 1.0 (4/4)

The freq params have the priority so if you specify the frequency, name and octave will be ignored:

.. code-block:: python

    n = Note(freq=440, name='B', octave=3)

    print(n.freq)  # 440
    print(n.name)  # 'A'
    print(n.octave)  # 4


Octave
--------------------------------

The octave is note's position on a standard 88-key piano keyboard and by default (as you can see in the previous example) is 4.

.. code-block:: python

    n = Note(name='A', octave=5)

    print(n.freq)  # 880.0
    print(n.name)  # 'A'
    print(n.octave)  # 5
    print(n.duration)  # 1.0 (4/4)


Alteration
--------------------------------

Now let's create a Bb note.

.. code-block:: python

    n = Note(freq=466.16)
    print(n.name)  # 'A#'

So we got A# as name because the A# and the Bb note has the same frequency. But what if you need to get a Bb? You can use alteration attribute.

.. code-block:: python

    n = Note(freq=466.16, alt='flat')

    print(n.name)  # 'Bb'


Duration
--------------------------------
The duration represent the relative duration of the note.

.. code-block:: python

    n = Note(name='A', duration=3/4)

    print(n.duration)  # 0.75 -> 3/4

You can change the duration of the note simply using the setter.

.. code-block:: python

    print(n.duration)  # 0.75 -> 3/4
    n.duration = 2/4
    print(n.duration)  # 0.5 -> 3/4


Change attribute
--------------------------------

You can easily change the note frequency and the note alteration. Babs will calculate again the name and the octave of the note.

.. code-block:: python

    n = Note(freq=440)

    print(n.name)  # 'A'

    n.freq = 466.16
    print(n.name)  # 'A#'

    n.alt = 'flat'
    print(n.name)  # 'Bb'

    n.freq = 880
    print(n.name)  # 'A'
    print(n.octave)  # 5


Pitch shift
--------------------------------

If you need more control to alter a note then just using the freq setter you can use a more powerful function, the pitch shift.
The pitch shift can be used in three different way.

* Add or sub a frequency value

.. code-block:: python

    n = Note(freq=440)

    n.pitch_shift(value=26.16)  # Increase the freq by 26.16hz
    print(n.freq)  # 466.16
    print(n.name)  # 'A#'

    n.pitch_shift(value=-26.16)  # Decrease the freq by 26.16hz
    print(n.freq)  # 440.0
    print(n.name)  # 'A'

* Add or sub an octave value

.. code-block:: python

    n = Note(freq=440)

    n.pitch_shift(value=2, octave=True) # Add 2 octaves
    print(n.freq)  # 1760.0
    print(n.name)  # 'A'
    print(n.octave)  # 6

    n.pitch_shift(value=-3, octave=True) # Sub 3 octaves
    print(n.freq)  # 220.0
    print(n.name)  # 'A'
    print(n.octave)  # 3

* Add or sub an half tone value

.. code-block:: python

    n = Note(freq=440)

    n.pitch_shift(value=2, half_step=True) # Add 1 tone (2 half tones)
    print(n.freq)  # 493.88
    print(n.name)  # 'B'
    print(n.octave)  # 4

    n.pitch_shift(value=-12, half_step=True) # Sub 6 tones (6 tones = 1 octave)
    print(n.freq)  # 246.94
    print(n.name)  # 'B'
    print(n.octave)  # 3

With half_step and octave you can specify the alteration you need as before

.. code-block:: python

    n = Note(freq=440)

    n.pitch_shift(value=1, half_step=True, alt='flat')  # Add half tone
    print(n.freq)  # 466.16
    print(n.name)  # 'Bb'
    print(n.octave)  # 4

Remember that 0 is a valid value so the following will works:

.. code-block:: python

    n = Note(freq=466.16)

    n.pitch_shift(value=0, alt='flat')  # Add half tone
    print(n.freq)  # 466.16
    print(n.name)  # 'Bb'
    print(n.octave)  # 4

Consider that we can obtain the same result in this **recommended** way without using the pitch shift function:

.. code-block:: python

    n = Note(freq=466.16)

    n.alt = 'flat'  # Add half tone
    print(n.freq)  # 466.16
    print(n.name)  # 'Bb'
    print(n.octave)  # 4


__str__ and __repr__
--------------------------------

__str__ will return the current name and octave of the note.

.. code-block:: python

    str(Note(freq=440))  # 'A4'

__repr__ will return the current representation of the Note so that you can call eval() on it.

.. code-block:: python

    repr(Note(freq=440))  # 'Note(freq=440, alt='None', duration=1.0)'

    n = Note(freq=440, duration=1/8)  # repr(n) -> Note(freq=440, alt='None', duration=0.125)
    x = eval(repr(x))  # x will be the same as n


Comparison
--------------------------------

Note support equal and not equal comparison operator. Two notes are the same if they have the same frequency and the same duration.

.. code-block:: python

    Note(name='A') == Note(name='A')  # True
    Note(name='A') == Note(name='A', duration=1/8)  # False
    Note(name='A') != Note(name='C')  # True
    Note(name='A') != Note(name='A', duration=1/8)  # True


