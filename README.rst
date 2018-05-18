========
Babs! Music Library
========

========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis|

.. |travis| image:: https://travis-ci.org/iskyd/babs.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/iskyd/babs


+---------------------------+
| Supported python Version  |
+===========================+
| 3.4                       |
+---------------------------+
| 3.5                       |
+---------------------------+
| 3.6                       |
+---------------------------+


Installation
============
    git clone https://github.com/iskyd/babs
    
    cd babs
    
    python -m venv venv

    source venv/bin/activate
    
    pip install -e .

Runinng Test
============
    pip install pytest
    
    pytest

Code Coverage
============
    pip install pytest-cov
    
    pytest --cov=babs --cov-report=html
