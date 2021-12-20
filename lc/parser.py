from lc.tokenizer import Token, Unknown, ParenOpen, ParenClose, Space, Lambda, Dot, Variable, tokenize

from collections import deque

from dataclasses import dataclass

from typing import Union

class ParserError(Exception):

    def __init__(self, reason, token):
        self.reason = reason
        self.token = token
        if token is not None:
            self.line_at = token.line_at
            self.char_at = token.char_at
            self.file_path = token.file_path

    def __str__(self):
        if self.token is None:
            return self.reason

        return f'Syntax eror at file "{self.file_path}", line {self.line_at} (character {self.char_at}):\n{self.reason}'

def next_token(tokens, last_tok, eof_err):
    try:
        tok = tokens.popleft()
    except IndexError:
        raise ParserError(eof_err, last_tok)

    return tok

def assert_class(tok, klass, expectation, invert=False):
    if isinstance(tok, klass) == invert:
        raise ParserError(f'Was expecting {expectation}, but found "{tok.content}"', tok)

class Node:
    def _indent(self, indent_level):
        return "  " * indent_level

@dataclass
class Leaf(Node):
    token: Token

    def debug(self, indent_level=0):
        indent = self._indent(indent_level)
        return f"{indent}{self.token.content}"

@dataclass
class Branch(Node):
    left: Node
    right: Node

    def debug(self, indent_level=0):
        indent = "  " * indent_level

        indent_level += 1
        left = self.left.debug(indent_level)
        right = self.right.debug(indent_level)

        return f"{indent}(\n{left}\n{right}\n{indent})"

def parse_str(s):
    return parse_tokens(deque(tokenize(s)))

def parse_tokens(tokens, paren_count=0):
    if not tokens:
        if paren_count > 0:
            raise ParserError("End of file reached before matching closed parenthsis.", tokens[-1])
        else:
            raise ParserError("End of file reached unexpectedly.")

    tok = tokens.popleft()

    if isinstance(tok, Space):
        return parse_tokens(tokens, paren_count)

    if isinstance(tok, Variable):
        return Leaf(tok)

    if isinstance(tok, Lambda):
        eof_err = "Unexpected end of file while defining abstraction"
        expect = lambda s: f"{s} while parsing abstraction"

        var_tok = next_token(tokens, tok, eof_err)
        assert_class(var_tok, Variable, expect("variable to bind"))

        dot_tok = next_token(tokens, var_tok, eof_err)
        assert_class(dot_tok, Dot, expect("expecting dot"))

        peek_tok = next_token(tokens, dot_tok, eof_err)
        assert_class(peek_tok, ParenClose, expect("a lambda term"), invert=True)

        tokens.appendleft(peek_tok)

        right = parse_tokens(tokens, paren_count)
        return Branch(Branch(Leaf(tok), Leaf(var_tok)), right)

    if isinstance(tok, ParenOpen):
        return parse_tokens(tokens, paren_count + 1)

    if isinstance(tok, ParenClose):
        return parse_tokens(tokens, paren_count - 1)

    raise ParserError(f'Unrecognize token found: "{tok.content}".', tok)
