""" """

from dataclasses import dataclass
from typing import *

EOF, ADD, SUB, MUL, DIV, INT, FLOAT = 'EOF', 'ADD', 'SUB', 'MUL', 'DIV', 'INT', 'FLOAT'

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


g_idx = 0
current_char = ""
def tokenizer() -> Iterable[Token]:
    """ """
    def get_char() -> str:
        global txt
        global g_idx
        global current_char

        if g_idx >= len(txt):
            current_char = EOF
            return

        if txt[g_idx].isspace():
            g_idx += 1
            get_char()
        else:
            current_char = txt[g_idx]
            g_idx += 1

    def getInt():
        global current_char
        tok = ""
        while current_char.isdigit():
            tok += current_char
            get_char()

        return Token(INT, int(tok))

    def getOP():
        global current_char

        tok = ""
        while tok + current_char in "add":
            if current_char == EOF:
                break
            
            tok += current_char
            get_char()

        return Token(ADD, tok)

    toks = []

    if len(txt) % 2 == 0:
        return toks

    get_char()
    toks.append(getInt())
    while current_char != EOF:
        toks.append(getOP())
        toks.append(getInt())

    return toks

def parser(tokens: List[Token]):
    """ """
    left = tokens[0]
    out = [left]

    for i in range(1, len(tokens) - 1):
        op = tokens[i]
        right = tokens[i+1]
        out.append([op, right])

    return out

def interpreter(tree):

    result = 0
    left = tree[0]
    for op, right in tree[1:]:
        result += OPERATOR_MAP[op.type](left.value, right.value)
        left = Token(INT, result)
    return result

txt = "12 add 11"
toks = list(tokenizer())
tree = parser(toks)
print(interpreter(tree))