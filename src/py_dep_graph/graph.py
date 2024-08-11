from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_dep_graph.filetree import FileTree, SourceCodeFileNode

from py_dep_graph.filetree import walk_source_code_tree


class DependencyNode:
    def __init__(self, source_code_node: SourceCodeFileNode) -> None:
        self.source_code_node = source_code_node
        self.links = []
        self.external_dependencies = []

    def find_links_in_file_tree(self, file_tree: FileTree):
        self.find_global_imports(file_tree)

    def find_global_imports(self, file_tree: FileTree):
        dtree = file_tree.as_dict()[file_tree.root_directory.name]
        for import_stm in self.source_code_node.imports:
            node = dtree
            blocks = import_stm.split(".")
            found_module_in_tree = False
            block_name = ""
            for block in blocks[:-1]:
                try:
                    node = node["children"][block]
                    block_name = block
                except KeyError:
                    pass

            # If second last block is of type source code file code,
            # then last block must be an internal code construct (function, class etc)
            # and we can safely ignore it.

            if node["type"] == "source_code_file":
                found_module_in_tree = True

            # otherwise, we need to do the last import
            else:
                try:
                    block_name = blocks[-1]
                    node = node["children"][blocks[-1]]
                    found_module_in_tree = True
                except (KeyError, IndexError):
                    pass

            if found_module_in_tree:
                self.links.append({**node, "name": block_name})
            else:
                self.external_dependencies.append(import_stm)


class DependencyGraph:
    """Uses an adjacency list style for representing the graph."""

    def __init__(self, file_tree) -> None:
        self.file_tree: FileTree = file_tree
        self.nodes: list[DependencyNode] = [
            DependencyNode(node) for node in walk_source_code_tree(file_tree.root_directory)
        ]

        for node in self.nodes:
            node.find_links_in_file_tree(self.file_tree)
