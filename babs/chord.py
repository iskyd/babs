from babs import Note
from babs.exceptions import ChordException


class Chord(object):
    """
    Any harmonic set of pitches consisting of two or more notes
    """

    MAJOR_TYPE = [4, 7]
    MAJOR_SEVEN_TYPE = [4, 7, 11]
    MINOR_TYPE = [3, 7]
    MINOR_SEVEN_TYPE = [3, 7, 10]
    DOMINANT_TYPE = [4, 7, 10]
    MINOR_MAJOR_SEVEN_TYPE = [3, 7, 11]
    HALF_DIMINISHED_SEVEN_TYPE = [3, 6, 10]
    DIMINISHED_TYPE = [3, 6]
    DIMINISHED_SEVEN_TYPE = [3, 6, 9]
    AUGMENTED_TYPE = [4, 8]
    AUGMENTED_SEVEN_TYPE = [4, 8, 10]
    AUGMENTED_MAJOR_SEVEN_TYPE = [4, 8, 11]
    MAJOR_SIXTH_TYPE = [4, 7, 9]
    MINOR_SIXTH_TYPE = [3, 7, 9]
    SUS4_TYPE = [5, 7]
    SUS4_SEVEN_TYPE = [5, 7, 10]
    SUS4_MAJOR_SEVEN_TYPE = [5, 7, 11]
    SUS2_TYPE = [2, 7]
    SUS2_SEVEN_TYPE = [2, 7, 10]
    SUS2_MAJOR_SEVEN_TYPE = [2, 7, 11]

    def __init__(self, *notes, **kwargs):
        """
        :param notes: list of notes
        :param kwargs: options [strict]
        """
        self.strict = kwargs.pop('strict', True)
        if self.strict is True:
            if len(notes) < 2:
                raise ChordException('Chords must have at least two notes, {} given.'.format(len(notes)))

            for n in notes:
                if not isinstance(n, Note):
                    error = 'Invalid Chord, instance of note expected but {} given.'.format(type(n).__name__)
                    raise ChordException(error)

        self._notes = list(set(notes))

    def __eq__(self, other):
        return set(self.notes) == set(other.notes)

    def __ne__(self, other):
        return set(self.notes) != set(other.notes)

    def __str__(self):
        return ','.join(list(map(lambda n: str(n), self.notes)))

    def __repr__(self):
        return 'Chord({}, strict={})'.format(','.join(list(map(lambda n: repr(n), self.notes))), self.strict)

    @property
    def notes(self):
        return self._notes

    def is_valid(self):
        """
        Check if chord is valid
        :return: bool
        """
        if len(self._notes) < 2:
            return False

        for n in self._notes:
            if not isinstance(n, Note):
                return False

        return True

    def add_note(self, note, strict=True):
        """
        Add note to chord
        :param note: note to be added in chord
        :param strict: raise ChordException if note is not valid
        :return: None
        """
        if strict is True:
            if not isinstance(note, Note):
                error = 'Instance of Note expected, {} given.'.format(type(note).__name__)
                raise ChordException(error)

        if note not in self._notes:
            self._notes.append(note)

    def remove_note(self, note=None, freq=None, name=None, octave=None, strict=True):
        """
        Remove note by note, freq, name or octave from chord
        :param note: note to remove
        :param freq: frequency to remove
        :param name: name to remove
        :param octave: octave to remove
        :param strict: raise ChordException if note is not valid, not found or if chord will be invalid
        :return: None
        """
        indices = []
        if note is not None:
            if strict is True and not isinstance(note, Note):
                raise ChordException("Instance of Note expected, {} given.".format(type(note).__name__))
            indices = [key for key, n in enumerate(self._notes) if n == note]
        elif freq is not None:
            indices = [key for key, n in enumerate(self._notes) if n.freq == freq]
        elif name is not None:
            indices = [key for key, n in enumerate(self._notes) if n.name == name]
        elif octave is not None:
            indices = [key for key, n in enumerate(self._notes) if n.octave == octave]

        if strict is True and len(indices) == 0:
            raise ChordException("Invalid request. Note not found in Chord.")

        if strict is True and len(self._notes) - len(indices) < 2:
            raise ChordException("Invalid request. Chords must have at least two notes.")

        if len(indices) > 0:
            self._notes = [n for key, n in enumerate(self._notes) if key not in indices]

    @classmethod
    def create_from_root(cls, root, chord_type=None, octave='root', alt='sharp'):
        """
        :param root: root note
        :param chord_type: a list of notes distance from root note
        :param octave: octave of notes in chord
        :param alt: note alteration 'sharp' or 'flat'
        :type root: Note
        :type chord_type: list
        :type octave: Union[int, string, callable]
        :type alt: string
        :return: Chord
        """
        if chord_type is None:
            chord_type = cls.MAJOR_TYPE

        root_idx = root.get_note_index()

        def get_octave(i, distance):
            if callable(octave):
                return octave(root.octave, i, distance)
            elif isinstance(octave, int):
                return octave
            elif octave == 'root':
                return root.octave
            elif octave == 'from_root':
                return root.octave + int(distance / len(Note.NOTES))
            else:
                return Note.A_DEFAULT_OCTAVE

        return cls(
            root,
            *(Note(
                    name=Note.get_note_name_by_index(root_idx + distance, alt=alt),
                    octave=get_octave(i, root_idx + distance),
                    alt=alt
            ) for i, distance in enumerate(chord_type))
        )
