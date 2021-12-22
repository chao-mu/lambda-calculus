from lc.parser import parse
from lc.ast import Abstraction, Variable, Application, Term

def test_to_tree():
    assert parse("x") == Variable("x")

    assert parse("λx.y") == Abstraction(Variable("x"), Variable("y"))

    assert parse("λa.b x") == parse("λa.(b x)")
    assert parse("λf.λx.f (f (f x))")

    assert parse("(λx.xx) (λx.xx)")

    # Assumes to_str is correct
    assert to_str(parse("M N S")) == "((M N) S)"
    assert to_str(parse("M (N S)")) == "(M (N S))"
    assert to_str(parse("(M N)")) == "(M N)"

    assert to_str(parse("λx.y M")) == "(λx (y M))"
    assert to_str(parse("(λx.y M) x")) == "((λx (y M)) x)"

def to_str(term: Term, _prepend: str="") -> str:
    if isinstance(term, Variable):
        return _prepend + term.value

    if isinstance(term, Abstraction):
        left = to_str(term.variable, _prepend="λ")
        right = to_str(term.body)

    if isinstance(term, Application):
        left = to_str(term.left)
        right = to_str(term.right)

    return f"({left} {right})"
