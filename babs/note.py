from __future__ import division

import math

from babs.exceptions import NoteException


class Note(object):
    """
    Musical note
    """

    A_FREQUENCY = 440
    NOTES = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    HALF_STEP_INTERVAL = 2 ** (1 / 12)

    def __init__(self, freq=None, name=None, octave=4, alt=None, value=1/4.0):
        """
        :param freq: frequency
        :param name: name of the note
        :param octave: note's position on a standard 88-key piano keyboard
        :param alt: note's alteration, could be sharp or flat. used to choose name (e.g D# or Eb)
        :param value: relative duration of the note
        """
        self._freq = freq
        self._name = name
        self._octave = octave
        self._alt = alt
        self.value = value

        if self._freq is None and self._name is None:
            raise NoteException("Can't create a note without frequency or name.")

        if self._name is not None and self._get_note_index() is False:
            raise NoteException("Invalid note.")

        if self._freq is None:
            self._set_freq()
        else:
            self._set_name_and_octave()

        self._freq = round(self._freq, 2)
    
    def __eq__(self, other):
        return self._freq == other.freq

    def __ne__(self, other):
        return self._freq != other.freq

    def __lt__(self, other):
        return self._freq < other.freq

    def __le__(self, other):
        return self._freq <= other.freq

    def __gt__(self, other):
        return self._freq > other.freq

    def __ge__(self, other):
        return self._freq >= other.freq

    def __repr__(self):
        return "Note(freq={}, alt='{}')".format(self._freq, self.alt)

    def __str__(self):
        return "{}{}".format(self._name, self._octave)

    def _get_note_index(self):
        """
        :return: position of the note in self.NOTES or False if not found
        """
        idx = 0
        for note in self.NOTES:
            names = note.split('/')
            for name in names:
                if self._name == name:
                    return idx
            idx += 1

        return False

    def _set_name_and_octave(self):
        """
        calculate and set _name and _octave based on freq and alt
        """
        octave = 4
        distance = int(round(len(self.NOTES) * (math.log(float(self._freq), 2) - math.log(self.A_FREQUENCY, 2))))
        oct_summer = 1

        if distance < -self.NOTES.index('A'):
            distance = -distance
            oct_summer = -1

        while distance + self.NOTES.index('A') - len(self.NOTES) >= 0:
            octave += oct_summer
            distance = distance - len(self.NOTES)

        names = self.NOTES[self.NOTES.index('A') + int(distance)].split('/')
        self._name = names[0]

        if len(names) > 1 and self._alt == 'flat':
            self._name = names[1]

        self._octave = octave

    def _set_freq(self):
        """
        calculate and set freq based on name and octave
        """
        note_distance = self._get_note_index() - self.NOTES.index('A')
        oct_distance = self._octave - 4
        distance = note_distance + (len(self.NOTES) * oct_distance)

        self._freq = self.A_FREQUENCY * (self.HALF_STEP_INTERVAL ** distance)

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, freq):
        self._freq = freq
        self._set_name_and_octave()

    @property
    def name(self):
        return self._name

    @property
    def octave(self):
        return self._octave

    @property
    def alt(self):
        return self._alt

    @alt.setter
    def alt(self, alt):
        self._alt = alt
        self._set_name_and_octave()

    def pitch_shift(self, val, half_step=False, octave=False, alt=None):
        """
        change the freq and calculate name and octave
        :param val: value to add or sub from freq
        :param half_step: if True val is based as half tone
        :param octave: if True val is based on octave
        :param alt: note's alteration, could be sharp or flat. used to choose name (e.g D# or Eb)
        """
        if self._alt is not None:
            self._alt = alt
        if half_step is True:
            self._freq = round(self._freq * (self.HALF_STEP_INTERVAL ** val), 2)
        elif octave is True:
            self._freq = round(self._freq * (2 ** val), 2)
        else:
            self._freq = round(self._freq + val, 2)

        self._set_name_and_octave()
