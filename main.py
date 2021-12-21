#!/usr/bin/env python3

# Internal
from lc.parser import parse, to_str, ParserError

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
            print("🐁 " + to_str(parse(user_input)))
            print("🐁 " + str(parse(user_input)))
        except ParserError as e:
            print(e)

if __name__ == "__main__":
    main()
