from babs import Note, NoteList

from babs.exceptions import ScaleException


class Scale(NoteList):
    """
    Set of musical notes ordered by fundamental frequency or pitch
    """

    ASCENDING_SCALE_TYPE='asc'
    DESCENDING_SCALE_TYPE='desc'

    MAJOR_TYPE = [2, 4, 5, 7, 9, 11]
    MINOR_TYPE = [2, 3, 5, 7, 8, 10]
    IONIAN_TYPE = MAJOR_TYPE
    DORIAN_TYPE = [2, 3, 5, 7, 9, 10]
    PHRIGIAN_TYPE = [1, 3, 5, 7, 8, 10]
    LIDYAN_TYPE = [2, 4, 6, 7, 9, 11]
    DOMINANT_TYPE = [2, 4, 5, 7, 9, 10]
    AEOLIAN_TYPE = MINOR_TYPE
    LOCRIAN_TYPE = [1, 3, 5, 6, 8, 10]
    PENTATONIC_TYPE = [2, 4, 7, 9]
    PENTATONIC_MINOR_TYPE = [3, 5, 7, 10]
    BLUES_TYPE = [2, 3, 4, 7, 9]
    BLUES_MINOR_TYPE = [3, 5, 6, 7, 10]
    MELODIC_MINOR_TYPE = [2, 3, 5, 7, 9, 11]
    HARMONIC_MINOR_TYPE = [2, 3, 5, 7, 8, 11]
    HARMONIC_MAJOR_TYPE = [2, 4, 5, 7, 8, 11]

    def __init__(self, *notes, **kwargs):
        """
        :param notes: list of notes
        :param kwargs: options [strict]
        """

        self._order_type = kwargs.pop('order', self.ASCENDING_SCALE_TYPE)

        super().__init__(*notes, strict=kwargs.pop('strict', True), invalid_exception=ScaleException)
        self._notes = list(set(self._notes))

        self._order()

    def _order(self):
        if self.is_valid():
            self._notes.sort(key=lambda note: note.freq, reverse=False if self._order_type == self.ASCENDING_SCALE_TYPE else True)

    def add_note(self, note, strict=True):
        """
        Add note to list
        :param note: note to be added in list
        :param strict: raise ScaleException if note is not valid, not found or if chord will be invalid
        :return: None
        """
        if note in self._notes:
            if strict is True:
                raise ScaleException('Note {} is alredy in Scale.'.format(str(note)))

            return

        super().add_note(note=note, strict=strict)
        self._order()

    def remove_note(self, note=None, freq=None, name=None, octave=None, strict=True):
        """
        Remove note by note, freq, name or octave from list
        :param note: note to remove
        :param freq: frequency to remove
        :param name: name to remove
        :param octave: octave to remove
        :param strict: raise ScaleException if note is not valid, not found or if scale will be invalid after remove
        :return: None
        """
        super().remove_note(note=note, freq=freq, name=name, octave=octave, strict=strict)
        self._order()

    @classmethod
    def create_from_root(cls, root, scale_type=None, octave=NoteList.OCTAVE_TYPE_ROOT, alt=Note.SHARP, order=None, strict=True):
        """
        :param root: root note
        :param scale_type: a list of notes distance from root note
        :param octave: octave of notes in chord
        :param alt: note alteration 'sharp' or 'flat'
        :type root: Note
        :type scale_type: list
        :type octave: Union[int, string, callable]
        :type alt: string
        :return: Scale
        """
        
        if scale_type is None:
            scale_type = cls.MAJOR_TYPE
        
        if order is None:
            order = Scale.ASCENDING_SCALE_TYPE

        notes = NoteList.get_notes_from_root(root=root, note_list_type=scale_type, octave=octave, alt=alt)

        return cls(
            *notes,
            order=order,
            strict=strict
        )