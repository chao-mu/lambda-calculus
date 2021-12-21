from collections import deque

from dataclasses import dataclass

from typing import Union

from enum import Enum, auto

from lc.tokenizer import TokenType, tokenize

"""
T -> V | AP | AB
AB -> λ V . T
AP -> (T T) | (T)T
V -> [a-z]
"""

class Term: pass

@dataclass
class Variable(Term):
    value: str

@dataclass
class Abstraction(Term):
    variable: Variable
    body: Term

@dataclass
class Application(Term):
    left: Term
    right: Term

class Parser:

    def __init__(self, program: str):
        self._tokens = deque(tokenize(program))
        if not self._tokens:
            raise ParserError("Program is empty")

        self._look_ahead = self._tokens.popleft()
        self._last_tok = None

    @property
    def _next_type(self):
        if not self._look_ahead:
            return None

        return self._look_ahead.tt

    def parse(self):
        return self._program()

    def _program(self):
        left = self._term()
        if self._look_ahead is None:
            return left

        return self._application(left)

    def _application(self, left=None):
        enclosed = self._next_type == TokenType.OPEN_PAREN
        if enclosed:
            self._eat(TokenType.OPEN_PAREN, "(")

        if left is None:
            left = self._term()

        right = self._term()

        app = Application(left, right)

        if self._next_type != TokenType.CLOSE_PAREN and self._tokens:
            app = self._application(app)

        if enclosed:
            self._eat(TokenType.CLOSE_PAREN, ")")

        return app

    def _term(self):
        spec = {
            TokenType.ID: self._variable,
            TokenType.LAMBDA: self._abstraction,
            TokenType.OPEN_PAREN: self._application,
        }

        head = self._look_ahead
        if head.tt not in spec:
            raise ParserError(f'Was expecting a term, but found "{head.content}"', head)
        return spec[head.tt]()

    def _abstraction(self):
        self._eat(TokenType.LAMBDA, "lambda")
        var = self._variable()
        self._eat(TokenType.DOT, "dot while_defining abstraction")

        return Abstraction(var, self._term())

    def _variable(self):
        tok = self._eat(TokenType.ID, "variable")
        return Variable(tok.content)

    def _eat(self, tt: TokenType, expectation: str):
        if not self._look_ahead:
            raise ParserError(f"Unexpected end of file reached.", self._last_tok)

        tok = self._look_ahead
        self._last_tok = tok

        if tok.tt != tt:
            raise ParserError(f'Was expecting {expectation}, but found "{tok.content}"', tok)

        self._look_ahead = None
        if self._tokens:
            self._look_ahead = self._tokens.popleft()

        return tok

class ParserError(Exception):

    def __init__(self, reason, token=None):
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

def to_str(node, prepend=""):
    if isinstance(node, Variable):
        return prepend + node.value

    if isinstance(node, Abstraction):
        left = to_str(node.variable, prepend="λ")
        right = to_str(node.body)

    if isinstance(node, Application):
        left = to_str(node.left)
        right = to_str(node.right)

    return f"({left} {right})"

def parse(s):
    return Parser(s).parse()
