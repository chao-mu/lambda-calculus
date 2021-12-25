from lc.ast import Term, Assignment
from lc.parser import parse

class Runtime:
    def __init__(self):
        self.aliases = {}

    def eval(self, s: str):
        root = parse(s)
        if isinstance(root, Assignment):
            self.aliases[root.name] = root.term
            return None, []

        return root, self.reduce(root)

    def reduce_times(self, term: Term, max_iter: int):
        for term in self.reduce(term):
            max_iter -= 1
            if max_iter <= 0:
                break

        return term

    def reduce(self, term: Term):
        while True:
            last_term = term
            term = term.substitute(self.aliases)
            term = term.reduce()
            if last_term == term:
                break
            else:
                yield term
