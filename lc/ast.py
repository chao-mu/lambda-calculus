from dataclasses import dataclass

# TODO alpha conversion and eta reduction

class Term:
    def reduce(self, bindings=None):
        return self

@dataclass
class Variable(Term):
    value: str

    def substitute(self, bindings=None):
        if bindings is not None and self.value in bindings:
            return bindings[self.value]

        return self

@dataclass
class Abstraction(Term):
    variable: Variable
    body: Term

    def substitute(self, bindings=None):
        return Abstraction(self.variable, self.body.substitute(bindings))

@dataclass
class Application(Term):
    left: Term
    right: Term

    def substitute(self, bindings=None):
        return Application(
                self.left.substitute(bindings), self.right.substitute(bindings))

    def reduce(self, bindings=None):
        if bindings is None:
            bindings = {}

        left = self.left.reduce()
        right = self.right.reduce()

        if isinstance(left, Abstraction):
            var = left.variable.value
            bindings[var] = right

            return left.body.substitute(bindings)

        return Application(left, right)

def to_str(term: Term, _prepend: str="") -> str:
    if isinstance(term, Variable):
        return term.value

    if isinstance(term, Abstraction):
        body = to_str(term.body)
        return f"(λ{term.variable.value}.{body})"

    if isinstance(term, Application):
        left = to_str(term.left)
        right = to_str(term.right)
        return f"({left} {right})"
