import os
import tempfile

import pytest

mock_files = {
    "mod1.py": """
    import .mod2
    from .mod3 import stuff
""",
    "mod2.py": """

    def my_func():
        pass

""",
    "mod3.py": """

    import mod6

    def stuff():
        print("hello stuff")

""",
    "mod4.py": """

    def some_func():
        pass

""",
    "mod5.py": """
   from pkg2.pkg4.mod4 import some_func

""",
    "mod6.py": """
    import os
    import somelib
""",
}


def _walk_dict(path: str, d: dict):
    for key, item in d.items():
        # Create directory
        if isinstance(item, dict):
            new_dir = os.path.join(path, key)
            os.mkdir(new_dir)
            _walk_dict(new_dir, item)

        # Create file
        else:
            filepath = os.path.join(path, key)
            with open(filepath, "w") as fp:
                file_contents = mock_files[key]
                fp.write(file_contents)


def _create_test_filesystem(tmp_dir_root):
    dirs = {
        "pkg1": {"mod1.py": None, "mod2.py": None, "mod3.py": None},
        "pkg2": {"pkg4": {"mod4.py": None}},
        "pkg3": {"mod5.py": None},
        "mod6.py": None,
    }
    _walk_dict(tmp_dir_root, dirs)


@pytest.fixture(scope="session")
def tmp_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        _create_test_filesystem(tmp_dir)
        yield tmp_dir
