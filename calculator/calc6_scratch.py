from dataclasses import dataclass
from typing import *

EOF, ADD, SUB, MUL, DIV, INT, FLOAT, OP, L_PARENS, R_PARENS = 'EOF', 'ADD', 'SUB', 'MUL', 'DIV', 'INT', 'FLOAT', 'OP', '(', ')'

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
        while self.current_char != EOF:
            if self.current_char.isdigit():
                yield self.getINT()
            elif self.current_char == '(':
                self.advance()
                yield Token(L_PARENS, None)

            elif self.current_char == ')':
                self.advance()
                yield Token(R_PARENS, None)

            else:
                try:
                    yield self.getOP()
                except:
                    raise EOFERR
        
## Is also the parser
class Interpreter():

    def __init__(self, txt):
        self.tokenizer = Tokenizer(txt)
        self.tokens = list(self.tokenizer.tokenize())
        self.idx = 0
        self.curr_token = None
        self.get_next_token()


    def get_next_token(self) -> Token:
        self.idx += 1
        if self.idx > len(self.tokens):
            raise EOFERR()
        else:
            self.curr_token = self.tokens[self.idx - 1]


    def expre(self):
        """
        expr : term( ( ADD | SUB) term) *
        """

        result = self.term()
        try:
            while self.curr_token.value in ("add", "sub"):
                print("YEE")
                token = self.curr_token
                print("got expre: " + str(self.curr_token))
                if token.value == "add":
                    self.get_next_token()
                    print("DDDD")
                    result = result + self.term()
                    
                elif token.value == "sub":
                    self.get_next_token()
                    result = result - self.term()
        except EOFERR:
            pass
        
        return result

    def term(self):
        """
        term : factor( (MUL | DIV) factor) *
        """

        result = self.factor()
        print(self.curr_token)
        while self.curr_token.value in ("mul", "div"):
            token = self.curr_token
            print("got term: " + str(self.curr_token))
            if token.value == "mul":
                self.get_next_token()
                result = result * self.factor()

            elif token.value == "div":
                self.get_next_token()
                result = result / self.factor()
    
        return result

    def factor(self):
        """ 
        factor : INT  L_PARENS expr R_PARENS
        """
            
        token = self.curr_token
        if token.type == INT:
            self.get_next_token()
            print("got factor: " + str(token))
            return token.value
        elif token.type == L_PARENS:
            print("got factor: " + str(token))
            self.get_next_token()
            result = self.expre()
            print("got factor: " + str(self.curr_token))
            self.get_next_token()
            return result


inp = "12 add 9"
inter = Interpreter(inp)
print(inter.tokens)

print(inter.expre())