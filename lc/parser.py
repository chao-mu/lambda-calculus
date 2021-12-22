# Core
from collections import deque

# Internal
from lc.tokenizer import TokenType, tokenize
from lc.ast import Term, Variable, Abstraction, Application

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
        return self._term()

    def _term(self):
        enclosed = self._next_type == TokenType.OPEN_PAREN
        if enclosed:
            self._eat(TokenType.OPEN_PAREN, "(")

        spec = {
            TokenType.ID: self._variable,
            TokenType.LAMBDA: self._abstraction,
            TokenType.OPEN_PAREN: self._term,
        }

        terms = deque([])
        while self._next_type in spec:
           terms.append(spec[self._next_type]())

        if not terms:
            raise ParserError(f'Expecting term, but found "{self._look_ahead}',
                    self._look_ahead)

        if enclosed:
            self._eat(TokenType.CLOSE_PAREN, ")")

        if self._next_type in spec:
            terms.append(spec[self._next_type]())

        if len(terms) == 1:
            return terms[0]

        # Form applications
        app = Application(terms.popleft(), terms.popleft())
        while terms:
            app = Application(app, terms.popleft())

        return app

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

def parse(s):
    return Parser(s).parse()
