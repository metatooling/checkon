import json
import subprocess
import sys


def test_test():
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "checkon",
            "test",
            "--log-file",
            "/dev/stderr",
            "--output-format=json",
            "--upstream-new",
            "git+https://github.com/metatooling/lib1.git",
            "--upstream-base",
            "git+https://github.com/metatooling/lib1.git@9b874f537d4a21b3de34df32f2b3d51e59240dd2",
            "dependents",
            "https://github.com/metatooling/lib2.git",
        ],
        capture_output=True,
    )

    expected = [
        {
            "envname": "coverage",
            "application": "https://github.com/metatooling/lib2.git",
            "classname": "tests.test_lib2",
            "name": "test_three",
            "line": 7,
            "provider": "git+https://github.com/metatooling/lib1.git",
            "message": "TypeError: add() takes 2 positional arguments but 3 were given",
            "text": "def test_three():\n>       assert lib2.app.add_args([1, 2, 3]) == 6\n\ntests/test_lib2.py:9: \n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ \n\nargs = [1, 2, 3]\n\n    def add_args(args: t.List[int]) -> int:\n>       return lib1.app.add(*args)\nE       TypeError: add() takes 2 positional arguments but 3 were given\n\nsrc/lib2/app.py:7: TypeError",
        }
    ]

    assert json.loads(proc.stdout.decode()) == expected
