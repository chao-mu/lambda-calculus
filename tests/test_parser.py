from lc.parser import parse_tokens, Leaf, Branch
from lc.tokenizer import tokenize, Variable, Lambda
import collections


def dq_tok(s):
    return collections.deque(tokenize(s))

def test_to_tree():
    assert parse_tokens(dq_tok("x")) == Leaf(Variable("x", 1))
    assert parse_tokens(dq_tok("λx.y")) == \
            Branch(Branch(Leaf(Lambda("λ", 1)), Leaf(Variable("x", 2))), Leaf(Variable("y", 4)))
