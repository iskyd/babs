from babs import Note, NoteList

from babs.exceptions import BarException


class Bar(NoteList):
    """
    Segment of time corresponding to a specific number of beats in which each beat is represented by a particular note value
    """

    def __init__(self, *notes, time_signature=4/4, **kwargs):
        """
        :param notes: list of notes
        :param kwargs: options [strict]
        """

        self._time_signature = time_signature
        super().__init__(*notes, strict=kwargs.pop('strict', True), invalid_exception=BarException)

    @property
    def time_signature(self):
        return self._time_signature

    @time_signature.setter
    def time_signature(self, time_signature):
        self._time_signature = time_signature

    def is_valid(self):
        """
        Check if bar is valid
        :return: bool
        """

        if not super().is_valid():
            return False

        if sum(note.duration for note in self._notes) > self._time_signature:
            return False

        return True
    
    def add_note(self, note, strict=True):
        """
        Add note to list
        :param note: note to be added in list
        :param strict: raise BarException if note is not valid or if bar will be invalid
        :return: None
        """
        super().add_note(note=note, strict=strict)

    def remove_note(self, note=None, freq=None, name=None, octave=None, strict=True):
        """
        Remove note by note, freq, name or octave from list
        :param note: note to remove
        :param freq: frequency to remove
        :param name: name to remove
        :param octave: octave to remove
        :param strict: raise BarException if bar will be invalid after remove
        :return: None
        """
        super().remove_note(note=note, freq=freq, name=name, octave=octave, strict=strict)
