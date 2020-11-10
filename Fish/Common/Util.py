import sys

def validate_int(arg):
    """
    Is the given argument an integer?
    If not, exit program and print message

    :arg: any    arg to check
    """
    try:
        int(arg)
    except ValueError:
        print_error("usage: must be integer")

def validate_non_neg_int(*args):
    """
    Are the given arguments an non-negative integers?
    If not, exit program and print message

    :args: array    array of args to check
    """
    for arg in args:
        validate_int(arg)
        if arg < 0:
            print_error("usage: must be non negative int")

def validate_pos_int(*args):
    """
    Are the given arguments an positive integers?
    If not, exit program and print message

    :args: array    array of args to check
    """
    for arg in args:
        validate_int(arg)
        if arg <= 0:
            print_error("usage: must be positive int")

def is_even(num):
    """
    Is the given number even?

    :num: int       Number to test
    """
    return num % 2 == 0

def print_error(mess):
    """
    Utility function to print a 'usage: ' message to user and 
    exit the system with error code 1

    :mess: string   Message to print to user
    """
    print(mess)
    sys.exit(1)
