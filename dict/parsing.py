# dict/parsing.py

import argparse


def parsing() -> str:
    parser = argparse.ArgumentParser(description="Dict From Weblio API")
    parser.add_argument("words", nargs="*", help="words you want to know")
    args = parser.parse_args()

    if len(args.words) == 0:
        parser.print_usage()
        raise SystemExit(1)

    return " ".join(args.words)
