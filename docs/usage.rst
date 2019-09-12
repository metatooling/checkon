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
