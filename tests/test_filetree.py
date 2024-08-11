from py_dep_graph.filetree import FileTree, walk_source_code_tree


def test_filetree(tmp_dir):
    file_tree = FileTree(tmp_dir)
    assert file_tree.root_directory.name == tmp_dir
    assert file_tree.root_directory.filepath == tmp_dir
    names = [child.name for child in file_tree.root_directory.children]
    assert sorted(names) == [
        "mod6",
        "pkg1",
        "pkg2",
        "pkg3",
    ]

    for child in file_tree.root_directory.children:
        if child.name == "pkg3":
            assert sorted([c.name for c in child.children]) == ["mod5"]
        elif child.name == "pkg1":
            assert sorted([c.name for c in child.children]) == ["mod1", "mod2", "mod3"]

        elif child.name == "pkg2":
            assert sorted([c.name for c in child.children]) == [
                "pkg4",
            ]

            assert sorted([c.name for c in child.children[0].children]) == ["mod4"]


def test_filetree_as_dict(tmp_dir):
    file_tree = FileTree(tmp_dir)

    d = file_tree.as_dict()
    root = d[tmp_dir]
    assert root == {
        "type": "dir",
        "children": {
            "pkg3": {
                "type": "dir",
                "children": {
                    "mod5": {
                        "type": "source_code_file",
                        "hash": "0b4231dfcd62cdd19ad235a3fa3ed3e01eb12ff262f259fafd4cd290d8e3d1a8",
                        "imports": ["pkg2.pkg4.mod4.some_func"],
                    }
                },
            },
            "pkg2": {
                "type": "dir",
                "children": {
                    "pkg4": {
                        "type": "dir",
                        "children": {
                            "mod4": {
                                "type": "source_code_file",
                                "hash": "f2ad41580e726691b2381b3b30e901e3d9bd70dadc6234b028b91f285b6bb693",
                                "imports": [],
                            }
                        },
                    }
                },
            },
            "pkg1": {
                "type": "dir",
                "children": {
                    "mod2": {
                        "type": "source_code_file",
                        "hash": "9e56cf21cd105ec7a715b0a355e4e8dcc1bd0ebd3f02935ee224063cfb6870d8",
                        "imports": [],
                    },
                    "mod3": {
                        "type": "source_code_file",
                        "hash": "7744ffeade24a187572ca745e99016402f56d196335bc2850bd43756e083a909",
                        "imports": ["mod6"],
                    },
                    "mod1": {
                        "type": "source_code_file",
                        "hash": "fe0d67af8c1aba435046c4843c788d4baf4ea29705b4757d3f8d54a20f62e81c",
                        "imports": [".mod2", ".mod3.stuff"],
                    },
                },
            },
            "mod6": {
                "type": "source_code_file",
                "hash": "79331d076c3b91d63f6d15f94cae2f9c1eeef2c32460b2cbb468e006bd37f420",
                "imports": ["os", "somelib"],
            },
        },
    }


def test_filetree_walk(tmp_dir):
    file_tree = FileTree(tmp_dir)
    source_code_nodes = walk_source_code_tree(file_tree.root_directory)

    assert len(source_code_nodes) == 6

    assert source_code_nodes[0].name == "mod5"
    assert source_code_nodes[0].parent.name == "pkg3"
