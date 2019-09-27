=====
Usage
=====

I maintain a library ``lib1``. ``lib1`` is used as a dependency by other libraries,
including ``lib2``. I want to make some changes to ``lib1``, but before releasing, I want
to make sure it won't break the code of my users in ``lib2``.

So I want to run ``lib2``'s test suite on the new version of ``lib1``.

.. code-block:: bash

    $ checkon test \
    --inject--new ../lib1 \
    --inject-base git+https://github.com/metatooling/lib1.git@master \
    dependents https://github.com/metatooling/lib2.git

Checkon will clone ``lib2``, run its test suite via ``tox``, and show if there are any
failures in the version on my branch specified by ``--inject-new`` that pass under the
``master`` verion on GitHub specified by ``--inject-base``. :download:`(Expand.) <table.txt>`

.. literalinclude:: table.txt


Suppose I'm contributing to a popular project like `attrs <http://attrs.org>`__. I can retrieve a list of projects depending on it from the web:

.. code-block:: bash


    $ checkon list dependents-from-librariesio --limit=5 attrs
    https://github.com/pytest-dev/pytest
    https://github.com/Julian/jsonschema
    https://github.com/twisted/twisted
    https://github.com/HypothesisWorks/hypothesis
    https://github.com/pypa/packaging



And I can run all their tests using my forked version of ``attrs``.

.. code-block:: bash

    $ checkon test \
    --inject-new ../attrs \
    --inject-base git+https://github.com/python-attrs/attrs \
    dependents-from-librariesio --limit=5 attrs


Or pick test suites in a configuration file. The file can specify repositories and tox environments to run.


.. code-block:: toml

    # dependents.toml
    [[dependents]]
    repository = "https://github.com/Julian/jsonschema"
    toxenv_regex = "py37"

    [[dependents]]
    repository = "https://github.com/twisted/twisted"
    toxenv_regex = "py37"


.. code-block:: bash

    $ checkon test \
    --inject-new ../attrs \
    --inject-base git+https://github.com/python-attrs/attrs \
    dependents-from-file ./dependents.txt


I can check all the pull requests in the ``attrs`` repository against specified dependents.

.. code-block:: bash

    $ checkon test \
    --output-format=json \
    --inject-pull-requests https://github.com/python-attrs/attrs \
    --inject-base git+https://github.com/python-attrs/attrs@master \
    dependents-from-file dependents.toml
