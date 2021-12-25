from dataclasses import dataclass

class Syntax: pass

class Term(Syntax):
    def reduce(self):
        return self

    def substitute(self, bindings=None):
        return self

@dataclass
class Assignment(Syntax):
    name: str
    term: Term

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

    def reduce(self):
        return Abstraction(self.variable.reduce(), self.body.reduce())

    def substitute(self, bindings=None):
        return Abstraction(self.variable, self.body.substitute(bindings))

@dataclass
class Application(Term):
    left: Term
    right: Term

    def substitute(self, bindings=None):
        return Application(
                self.left.substitute(bindings), self.right.substitute(bindings))

    def reduce(self):
        left = self.left.reduce()
        right = self.right.reduce()

        if isinstance(left, Abstraction):
            var = left.variable.value
            bindings = {var: right}
            return left.body.substitute(bindings)

        return Application(left, right)

def to_str(syntax: Syntax, _prepend: str="") -> str:
    if isinstance(syntax, Variable):
        return syntax.value

    if isinstance(syntax, Abstraction):
        body = to_str(syntax.body)
        return f"(λ{syntax.variable.value}.{body})"

    if isinstance(syntax, Application):
        left = to_str(syntax.left)
        right = to_str(syntax.right)
        return f"({left} {right})"

    if isinstance(syntax, Assignment):
        term = to_str(syntax.term)
        return f"{syntax.name} := {term}"
