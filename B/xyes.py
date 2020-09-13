#!/usr/local/bin/python
import sys;


def concat(words):
    phrase = ""
    for i in words:
        phrase = phrase + i + " "
    phrase = phrase.strip()
    return phrase

def printSTDOUT(phrase, limit=None):
    if limit:
        for i in range(0, limit):
            print(phrase)
    else:
        while True:
            print(phrase)


def main(argv):
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



#main(sys.argv)
