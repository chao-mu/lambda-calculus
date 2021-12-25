from lc.ast import Term, Variable, Abstraction, Application
from lc.interpreter import Runtime



def test_reduce():
    rt = Runtime()
    def r(root):
        return rt.reduce_times(root, 100)

    x = Variable("x")
    y = Variable("y")
    a = Variable("a")
    b = Variable("b")

    assert x.reduce() == x

    identity = Abstraction(x, x)
    assert r(identity) == identity
    assert r(Application(identity, x)) == x
    assert r(Application(identity, y)) == y
    assert r(Application(identity, identity)) == identity

    # λx.λy.x
    true = Abstraction(x, Abstraction(y, x))
    # (((λx.λy.x) a) b)
    # ((λy.a) b)
    # a
    assert r(Application(Application(true, a), b)) == a
    assert r(Application(Application(true, b), a)) == b

    # λx.λy.y
    false = Abstraction(x, Abstraction(y, y))
    assert r(Application(Application(false, a), b)) == b
    assert r(Application(Application(false, b), a)) == a

    # ((λx. x x) (λx. x x))
    omega_side = Abstraction(x, Application(x, x))
    omega = Application(omega_side, omega_side)
    assert r(omega) == omega

    succ = Abstraction(Variable(value='n'), Abstraction( Variable('f'), Abstraction( Variable('x'), Application( Variable('f'), Application( Application( Variable('n'), Variable('f')), Variable('x'))))))
    zero = Abstraction(Variable('f'), Abstraction(Variable('x'), Variable(value='x')))
    one = Abstraction(Variable('f'), Abstraction(Variable('x'), Application(Variable(value='f'), Variable('x'))))
    two = Abstraction(Variable(value='f'), Abstraction(Variable('x'), Application(Variable('f'), Application(Variable('f'), Variable('x')))))

    assert r(Application(succ, zero)) == one
    assert r(Application(succ, one)) == two
    assert r(Application(succ, Application(succ, zero))) == two
