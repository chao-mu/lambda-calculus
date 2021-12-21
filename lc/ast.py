from dataclasses import dataclass

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


