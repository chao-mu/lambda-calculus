from lc.parser import parse, to_str, Abstraction, Variable, Application
#from lc.tokenizer import tokenize, Variable, Lambda
#import collections

def test_to_tree():
    assert parse("x") == Variable("x")

    assert parse("λx.y") == Abstraction(Variable("x"), Variable("y"))

    assert parse("λa.b x") == parse("λa.(b x)")
    assert parse("λf.λx.f (f (f x))")

    assert parse("(λx.xx) (λx.xx)")

    assert to_str(parse("M N S")) == "((M N) S)"
    assert to_str(parse("M (N S)")) == "(M (N S))"
    assert to_str(parse("(M N)")) == "(M N)"
#    assert parse_tokens(dq_tok("x")) == Leaf(Variable("x", 1))
#    assert parse_tokens(dq_tok("λx.y")) == \
            #Branch(Branch(Leaf(Lambda("λ", 1)), Leaf(Variable("x", 2))), Leaf(Variable("y", 4)))
