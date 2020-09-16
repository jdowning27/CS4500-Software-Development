#!/usr/local/bin/python
import sys
import json

def print_result(ordered_output):
    print({'count': len(ordered_output), 'seq': ordered_output})
    reversed_list = ordered_output.copy()
    reversed_list.reverse()
    reversed_list.insert(0, len(ordered_output))
    print(reversed_list)


def valid_json(str):
    """
    Is the given string a valid JSON Object?
    """ 
    try:
        json.loads(str)
        return True
    except ValueError:
        return False
    

def main():
    ordered_output = []
    maybe_json = ''
    for line in sys.stdin:
        if line.rstrip() == '/d':
            break
        else:
            # decode
            # ask about commas
            strip_line = line.strip()
            for char in strip_line:
                curr_json = maybe_json + char
                # if maybe_json is valid but curr_json is
                if valid_json(maybe_json) and not valid_json(curr_json):
                    ordered_output.append(json.loads(maybe_json))
                    maybe_json = char
                else:
                    maybe_json = curr_json
    ordered_output.append(json.loads(maybe_json))
            
    print_result(ordered_output)

main()
