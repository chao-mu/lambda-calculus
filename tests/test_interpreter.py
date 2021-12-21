from lc.ast import Term, Variable, Abstraction, Application
from lc.parser import parse

def test_reduce():
    x = Variable("x")
    y = Variable("y")
    a = Variable("a")
    b = Variable("b")

    assert x.reduce() == x

    identity = Abstraction(x, x)
    assert identity.reduce() == identity
    assert Application(identity, x).reduce() == x
    assert Application(identity, identity).reduce() == identity

    # λx.λy.x
    true = Abstraction(x, Abstraction(y, x))
    # (((λx.λy.x) 1) 2)
    # ((λy.1) 2)
    # 1
    assert Application(Application(true, a), b).reduce() == a
    assert Application(Application(true, b), a).reduce() == b

    false = Abstraction(x, Abstraction(y, y))
    # λx.λy.y
    assert Application(Application(false, a), b).reduce() == b
    assert Application(Application(false, b), a).reduce() == a
