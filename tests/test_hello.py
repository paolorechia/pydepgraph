from py_dep_graph import hello


def test_hello():
    assert hello.world() == "!"
