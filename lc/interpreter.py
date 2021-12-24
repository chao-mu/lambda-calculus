from lc.ast import Term, Assignment
from lc.parser import parse

class Runtime:
    def __init__(self):
        self.assignments = {}

    def eval(self, s: str):
        root = parse(s)
        if isinstance(root, Assignment):
            self.assignments[root.name] = root.term
            return None, []

        return root, self.reduce(root)

    def reduce(self, term: Term):
        while True:
            last_term = term
            term = term.reduce(self.assignments)
            if last_term == term:
                break
            else:
                yield term
