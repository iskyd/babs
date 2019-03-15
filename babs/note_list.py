from abc import ABC

from babs import Note

from babs.exceptions import NoteListException


class NoteList(ABC):
    OCTAVE_TYPE_ROOT = 'root'
    OCTAVE_TYPE_FROM_ROOT = 'from_root'

    def __init__(self, *notes, **kwargs):
        """
        :param notes: list of notes
        """
        self._notes = list(notes)
        self.strict = kwargs.pop('strict', True)
        self.invalid_exception = kwargs.pop('invalid_exception', NoteListException)

        if self.strict is True and self.is_valid() is False:
            raise self.invalid_exception('Invalid {}.'.format(type(self).__name__))
    
    def __eq__(self, other):
        return self._notes == other.notes

    def __ne__(self, other):
        return self._notes != other.notes
    
    def __str__(self):
        return ','.join(list(map(lambda n: str(n), self._notes)))

    def __repr__(self):
        return '{}({}, strict={})'.format(type(self).__name__, ','.join(list(map(lambda n: repr(n), self._notes))), self.strict)

    @property
    def notes(self):
        return self._notes

    def is_valid(self):
        """
        Check if list is valid
        :return: bool
        """
        if len(self._notes) < 1:
            return False
        
        for n in self._notes:
            if not isinstance(n, Note):
                return False

        return True

    def add_note(self, note, strict=True):
        """
        Add note to list
        :param note: note to be added in list
        :param strict: raise NoteListException if note is not valid
        :return: None
        """
        if strict and not isinstance(note, Note):
            raise self.invalid_exception('Invalid note given.')
        
        self._notes.append(note)
    
    def remove_note(self, note=None, freq=None, name=None, octave=None, strict=True):
        """
        Remove note by note, freq, name or octave from list
        :param note: note to remove
        :param freq: frequency to remove
        :param name: name to remove
        :param octave: octave to remove
        :param strict: raise NoteListException if note is not valid, not found or if list will be invalid after remove
        :return: None
        """

        notes = self._notes

        indices = []
        if note is not None:
            indices = [key for key, n in enumerate(self._notes) if n == note]
        elif freq is not None:
            indices = [key for key, n in enumerate(self._notes) if n.freq == freq]
        elif name is not None:
            indices = [key for key, n in enumerate(self._notes) if n.name == name]
        elif octave is not None:
            indices = [key for key, n in enumerate(self._notes) if n.octave == octave]

        if len(indices) > 0:
            self._notes = [n for key, n in enumerate(self._notes) if key not in indices]

        if strict is True and not self.is_valid():
            self._notes = notes
            raise self.invalid_exception('Invalid {}.'.format(type(self).__name__))
    
    @classmethod
    def get_notes_from_root(cls, root, note_list_type=None, octave=None, alt=Note.SHARP):
        """
        :param root: root note
        :param note_list_type: a list of notes distance from root note
        :param octave: octave of notes in chord
        :param alt: note alteration 'sharp' or 'flat'
        :type root: Note
        :type note_list_type: list
        :type octave: Union[int, string, callable]
        :type alt: string
        :return: Scale
        """
        
        if note_list_type is None:
            raise NoteListException('Invalid note list type')
        
        if octave is None:
            octave = cls.OCTAVE_TYPE_ROOT
        
        root_idx = root.get_note_index()

        def get_octave(i, distance):
            if callable(octave):
                return octave(root.octave, i, distance)
            elif isinstance(octave, int):
                return octave
            elif octave == cls.OCTAVE_TYPE_ROOT:
                return root.octave
            elif octave == cls.OCTAVE_TYPE_FROM_ROOT:
                return root.octave + int(distance / len(Note.NOTES))
            else:
                return Note.A_DEFAULT_OCTAVE

        notes = [Note(
            name=Note.get_note_name_by_index(root_idx + distance, alt=alt),
            octave=get_octave(i, root_idx + distance),
            alt=alt
        ) for i, distance in enumerate(note_list_type)]

        notes.insert(0, root)
        
        return notes
        