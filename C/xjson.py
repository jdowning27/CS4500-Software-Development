#!/usr/local/bin/python
import sys
import json

def print_result(ordered_output):
    """
    Print the JSON object results
    """

    print(json.dumps({'count': len(ordered_output), 'seq': ordered_output}))

    reversed_list = ordered_output.copy()
    reversed_list.reverse()
    reversed_list.insert(0, len(ordered_output))
    print(json.dumps(reversed_list))


def valid_json(str):
    """
    Is the given string a valid JSON Object?
    """ 
    try:
        json.loads(str)
        return True
    except ValueError:
        return False
'''
def is_number(curr_json):
    length = len(curr_json)
    if curr_json[length - 1] is in ['E', 'e', '+', '-', '.', '/']:
        if curr_json[length - 2] != ' ':
            return True
    '''

def main():
    ordered_output = []
    maybe_json = ''
    for line in sys.stdin:

        if line.rstrip() == '/d':
            break
        else:
            strip_line = line.strip()
            for char in strip_line:
                curr_json = maybe_json + char
                # if maybe_json is valid but curr_json is
                if valid_json(maybe_json) and not valid_json(curr_json):
                    if char in ['E', 'e', '+', '-', '.', '/'] and maybe_json[len(maybe_json) - 1] is not ' ':
                        maybe_json = curr_json
                    else:
                        ordered_output.append(json.loads(maybe_json))
                        maybe_json = char
                else:
                    maybe_json = curr_json
            if valid_json(maybe_json):
                ordered_output.append(json.loads(maybe_json))
                maybe_json = ''
                
            # otherwise we should check if maybe_json is valid json and add
            
    print_result(ordered_output)

main()
