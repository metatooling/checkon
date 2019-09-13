=====
Usage
=====

I maintain a library ``lib1``. ``lib1`` is used as a dependency by other libraries,
including ``lib2``. I want to make some changes to ``lib1``, but before releasing, I want
to make sure it won't break the code of my users in ``lib2``.

So I want to run ``lib2``'s test suite on the new version of ``lib1``.

.. code-block:: bash

    $ checkon test --inject ../lib1 dependents https://github.com/metatooling/lib2

Checkon will clone ``lib2``, run its test suite, and show if there are any failures.


.. code-block:: text

    envname    application                          classname        name          line  provider                                     message                                                         text
    ---------  -----------------------------------  ---------------  ----------  ------  -------------------------------------------  --------------------------------------------------------------  --------------------------------------------------------------------------------
    py37       https://github.com/metatooling/lib2  tests.test_lib2  test_three       7  git+https://github.com/metatooling/lib1.git  TypeError: add() takes 2 positional arguments but 3 were given  def test_three():
                                                                                                                                                                                                          >       assert lib2.app.add_args([1, 2, 3]) == 6

                                                                                                                                                                                                          tests/test_lib2.py:9:
                                                                                                                                                                                                          _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

                                                                                                                                                                                                          args = [1, 2, 3]

                                                                                                                                                                                                              def add_args(args: t.List[int]) -> int:
                                                                                                                                                                                                          >       return lib1.app.add(*args)
                                                                                                                                                                                                          E       TypeError: add() takes 2 positional arguments but 3 were given

                                                                                                                                                                                                          src/lib2/app.py:7: TypeError


Suppose I'm contributing to a popular library like `attrs <http://attrs.org>`__. I can retrieve a list of libraries depending on it from the web:

.. code-block:: bash


    $ checkon list dependents-from-librariesio --limit=5 attrs
    https://github.com/pytest-dev/pytest
    https://github.com/Julian/jsonschema
    https://github.com/twisted/twisted
    https://github.com/HypothesisWorks/hypothesis
    https://github.com/pypa/packaging



And I can run all their tests using my forked version of ``attrs``.

.. code-block:: bash

    $ checkon test --inject ../attrs dependents-from-librariesio --limit=5 attrs


Or pick test suites in a configuration file. The file can specify repositories and tox environments to run.


.. code-block:: toml

    # dependents.toml
    [[dependents]]
    repository = "https://github.com/Julian/jsonschema"
    toxenv_glob = "py37*"

    [[dependents]]
    repository = "https://github.com/twisted/twisted"
    toxenv_glob = "py37*"


.. code-block:: bash

    $ checkon test --inject ../attrs dependents-from-file ./dependents.txt
