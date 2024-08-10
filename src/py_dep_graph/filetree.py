from __future__ import annotations

import os


class Node:
    """Represents an abstract generic node (dir or file)"""

    def __init__(self, name: str, filepath: str) -> None:
        self.name: str = name
        self.filepath: str = filepath


class DirNode(Node):
    """Represents a specific directory node in the tree"""

    def __init__(self, name: str, filepath: str, parent: None | DirNode = None) -> None:
        super().__init__(name, filepath)
        self.children = []
        self.parent: None | DirNode = parent

    def add_child(self, node: DirNode | SourceCodeFileNode):
        self.children.append(node)

    def __repr__(self) -> str:
        children_repr = [child.__repr__() for child in self.children]
        children_repr_str = ", ".join(children_repr)
        return f"DirNode(name={self.name}, children={children_repr_str})"


class SourceCodeFileNode(Node):
    """Represents a specific source code file node in tree"""

    def __init__(self, name: str, filepath: str, parent: DirNode) -> None:
        super().__init__(name, filepath)
        self.parent: DirNode = parent

    def __repr__(self) -> str:
        return f"SourceCodeFileNode(name={self.name})"


class FileTree:
    """Represents the current files in a root directory"""

    def __init__(self, root_directory_filepath: str) -> None:
        self.root_directory: DirNode = DirNode(root_directory_filepath, root_directory_filepath)
        iter_ = os.walk(root_directory_filepath)
        path, directories, files = next(iter_)
        for dir_ in directories:
            self.root_directory.add_child(DirNode(dir_, os.path.join(path, dir_), self.root_directory))

        for f in files:
            if ".py" in f:
                self.root_directory.add_child(SourceCodeFileNode(f, os.path.join(path, f), self.root_directory))

        # Need to convert into recursive DFS to match os.walk
        path, directories, files = next(iter_)
        current_dir = None
        for child in self.root_directory.children:
            if child.filepath == path:
                current_dir: DirNode = child
                break

        assert current_dir, "Programming error logic"

        for dir_ in directories:
            current_dir.add_child(DirNode(dir_, os.path.join(path, dir_), self.root_directory))

        for f in files:
            if ".py" in f:
                current_dir.add_child(SourceCodeFileNode(f, os.path.join(path, f), self.root_directory))
        
        print(current_dir)