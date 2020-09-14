#!/usr/local/bin/python
import sys;


def concat(words):
    """
    Concatenates the array of strings, separated by single blank space.
    Returns the concatenated string
    """
    phrase = ""
    for i in words:
        phrase = phrase + i + " "
    phrase = phrase.strip()
    return phrase

def printSTDOUT(phrase, limit=None):
    """
    Prints the given phrase the limited number of times. If no limit is supplied,
    print indefinitely.
    """
    if limit:
        for i in range(0, limit):
            print(phrase)
    else:
        while True:
            print(phrase)


def main(argv):
    """
    Handle command line arguments. Dispatch to helper functions accordingly to
    concatenate strings and print to console.
    """
    if len(argv) == 1:
        printSTDOUT("hello world")
    elif argv[1] == "-limit":
        if len(argv) == 2:
            # print hello world 20
            printSTDOUT("hello world", 20)
        else:
            # concat args and print 20 times
            printSTDOUT(concat(argv[2:]), 20)
    else:
        # concat args and print inf times
        printSTDOUT(concat(argv[1:]))
