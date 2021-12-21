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

        print("🐁 " + to_str(parsed))

        if debug:
            print("🐁 " + str(parsed))

        for reduced in reduce(parsed):
            print("🐟 " + to_str(reduced))
            if debug:
                print("🐟 " + str(reduced))

if __name__ == "__main__":
    main()
