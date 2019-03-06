from babs import Note, NoteList


class Scale(NoteList):
    """
    Set of musical notes ordered by fundamental frequency or pitch
    """

    MAJOR_TYPE = [2, 4, 5, 7, 9, 11]
    MINOR_TYPE = [2, 3, 5, 7, 8, 10]

    @classmethod
    def create_from_root(cls, root, scale_type=None, octave=NoteList.OCTAVE_TYPE_ROOT, alt=Note.SHARP):
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
        
        notes = NoteList.get_notes_from_root(root=root, note_list_type=scale_type, octave=octave, alt=alt)

        return cls(
            *notes
        )