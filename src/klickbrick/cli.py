import argparse

import sys


# def hello_cmd(name=None):

#     if parsed_args.name:
#         "Hello %s" % parsed_args.name
#     else:
#         "Hello World"

def main(args=None):
    if not args:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("hello")
    parser.add_argument("--name", help="the name to say hello to")

    parsed_args = parser.parse_args(args)

    # hello_cmd(parsed_args)
    if parsed_args.name:
        # print("Hello %s" % parsed_args.name)
        # print(hello(parsed_args.name))
        pritn("Hello %s" % parsed_args.name)
    else:
        print("Hello World")
        # print(hello())

    # print("the square of {} equals {}".format(args.square, answer))
    # print(parsed_args)
