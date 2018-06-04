from babs import Note
from babs.exceptions import ChordException


class Chord(object):
    """
    Any harmonic set of pitches consisting of two or more notes
    """

    def __init__(self, *notes, **kwargs):
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
        if len(self._notes) < 2:
            return False

        for n in self._notes:
            if not isinstance(n, Note):
                return False

        return True

    def add_note(self, note, strict=True):
        if strict is True:
            if not isinstance(note, Note):
                error = 'Instance of Note expected, {} given.'.format(type(note).__name__)
                raise ChordException(error)

        if note not in self._notes:
            self._notes.append(note)

    def remove_note(self, note=None, freq=None, name=None, octave=None, strict=True):
        indices = []
        if note is not None:
            if strict is True and not isinstance(note, Note):
                raise ChordException("Instance of Note expected, {} given.".format(type(note).__name__))
            indices = [key for key, n in enumerate(self._notes) if n == note]
        if freq is not None:
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
