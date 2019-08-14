"""
General utils
"""


def strigify_dict(my_dict):
    returned_string = ""
    for key, value in my_dict.items():
        returned_string += " - " + ", ".join(value)
    return returned_string
