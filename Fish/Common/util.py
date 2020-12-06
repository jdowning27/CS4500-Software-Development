from queue import Queue
import sys
from threading import Thread


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


def get_max_penguin_count(player_count):
    """
    gets the max number of penguins a player can have in a game with player_count players
    Integer -> Integer
    """
    return 6 - player_count


def is_posn(obj):
    """
    Test if an object is a Posn (a length 2 list or tuple of ints).

    Object -> Boolean
    """
    return (len(obj) == 2 and
            isinstance(obj[0], int) and
            isinstance(obj[1], int))


def is_json_action(obj):
    """
    Test if an object is a json representation of an Action
    (False or a list of two Posns).

    Object -> Boolean
    """
    return (obj is False or
            (len(obj) == 2 and
             is_posn(obj[0]) and
             is_posn(obj[1])))


def safe_call(timeout, func, args=[]):
    """
    Used to make safe calls to code. It will call the given
    function with the given arguments and catch any exceptions.

    If the function takes longer than timeout or raises an
    exception then this function will return False.

    Natural, [X ... -> Y], X ... -> [Maybe Y]
    """

    def thread_call(func, args, queue):
        """Helper to put threaded function return value in a queue.

        Puts None in the queue if an exception occurs.

        func:   The function to run.
        args:   An iterable of function arguments.
        queue:  The queue to put the result in.
        """
        try:
            queue.put(func(*args))
        except Exception as exc:
            print(exc)
            queue.put(False)

    queue = Queue()
    thread = Thread(target=thread_call, args=[func, args, queue], daemon=True)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print("timeout")
        return False

    return queue.get()
