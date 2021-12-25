from dataclasses import dataclass

class Syntax: pass

class Term(Syntax):
    def reduce(self):
        return self

    def substitute(self, bindings=None):
        return self

@dataclass(frozen=True)
class Assignment(Syntax):
    name: str
    term: Term

    def friendly(self, aliases):
        if self in aliases:
            return aliases[self]

        term = self.term.friendly(aliases)

        return f"{name} := {term}"

@dataclass(frozen=True)
class Variable(Term):
    value: str

    def substitute(self, bindings=None):
        if bindings is not None and self.value in bindings:
            return bindings[self.value]

        return self

    def friendly(self, aliases):
        if self in aliases:
            return aliases[self]

        return self.value

@dataclass(frozen=True)
class Abstraction(Term):
    variable: Variable
    body: Term

    def reduce(self):
        return Abstraction(self.variable.reduce(), self.body.reduce())

    def substitute(self, bindings=None):
        return Abstraction(self.variable, self.body.substitute(bindings))

    def friendly(self, aliases):
        if self in aliases:
            return aliases[self]

        body = self.body.friendly(aliases)

        return f"(λ{self.variable.value}.{body})"

@dataclass(frozen=True)
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

    def friendly(self, aliases):
        if self in aliases:
            return aliases[self]

        left = self.left.friendly(aliases)
        right = self.right.friendly(aliases)

        return f"({left} {right})"
