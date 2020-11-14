import json
def parser(input_stream):
    """
    Parse the given input string as JSON and creates a python representation
    String -> Python Object
    """
    ordered_output = []
    maybe_json = ''
    for line in input_stream:
        strip_input = line.strip()
        maybe_json = maybe_json + strip_input
    return json.loads(maybe_json)

def json_print(value):
    """
    takes any python object and prints it to STDOUT
    EFFECT: prints the json representation of the object to STDOUT
    Any -> void
    """
    print(json.dumps(value))