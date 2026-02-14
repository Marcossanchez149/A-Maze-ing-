"""
parser.py
The file has functions to parse config.txt and convert values
"""


from typing import Union, Tuple, Dict


def convert_value(value: str) -> Union[int, bool, Tuple[int, int], str]:
    """
    Docstring for convert_value

    :param value: recive a string
    :return: a number, boolean, tuple of ints or a string
    """
    value = value.strip()

    if value.lower() == "true":
        return True

    elif value.lower() == "false":
        return False

    elif "," in value:
        try:
            return tuple(int(x.strip()) for x in value.split(","))
        except ValueError:
            pass

    try:
        return int(value)
    except ValueError:
        pass

    return value


def parse_config_file(path: str) -> Dict[str,
                                         Union[int, bool, Tuple[int, int], str]
                                         ]:
    """
    Read a key=value file and converts it to a dictionary
    with keys in lower and values as strings

    :param path: a file path
    :return: a dict with a key and a value number,
     boolean, tuple of ints or a string
    """
    config = {}

    try:
        with open(path, "r") as f:

            for line in f:

                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError(f"Invalid line: {line}")

                key, value = line.split("=", 1)
                config[key.strip().lower()] = convert_value(value)

        return config

    except FileNotFoundError:
        print(f"ERROR: file {path} not found.\n")
        return {}
