from lc.ast import Term, Variable, Abstraction, Application
from lc.parser import parse

def test_reduce():
    x = Variable("x")
    y = Variable("y")

    assert x.reduce() == x

    identity = Abstraction(x, x)
    assert Application(identity, x).reduce() == x
    assert Application(identity, identity).reduce() == identity

    # λx.λy.x
    true = Abstraction(x, Abstraction(y, x))
    assert Application(Application(true, x), y).reduce() == x
    assert Application(Application(true, y), x).reduce() == y

    # λx.λy.y
    false = Abstraction(x, Abstraction(y, y))
    assert Application(Application(false, x), y).reduce() == y
    assert Application(Application(false, y), x).reduce() == x
