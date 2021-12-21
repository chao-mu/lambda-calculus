#!/usr/bin/env python3

# Internal
from lc.parser import parse, ParserError
from lc.ast import to_str

# Core
import readline

def main():
    try:
        repl()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting meow!")

def repl() -> None:
    while True:
        user_input = input("🐱 ")
        if not user_input:
            continue
        try:
            parsed = parse(user_input)
        except ParserError as e:
            print(e)

        print("🐁 " + str(parsed))
        print("🐁 " + to_str(parsed))
        reduced = parsed.reduce()
        if reduced != parsed:
            print("🐟 " + str(reduced))
            print("🐟 " + to_str(reduced))

if __name__ == "__main__":
    main()
