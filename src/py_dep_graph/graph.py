from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_dep_graph.filetree import FileTree


class DependencyGraph:
    def __init__(self, file_tree) -> None:
        self.file_tree: FileTree = file_tree
