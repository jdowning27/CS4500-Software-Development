import sys

def validate_int(arg):
    try:
        int(arg)
    except ValueError:
        print_error("usage: must be integer")

def validate_non_neg_int(*args):
        for arg in args:
            validate_int(arg)
            if arg < 0:
                print_error("usage: must be non negative int")

def validate_pos_int(*args):
    for arg in args:
        validate_int(arg)
        if arg <= 0:
            print_error("usage: must be positive int")

def is_even(num):
    return num % 2 == 0

def print_error(mess):
    print(mess)
    sys.exit(1)
