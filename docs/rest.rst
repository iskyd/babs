Rest
================================

.. py:class:: Rest(value=4/4)

    Return a rest, an interval of silence

__repr__
--------------------------------

__repr__ will return the current representation of the Rest so that you can call eval() on it.

.. code-block:: python

    repr(Rest(value=1/4)) # 'Rest(value=0.25)'

    r = Rest(value=1/4)
    x = eval(repr(r)) # x will be the same as r