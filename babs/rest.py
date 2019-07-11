from __future__ import division

from babs import Interval


class Rest(Interval):
    """
    Interval of silence
    Note without a sound
    """

    def __init__(self, duration=4/4):
        """
        :param duration: relative duration of the rest
        """
        self.duration = duration

    def __eq__(self, other):
        return self.duration == other.duration

    def __ne__(self, other):
        return self.duration != other.duration

    def __lt__(self, other):
        return self.duration < other.duration

    def __le__(self, other):
        return self.duration <= other.duration

    def __gt__(self, other):
        return self.duration > other.duration

    def __ge__(self, other):
        return self.duration >= other.duration

    def __repr__(self):
        return "Rest(duration={})".format(self.duration)
