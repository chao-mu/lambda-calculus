#!/usr/bin/env python3

# Internal
from lc.parser import parse, ParserError
from lc.interpreter import reduce
from lc.ast import to_str

# Core
import readline

def main():
    try:
        repl(True)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting meow!")

def repl(debug: bool) -> None:
    while True:
        user_input = input("🐱 ")
        if not user_input:
            continue

        try:
            parsed = parse(user_input)
        except ParserError as e:
            print(e)
            continue

        print_result(parsed, debug)

        max_iter = 100
        for reduced in reduce(parsed):
            print_result(parsed, debug)
            max_iter -= 1
            if max_iter <= 0:
                print("❗ Max number of reductions reached!")
                break


def print_result(result, debug):
    print("🐁 " + to_str(result))

    if debug:
        print("🐁 " + str(result))

if __name__ == "__main__":
    main()
