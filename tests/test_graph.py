from __future__ import annotations

from py_dep_graph.filetree import FileTree
from py_dep_graph.graph import DependencyGraph


def test_dependency_graph(tmp_dir):
    dep_graph = DependencyGraph(FileTree(tmp_dir))
    assert dep_graph.nodes[0].source_code_node.name == "mod5"
    assert dep_graph.nodes[0].links[0]["name"] == "mod4"
