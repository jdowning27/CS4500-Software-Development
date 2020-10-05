import sys

def validate_int(arg):
    try:
        int(arg)
    except ValueError:
        print("usage: must be integer")
        sys.exit(1)

def validate_non_neg_int(*args):
        for arg in args:
            validate_int(arg)
            if arg < 0:
                print("usage: must be non negative int")
                sys.exit(1)

def validate_pos_int(*args):
    for arg in args:
        validate_int(arg)
        if arg <= 0:
            print("usage: must be positive int")
            sys.exit(1)

def is_even(num):
    return num % 2 == 0

