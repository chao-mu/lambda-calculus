from dataclasses import dataclass
import re

MEMORY_FILE_PATH="<memory>"

@dataclass
class Token:
    content: str
    char_at: int
    line_at: int = 1
    file_path: str = MEMORY_FILE_PATH

class Unknown(Token): pass
class ParenOpen(Token): pass
class ParenClose(Token): pass
class Space(Token): pass
class Lambda(Token): pass
class Dot(Token): pass
class Variable(Token): pass

def tokenize(s, file_path=MEMORY_FILE_PATH):
    tokens = []
    line_at = 1
    char_at = 1
    for t in re.split(r"([^A-Za-z_])", s):
        if not t:
            continue

        if t == "\n":
            line_at += 1
            char_at = 1
            continue

        klass = Unknown
        if t == "(":
            klass = ParenOpen
        elif t == ")":
            klass = ParenClose
        elif t == " ":
            klass = Space
        elif t == "λ":
            klass = Lambda
        elif t == ".":
            klass = Dot
        elif t.isalnum():
            klass = Variable

        tokens.append(klass(t, char_at, line_at, file_path))
        char_at += len(t)

    return tokens
