from lc.ast import Term, Variable, Abstraction, Application

def reduce(term):
    while True:
        last_term = term
        term = term.reduce()
        if last_term == term:
            break
        else:
            yield term
