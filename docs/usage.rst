=====
Usage
=====

I maintain a library ``lib1``. ``lib1`` is used as a dependency by other libraries,
including ``lib2``. I want to make some changes to ``lib1``, but before releasing, I want
to make sure it won't break the code of my users in ``lib2``.

So I want to run ``lib2``'s test suite on the new version of ``lib1``.

.. code-block:: bash

    $ checkon test --inject ../lib1 dependents https://github.com/metatooling/lib2.git

Checkon will clone ``lib2``, run its test suite, and show if there are any failures.


.. code-block::

    envname    application                              classname        name          line  provider                                     message                                                         text
    ---------  ---------------------------------------  ---------------  ----------  ------  -------------------------------------------  --------------------------------------------------------------  --------------------------------------------------------------------------------
    py37       https://github.com/metatooling/lib2.git  tests.test_lib2  test_three       7  git+https://github.com/metatooling/lib1.git  TypeError: add() takes 2 positional arguments but 3 were given  def test_three():
                                                                                                                                                                                                          >       assert lib2.app.add_args([1, 2, 3]) == 6

                                                                                                                                                                                                          tests/test_lib2.py:9:
                                                                                                                                                                                                          _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

                                                                                                                                                                                                          args = [1, 2, 3]

                                                                                                                                                                                                              def add_args(args: t.List[int]) -> int:
                                                                                                                                                                                                          >       return lib1.app.add(*args)
                                                                                                                                                                                                          E       TypeError: add() takes 2 positional arguments but 3 were given

                                                                                                                                                                                                          src/lib2/app.py:7: TypeError
