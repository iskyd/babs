import abc

ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()}) #compatible with python 2 and 3

from babs import Note

from babs.exceptions import NoteListException


class NoteList(ABC):
    OCTAVE_TYPE_ROOT = 'root'

    def __init__(self, *notes):
        """
        :param notes: list of notes
        """
        self._notes = list(set(notes))
    
    def __eq__(self, other):
        return set(self._notes) == set(other.notes)

    def __ne__(self, other):
        return set(self._notes) != set(other.notes)
    
    def __str__(self):
        return ','.join(list(map(lambda n: str(n), self._notes)))

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, ','.join(list(map(lambda n: repr(n), self._notes))))

    @property
    def notes(self):
        return self._notes

    def add_note(self, note):
        """
        Add note to chord
        :param note: note to be added in chord
        :param strict: raise ChordException if note is not valid
        :return: None
        """

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
            indices = [key for key, n in enumerate(self._notes) if n == note]
        elif freq is not None:
            indices = [key for key, n in enumerate(self._notes) if n.freq == freq]
        elif name is not None:
            indices = [key for key, n in enumerate(self._notes) if n.name == name]
        elif octave is not None:
            indices = [key for key, n in enumerate(self._notes) if n.octave == octave]

        if strict is True and len(indices) == 0:
            raise NoteListException('Invalid request. Note not found in Chord.')

        if strict is True and len(self._notes) - len(indices) < 2:
            raise NoteListException('Invalid request. Chords must have at least two notes.')

        if len(indices) > 0:
            self._notes = [n for key, n in enumerate(self._notes) if key not in indices]
    
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
            elif octave == 'root':
                return root.octave
            elif octave == 'from_root':
                return root.octave + int(distance / len(Note.NOTES))
            else:
                return Note.A_DEFAULT_OCTAVE

        notes = [Note(
            name=Note.get_note_name_by_index(root_idx + distance, alt=alt),
            octave=get_octave(i, root_idx + distance),
            alt=alt
        ) for i, distance in enumerate(note_list_type)]

        notes.append(root)
        
        return notes
        