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

        super().__init__(*notes, strict=kwargs.pop('strict', True), invalid_exception=ChordException)
        self._order()

    def _order(self):
        if self.is_valid():
            self._notes.sort(key=lambda note: note.freq, reverse=False)

    def is_valid(self):
        """
        Check if chord is valid
        :return: bool
        """

        if not super().is_valid():
            return False

        if len(self._notes) < 2:
            return False

        return True
    
    def add_note(self, note, strict=True):
        """
        Add note to list
        :param note: note to be added in list
        :param strict: raise NoteException if note is not valid, not found or if chord will be invalid
        :return: None
        """
        super().add_note(note=note, strict=strict)
        self._order()

    def remove_note(self, note=None, freq=None, name=None, octave=None, strict=True):
        super().remove_note(note=note, freq=freq, name=name, octave=octave, strict=strict)
        self._order()

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
