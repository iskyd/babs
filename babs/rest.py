from __future__ import division


class Rest:
    """
    Interval of silence
    """

    def __init__(self, value=4/4):
        """
        :param value: relative duration of the rest
        """
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __repr__(self):
        return "Rest(value={})".format(self.value)
