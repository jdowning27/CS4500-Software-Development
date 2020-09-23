#!/usr/bin/env python
import sys
import json
import io

def print_result(ordered_output):
    """
    Print the JSON object results
    """
    count = {'count': len(ordered_output), 'seq': ordered_output}
  
    reversed_list = ordered_output[:]
    reversed_list.reverse()
    reversed_list.insert(0, len(ordered_output))

    output_string = "{}\n{}\n".format(json.dumps(count) , json.dumps(reversed_list))
    return bytes(output_string, 'utf-8')


def valid_json(str):
    """
    Is the given string a valid JSON Object?
    """ 
    try:
        json.loads(str)
        return True
    except ValueError:
        return False

def parser(input_stream):

    ordered_output = []
    maybe_json = ''

    strip_input = input_stream.strip()
    for char in strip_input:
        curr_json = maybe_json + char
        # if maybe_json is valid but curr_json is
        if valid_json(maybe_json) and not valid_json(curr_json):
            if char in ['E', 'e', '+', '-', '.', '/'] and maybe_json[len(maybe_json) - 1] != ' ':
                maybe_json = curr_json
            else:
                ordered_output.append(json.loads(maybe_json))
                maybe_json = char
        else:
            maybe_json = curr_json
    if valid_json(maybe_json):
        ordered_output.append(json.loads(maybe_json))
        maybe_json = ''
    
    return print_result(ordered_output)
