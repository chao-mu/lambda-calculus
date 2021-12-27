#!/usr/bin/env python3

# Internal
import lc

# Core
import readline
import importlib
import atexit
import os

def main():
    hist_path = os.path.join(
            os.path.expanduser("~"), ".lambda_cats_history")

    repl = REPL(hist_path, False)
    atexit.register(repl.save)

    repl.loop()

class REPL:

    def __init__(self, hist_path, verbose=False):
        self.hist_path = hist_path
        self.verbose = verbose
        self.rt = lc.Runtime()
        self.h_len = None

    def loop(self):
        try:
            readline.read_history_file(self.hist_path)
            self.h_len = readline.get_current_history_length()
        except FileNotFoundError:
            open(self.hist_path, 'wb').close()
            self.h_len = 0

        onwards = True
        while onwards:
            try:
                onwards = self._one_loop()
            except lc.ParserError as e:
                print(e)
            except (EOFError, KeyboardInterrupt):
                print("\nExiting meow!")
                onwards = False

    def _one_loop(self):
        user_input = input("🐱 ")
        if not user_input:
            return True

        if user_input == "/r":
            importlib.reload(lc)
            self.rt = lc.Runtime()
            return True

        root, reductions = self.rt.eval(user_input)
        if root is None:
            return True

        history = [root]
        if self.verbose:
            self.print_result(root)

        max_iter = 100
        reduced = None
        for reduced in reductions:
            if self.verbose:
                self.print_result(reduced)
            max_iter -= 1
            if max_iter <= 0:
                print("❗ Max number of reductions reached!")
                break

        if not self.verbose and reduced is not None:
            self.print_result(reduced)

        return True

    def print_result(self, result):
        aliases = {term: name for name, term in self.rt.aliases.items()}
        print("🐁 " + result.friendly(aliases))

        if self.verbose:
            print("🐁 " + str(result))

    def save(self):
        if self.h_len is None:
            return

        new_h_len = readline.get_current_history_length()
        readline.set_history_length(1000)
        readline.append_history_file(new_h_len - self.h_len, self.hist_path)

if __name__ == "__main__":
    main()
