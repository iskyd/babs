from babs import Note, NoteList

from babs.exceptions import ChordException


class Chord(NoteList):
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

        self._notes = list(set(notes))

    def __repr__(self):
        return 'Chord({}, strict={})'.format(','.join(list(map(lambda n: repr(n), self._notes))), self.strict)

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

    @classmethod
    def create_from_root(cls, root, chord_type=None, octave=NoteList.OCTAVE_TYPE_ROOT, alt=Note.SHARP):
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
        
        notes = NoteList.get_notes_from_root(root=root, note_list_type=chord_type, octave=octave, alt=alt)

        return cls(
            *notes
        )
