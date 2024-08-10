import os
import tempfile

from py_dep_graph.filetree import FileTree


def walk_dict(path: str, d: dict):
    for key, item in d.items():
        # Create directory
        if isinstance(item, dict):
            new_dir = os.path.join(path, key)
            os.mkdir(new_dir)
            walk_dict(new_dir, item)

        # Create file
        else:
            filepath = os.path.join(path, key)
            with open(filepath, "w") as fp:
                fp.write("")


def create_test_filesystem(tmp_dir_root):
    dirs = {
        "pkg1": {"mod1.py": None, "mod2.py": None, "mod3.py": None},
        "pkg2": {"pkg4": {"mod4.py": None}},
        "pkg3": {"mod5.py": None},
        "mod6.py": None,
    }
    walk_dict(tmp_dir_root, dirs)


def test_filetree():
    with tempfile.TemporaryDirectory() as tmp_dir:
        create_test_filesystem(tmp_dir)

        file_tree = FileTree(tmp_dir)
        assert file_tree.root_directory.name == tmp_dir
        assert file_tree.root_directory.filepath == tmp_dir
        names = [child.name for child in file_tree.root_directory.children]
        assert sorted(names) == [
            "mod6.py",
            "pkg1",
            "pkg2",
            "pkg3",
        ]

        for child in file_tree.root_directory.children:
            if child.name == "pkg3":
                assert sorted([c.name for c in child.children]) == ["mod5.py"]
            elif child.name == "pkg1":
                assert sorted([c.name for c in child.children]) == ["mod1.py", "mod2.py", "mod3.py"]

            elif child.name == "pkg2":
                assert sorted([c.name for c in child.children]) == [
                    "pkg4",
                ]

                assert sorted([c.name for c in child.children[0].children]) == ["mod4.py"]
