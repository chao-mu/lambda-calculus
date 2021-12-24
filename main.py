#!/usr/bin/env python3

# Internal
import lc

# Core
import readline
import importlib

def main():
    try:
        repl(True)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting meow!")

def repl(debug: bool) -> None:
    rt = lc.Runtime()
    while True:
        user_input = input("🐱 ")
        if not user_input:
            continue

        if user_input == "/r":
            importlib.reload(lc)
            rt = lc.Runtime()
            continue

        try:
            root, reductions = rt.eval(user_input)
        except lc.ParserError as e:
            print(e)
            continue

        if root is None:
            continue

        print_result(root, debug)

        max_iter = 100
        for reduced in reductions:
            print_result(reduced, debug)
            max_iter -= 1
            if max_iter <= 0:
                print("❗ Max number of reductions reached!")
                break

def print_result(result, debug):
    print("🐁 " + lc.to_str(result))

    if debug:
        print("🐁 " + str(result))

if __name__ == "__main__":
    main()
