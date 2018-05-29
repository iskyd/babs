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

    def __repr__(self):
        return "Rest(value={})".format(self.value)

