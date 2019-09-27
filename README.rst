========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/checkon/badge/?style=flat
    :target: https://readthedocs.org/projects/checkon
    :alt: Documentation Status


.. |travis| image:: https://img.shields.io/travis/com/metatooling/checkon/master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/metatooling/checkon

.. |version| image:: https://img.shields.io/pypi/v/checkon.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/pypi/checkon

.. |commits-since| image:: https://img.shields.io/github/commits-since/metatooling/checkon/v0.1.4.svg
    :alt: Commits since latest release
    :target: https://github.com/metatooling/checkon/compare/v0.1.4...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/checkon.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/pypi/checkon

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/checkon.svg
    :alt: Supported versions
    :target: https://pypi.org/pypi/checkon

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/checkon.svg
    :alt: Supported implementations
    :target: https://pypi.org/pypi/checkon


.. end-badges


Checkon is a tool to help library maintainers ensure backward-compatibilty by running downstream applications' test suites with library pre-release versions.

Supported meta-runners:

- tox_

Supported test-runners:

- PyTest_
- Trial_


Currently missing support for:

- unittest_
- nose_


Installation
============

::

    pip install checkon

Documentation
=============


https://checkon.readthedocs.io/


.. _tox: https://tox.readthedocs.io/en/latest/index.html
.. _PyTest: https://pytest.org
.. _Trial: https://twistedmatrix.com/trac/wiki/TwistedTrial
.. _unittest: https://docs.python.org/3/library/unittest.html
.. _nose: https://nose.readthedocs.io/en/latest/
