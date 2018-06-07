Rest
================================

.. py:class:: Rest(duration=4/4)

    Return a rest, an interval of silence.
    duration represent the relative duration of the rest.

__repr__
--------------------------------

__repr__ will return the current representation of the Rest so that you can call eval() on it.

.. code-block:: python

    repr(Rest(duration=1/4))  # 'Rest(duration=0.25)'

    r = Rest(duration=1/4)
    x = eval(repr(r))  # x will be the same as r

Comparison
--------------------------------
Rest support all comparison operator.
This is just a shortcut of using .duration attribute.

.. code-block:: python

    Rest(duration=1/8) < Rest(duration=1/4) == Rest(duration=1/8).duration < Rest(duration=1/4).duration  # True