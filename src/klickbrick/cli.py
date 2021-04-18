import argparse

import sys


def main(args=None):
    if not args:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("hello")
    parser.add_argument("--name", help="the name to say hello with")

    parsed_args = parser.parse_args(args)

    if parsed_args.name:
        print("Hello %s" % parsed_args.name)
    else:
        print("Hello World")
