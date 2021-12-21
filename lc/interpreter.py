from lc.ast import Term, Variable, Abstraction, Application

def reduce(term):
    last_term = None
    while last_term != term:
        last_term = term
        term = term.reduce()
        yield term
