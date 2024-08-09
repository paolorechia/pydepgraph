from typing import List

def parse_imports(sourcecode: str) -> List[str]:
    """Parses the lines of a file, looking for import statements.

    This function implements a C like logic for handling string processing.
    It tries to be really low level, so it can be very flexible. 

    It could also be easily ported to C later if performance becomes a problem.
    """
    word_buffer = []
    import_statements = []
    parsing_import = False
    parsing_next_parameter = False
    parsing_parenthesis_group = False
 
    current_import_statement = ""
    for char in sourcecode:
        # If not currently parsing an import statement, just apply logic until the next statement
        # is found
        if not parsing_import:
            if char == " ":
                if "".join(word_buffer) == "import":
                    print("Found import statement")
                    parsing_import = True
                word_buffer = []
            else:
                word_buffer.append(char)

        # Otherwise, try to find all applicable arguments
        else:
            # Case 0: arguments are delimited by parenthesis
            if char == "(":
                parsing_parenthesis_group = True
                continue

            elif parsing_parenthesis_group:
                if char == ")":
                    current_import_statement = "".join(word_buffer)
                    import_statements.append(current_import_statement)
                    parsing_import = False
                    parsing_parenthesis_group = False
                    continue
                
                if char == " " or char == "\n" or char == "\t":
                    continue

                if char == ',':
                    current_import_statement = "".join(word_buffer)
                    import_statements.append(current_import_statement)
                    word_buffer = []
                    continue

            # Case 1: single argument followed by \n
            elif char == "\n" and not parsing_next_parameter:
                current_import_statement = "".join(word_buffer)
                parsing_import = False
                import_statements.append(current_import_statement)
                continue
            # Case 2: multiple arguments defined by ,
            elif char == ",":
                parsing_next_parameter = True
                current_import_statement = "".join(word_buffer)
                import_statements.append(current_import_statement)
                word_buffer = []
                continue
            elif parsing_next_parameter:
                # Ignore breakline
                if char == "\\":
                    continue

                # Ignore whitespaces before filling the word buffer for next param
                if len(word_buffer) == 0 and (char == " " or char == "\n"):
                    continue

                # If found an additional argument, push it and keep parsing
                if len(word_buffer) > 0:
                    if char == ",":
                        current_import_statement = "".join(word_buffer)
                        import_statements.append(current_import_statement)
                        word_buffer = []
                        continue

                    # If found a newline after filling word buffer, import statement is fully parsed
                    # wrap it up
                    if char == '\n' or char == " ":
                        parsing_next_parameter = False
                        parsing_import = False
                        current_import_statement = "".join(word_buffer)
                        import_statements.append(current_import_statement)
                        word_buffer = []
                        continue

            word_buffer.append(char)



    return import_statements


