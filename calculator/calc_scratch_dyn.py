""" """

from dataclasses import dataclass
from typing import *

EOF, ADD, SUB, MUL, DIV, INT, FLOAT, OP = 'EOF', 'ADD', 'SUB', 'MUL', 'DIV', 'INT', 'FLOAT', 'OP'

OPERATOR_MAP = {
    ADD: lambda a,b: a + b,
    SUB: lambda a,b: a - b,
    MUL: lambda a,b: a * b,
    DIV: lambda a,b: a / b
}

TYPEERR = Exception("TYPEERR")

class EOFERR(BaseException):
    pass


@dataclass
class Token:
    type: Any
    value: Any

class Tokenizer():

    def advance(self) -> None:
        """ Advance input string pointer,
            Skips whitespaces
        """

        self.pos += 1
        if self.pos >= len(self.txt):
            self.current_char = EOF
        else:
            self.current_char = self.txt[self.pos]
            if self.current_char.isspace():
                self.advance()


    def getType(self, type, check: callable, constructer: callable) -> Token:
        """ Abstract Method for Lexical Analysis Token Creation """

        tok = ""
        while(check(tok + self.current_char) == True):
            tok += self.current_char
            self.advance()

        return Token(type, constructer(tok))

    
    def __init__(self, txt):
        self.txt = txt
        self.pos = -1
        self.current_char = None
        self.advance()

        # Overloading
        self.getOP = lambda: self.getType(
            OP,
            lambda tok: any([tok in "add"]),
            lambda tok: tok
        )

        self.getINT = lambda: self.getType(
            INT,
            lambda tok: tok.isdigit(),
            lambda tok: int(tok)
        ) 


    def tokenize(self) -> Iterable[Token]:
        yield self.getINT()
        while self.current_char != EOF:
            yield self.getOP()
            yield self.getINT()
            


my_string = "12 add 526"
tokenizer = Tokenizer(my_string)
for token in tokenizer.tokenize():
    print(token)

