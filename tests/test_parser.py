from py_dep_graph.parser import parse_imports

def test_parser():
    import_statements = parse_imports("""
    import something

    import another
                                      
    import one, two, three


    import newone, \\
        newtwo, \\
        newthree
                                       
    import (pone, ptwo, pthree)
                                      
    import (
        pmlone,
        pmltwo,
        pmlthree
    )
""")
    print(import_statements)
    assert import_statements[0] == "something"
    assert import_statements[1] == "another"
    assert import_statements[2] == "one"
    assert import_statements[3] == "two"
    assert import_statements[4] == "three"
    assert import_statements[5] == "newone"
    assert import_statements[6] == "newtwo"
    assert import_statements[7] == "newthree"
    assert import_statements[8] == "pone"
    assert import_statements[9] == "ptwo"
    assert import_statements[10] == "pthree"
    assert import_statements[11] == "pmlone"
    assert import_statements[12] == "pmltwo"
    assert import_statements[13] == "pmlthree"