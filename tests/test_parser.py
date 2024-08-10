from py_dep_graph.parser import parse_imports

# ruff: noqa


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
                                      
    from this import that, andthat, andeventhat
                                      
    from country import justice, \\
        solidarity, \\
        freedom

    from job import (
        respect,
        money,
        andwhatelse
    )
                                      
    import (
        spmlone,
        spmltwo,
        spmlthree,
    )
                                      
    import doo.foo
                                      
    from nested.pkg import ultra
                                      
    from nested.another import (
        super,
        cool,
        stuff
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

    assert import_statements[14] == "this.that"
    assert import_statements[15] == "this.andthat"
    assert import_statements[16] == "this.andeventhat"

    assert import_statements[17] == "country.justice"
    assert import_statements[18] == "country.solidarity"
    assert import_statements[19] == "country.freedom"

    assert import_statements[20] == "job.respect"
    assert import_statements[21] == "job.money"
    assert import_statements[22] == "job.andwhatelse"

    assert import_statements[23] == "spmlone"
    assert import_statements[24] == "spmltwo"
    assert import_statements[25] == "spmlthree"

    assert import_statements[26] == "doo.foo"
    assert import_statements[27] == "nested.pkg.ultra"

    assert import_statements[28] == "nested.another.super"
    assert import_statements[29] == "nested.another.cool"
    assert import_statements[30] == "nested.another.stuff"
