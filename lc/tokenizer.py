from dataclasses import dataclass
import re
from enum import Enum, auto

MEMORY_FILE_PATH="<memory>"

class TokenType(Enum):
    ID = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    SPACE = auto()
    DOT = auto()
    LAMBDA = auto()
    UNKNOWN = auto()

TokenSpec = [
    (lambda s: s.isalpha(), TokenType.ID),
    (lambda s: s == "(", TokenType.OPEN_PAREN),
    (lambda s: s == ")", TokenType.CLOSE_PAREN),
#    (lambda s: s == " ", TokenType.SPACE),
    (lambda s: s == " ", None),
    (lambda s: s == ".", TokenType.DOT),
    (lambda s: s == "λ" , TokenType.LAMBDA),
]

@dataclass
class Token:
    tt: TokenType
    content: str
    char_at: int
    line_at: int = 1
    file_path: str = MEMORY_FILE_PATH

def tokenize(s, file_path=MEMORY_FILE_PATH):
    tokens = []
    line_at = 1
    char_at = 1
    for raw_token in re.split(r"([^A-Za-z_])", s):
        if not raw_token:
            continue

        if raw_token == "\n":
            line_at += 1
            char_at = 1
            continue

        token_type = TokenType.UNKNOWN
        for p, candidate_type in TokenSpec:
            if p(raw_token):
                token_type = candidate_type

        if token_type is not None:
            tokens.append(Token(token_type, raw_token, char_at, line_at, file_path))

        char_at += len(raw_token)

    return tokens
