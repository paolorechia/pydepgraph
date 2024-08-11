import os
import tempfile

from py_dep_graph.filetree import FileTree

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

    def stuff():
        print("hello stuff")

""",
    "mod4.py": "",
    "mod5.py": "",
    "mod6.py": "",
}


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
                file_contents = mock_files[key]
                fp.write(file_contents)


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


def test_filetree_as_dict():
    with tempfile.TemporaryDirectory() as tmp_dir:
        create_test_filesystem(tmp_dir)
        file_tree = FileTree(tmp_dir)

        d = file_tree.as_dict()
        root = d[tmp_dir]
        assert root == {
            "type": "dir",
            "children": {
                "pkg3": {
                    "type": "dir",
                    "children": {
                        "mod5.py": {
                            "type": "source_code_file",
                            "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                        }
                    },
                },
                "pkg2": {
                    "type": "dir",
                    "children": {
                        "pkg4": {
                            "type": "dir",
                            "children": {
                                "mod4.py": {
                                    "type": "source_code_file",
                                    "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                                }
                            },
                        }
                    },
                },
                "pkg1": {
                    "type": "dir",
                    "children": {
                        "mod2.py": {
                            "type": "source_code_file",
                            "hash": "9e56cf21cd105ec7a715b0a355e4e8dcc1bd0ebd3f02935ee224063cfb6870d8",
                        },
                        "mod3.py": {
                            "type": "source_code_file",
                            "hash": "af29547b948ff540e18cde4494b87a77a32b0c0b80c79e3c3a963abf36355002",
                        },
                        "mod1.py": {
                            "type": "source_code_file",
                            "hash": "fe0d67af8c1aba435046c4843c788d4baf4ea29705b4757d3f8d54a20f62e81c",
                        },
                    },
                },
                "mod6.py": {
                    "type": "source_code_file",
                    "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                },
            },
        }
