======================================
Babs! Music Library
======================================

======================================
Overview
======================================

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|

.. |docs| image:: https://readthedocs.org/projects/babs/badge/?style=flat
    :target: https://readthedocs.org/projects/babs
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/iskyd/babs.svg?branch=dev
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/iskyd/babs


+---------------------------+
| Supported python Version  |
+===========================+
| 2.7                       |
+---------------------------+
| 3.4                       |
+---------------------------+
| 3.5                       |
+---------------------------+
| 3.6                       |
+---------------------------+


Installation
======================================
    git clone https://github.com/iskyd/babs
    
    cd babs
    
    pip install -e .

Runinng Test
======================================
    pip install pytest
    
    pytest

Code Coverage
======================================
    pip install pytest-cov
    
    pytest --cov=babs --cov-report=html
