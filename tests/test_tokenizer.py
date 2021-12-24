from lc.tokenizer import Token, TokenType, tokenize

def test_tokenize():
    # Variable
    assert tokenize("x") == [Token(TokenType.ID, "x", 1)]
    assert tokenize("(") == [Token(TokenType.OPEN_PAREN, "(", 1)]
    assert tokenize(")") == [Token(TokenType.CLOSE_PAREN, ")", 1)]
    assert tokenize(" ") == []
    assert tokenize("λ") == [Token(TokenType.LAMBDA, "λ", 1)]
    assert tokenize(".") == [Token(TokenType.DOT, ".", 1)]
    assert tokenize("|") == [Token(TokenType.UNKNOWN, "|", 1)]
    assert tokenize(":=") == [Token(TokenType.ASSIGN, ":=", 1)]

    assert len(tokenize("(λx.M)")) > 1

    # Abstraction
    assert tokenize("(λx.M)") == [
        Token(TokenType.OPEN_PAREN, "(", 1),
        Token(TokenType.LAMBDA, "λ", 2),
        Token(TokenType.ID, "x", 3),
        Token(TokenType.DOT, ".", 4),
        Token(TokenType.ID, "M", 5),
        Token(TokenType.CLOSE_PAREN, ")", 6),
    ]

    # Application
    assert tokenize("(M N)") == [
        Token(TokenType.OPEN_PAREN, "(", 1),
        Token(TokenType.ID, "M", 2),
        Token(TokenType.ID, "N", 4),
        Token(TokenType.CLOSE_PAREN, ")", 5),
    ]

    # Assignment
    assert tokenize("N := (λx.M)") == [
        Token(TokenType.ID, "N", 1),
        Token(TokenType.ASSIGN, ":=", 3),
        Token(TokenType.OPEN_PAREN, "(", 6),
        Token(TokenType.LAMBDA, "λ", 7),
        Token(TokenType.ID, "x", 8),
        Token(TokenType.DOT, ".", 9),
        Token(TokenType.ID, "M", 10),
        Token(TokenType.CLOSE_PAREN, ")", 11),
    ]
