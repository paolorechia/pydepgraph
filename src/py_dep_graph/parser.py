from typing import List


class ImportParser:
    def __init__(self, sourcecode):
        self.sourcecode = sourcecode
        self.word_buffer = []
        self.import_statements = []
        self.parsing_from = False
        self.current_from_statement = ""

        self.parsing_import = False
        self.parsing_next_parameter = False
        self.parsing_parenthesis_group = False 
        self.current_import_statement = ""


    def _push_parsed_word(self):
        self.current_import_statement = "".join(self.word_buffer)
        if self.current_from_statement:
            self.current_import_statement = f"{self.current_from_statement}.{self.current_import_statement}"
        self.import_statements.append(self.current_import_statement)
        self.word_buffer = []


    def parse(self) -> List[str]:
        """Parses the lines of a file, looking for import statements.

        This function implements a C like logic for handling string processing.
        It tries to be really low level, so it can be very flexible. 

        It could also be easily ported to C later if performance becomes a problem.
        """


        for char in self.sourcecode:
            # If not currently parsing an import statement, just apply logic until the next statement
            # is found
            if not self.parsing_import:
                if char == " ":
                    if self.parsing_from:
                        self.current_from_statement = "".join(self.word_buffer)
                        self.parsing_from = False

                    if "".join(self.word_buffer) == "import":
                        self.parsing_import = True
                    if "".join(self.word_buffer) == "from":
                        self.parsing_from = True
                    self.word_buffer = []
                else:
                    self.word_buffer.append(char)

            # Otherwise, try to find all applicable arguments
            else:
                # Case 0: arguments are delimited by parenthesis
                if char == "(":
                    self.parsing_parenthesis_group = True
                    continue

                elif self.parsing_parenthesis_group:
                    if char == ")":
                        self._push_parsed_word()
                        self.current_from_statement = ""
                        self.parsing_import = False
                        self.parsing_parenthesis_group = False
                        continue
                    
                    if char == " " or char == "\n" or char == "\t":
                        continue

                    if char == ',':
                        self._push_parsed_word()
                        continue

                # Case 1: single argument followed by \n
                elif char == "\n" and not self.parsing_next_parameter:
                    self._push_parsed_word()
                    self.parsing_import = False
                    self.current_from_statement = ""
                    continue

                # Case 2: multiple arguments defined by ,
                elif char == ",":
                    self.parsing_next_parameter = True
                    self._push_parsed_word()
                    continue
                elif self.parsing_next_parameter:
                    # Ignore breakline
                    if char == "\\":
                        continue

                    # Ignore whitespaces before filling the word buffer for next param
                    if len(self.word_buffer) == 0 and (char == " " or char == "\n"):
                        continue

                    # If found an additional argument, push it and keep parsing
                    if len(self.word_buffer) > 0:
                        if char == ",":
                            self._push_parsed_word()
                            continue

                        # If found a newline after filling word buffer, import statement is fully parsed
                        # wrap it up
                        if char == '\n' or char == " ":
                            self.parsing_next_parameter = False
                            self.parsing_import = False
                            self._push_parsed_word()
                            continue

                self.word_buffer.append(char)

        # Filter out empty strings to handle edge case of trailing comma in parenthesis group, e.g.,
        # (a,b,c,)
        return [imp for imp in self.import_statements if imp]


