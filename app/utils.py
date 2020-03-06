import ujson
import time


def read_js(filename):
    """
    Reads a specific type of JS file to JSON
    JS file - defines one variable to be interpreted as JSON

    :param filename: JS file name
    :return: JSON
    """
    with open(filename, 'r') as f:
        js_text = f.readlines()[0]  # JS should all be on a single line
        equal_sign_index = js_text.index('=')  # JSON text should be available after this index in a JS file
        js_text = js_text[equal_sign_index + 1:]  # + 1 for space
    return ujson.loads(js_text)


def save_data(data, filename, key):
    """
    :param data: A list of dicts - should contain what's already in file
    :param filename: Path of where to save file
    :return: None - saves to JS file
    """
    json_str = ujson.dumps({
            "data": data,
            "last_updated": time.time(),
        })

    with open(filename, 'w') as f:
        f.write(f'{key} = ' + json_str)


def get_object_by_id(list_of_dicts, _id):
    for dict in list_of_dicts:
        if dict['id'] == _id:
            return dict
