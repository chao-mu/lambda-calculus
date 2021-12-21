from dataclasses import dataclass


# TODO alpha conversion and eta reduction

class Term: pass

@dataclass
class Variable(Term):
    value: str

    def reduce(self, bindings=None):
        if bindings is not None and self.value in bindings:
            return bindings[self.value]

        return self

@dataclass
class Abstraction(Term):
    variable: Variable
    body: Term

    def reduce(self, bindings=None):
        return self.body.reduce(bindings)

@dataclass
class Application(Term):
    left: Term
    right: Term

    def reduce(self, bindings=None):
        if bindings is None:
            bindings = {}

        left = self.left
        if isinstance(self.left, Application):
            left = self.left.reduce(bindings)

        right = self.right
        if isinstance(self.right, Application):
            right = self.right.reduce(bindings)

        if isinstance(self.left, Abstraction):
            var = self.left.variable.value
            bindings[var] = self.right

            return self.left.body.reduce(bindings)

        return Application(left, right)

def to_str(term: Term, _prepend: str="") -> str:
    if isinstance(term, Variable):
        return term.value

    if isinstance(term, Abstraction):
        body = to_str(term.body)
        return f"λ{term.variable}.{body}"

    if isinstance(term, Application):
        left = to_str(term.left)
        right = to_str(term.right)
        return f"({left} {right})"
