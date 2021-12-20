from lc.tokenizer import *

def test_tokenize():
    # Variable
    assert tokenize("x") == [Variable("x", 1)]
    assert tokenize("(") == [ParenOpen("(", 1)]
    assert tokenize(")") == [ParenClose(")", 1)]
    assert tokenize(" ") == [Space(" ", 1)]
    assert tokenize("λ") == [Lambda("λ", 1)]
    assert tokenize(".") == [Dot(".", 1)]
    assert tokenize("|") == [Unknown("|", 1)]

    assert len(tokenize("(λx.M)")) > 1

    # Abstraction
    assert tokenize("(λx.M)") == [
        ParenOpen("(", 1),
        Lambda("λ", 2),
        Variable("x", 3),
        Dot(".", 4),
        Variable("M", 5),
        ParenClose(")", 6),
    ]

    # Application
    assert tokenize("(M N)") == [
        ParenOpen("(", 1),
        Variable("M", 2),
        Space(" ", 3),
        Variable("N", 4),
        ParenClose(")", 5),
    ]
