Installation
================================

Download babs

.. code-block:: bash

    git clone https://github.com/iskyd/babs
    cd babs

Create virtual environment (OPTIONALS)

.. code-block:: bash

    python -m venv venv

If you are using python you can use virtualenv

Install babs

.. code-block:: bash

    pip install -e .


Test
--------------------------------

.. code-block:: bash

    pip install pytest
    pytest

Run single test

.. code-block:: bash

    pytest tests/[test_file.py]


Coverage
--------------------------------
.. code-block:: bash

    pip install pytest-cov
    pytest --cov=babs --cov-report html:htmlcov

It will create htmlcov directory with html report.

If everything goes well... You are ready to get started!