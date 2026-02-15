"""
validator.py
Contains functions to validate config file content
"""

from .types import ConfigDict
from .constants import (
    REQUIRED_KEYS,
    POSITIVE_INT,
    BOOL,
    TUPLES,
    ALGORITHMS,
    DISPLAYS,
)


def validate_positive_int(config: ConfigDict, key: str) -> None:
    value = config[key]

    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{key.capitalize()} must be a positive integer")


def validate_bool(config: ConfigDict, key: str) -> None:
    value = config[key]

    if not isinstance(value, bool):
        raise ValueError(f"{key.capitalize()} must be a boolean")


def validate_tuples(config: ConfigDict, key: str) -> None:
    value = config[key]

    if not (isinstance(value, tuple) and len(value) == 2):
        raise ValueError(f"{key.capitalize()} must be a tuple of 2 integers")

    for elem in value:
        if not isinstance(elem, int) or elem < 0:
            raise ValueError(f"Elements of {key} must be positive integers")


def validate_str(config: ConfigDict, key: str, allowed: set[str]) -> None:
    value = config[key]

    if not isinstance(value, str):
        raise ValueError(f"{key.capitalize()} must be a string")

    if value not in allowed:
        raise ValueError(f"Invalid {key}: {value}. Allowed values: {allowed}")


def validate_file(config: ConfigDict, key: str) -> None:
    value = config[key]

    if not isinstance(value, str):
        raise ValueError(f"{key.capitalize()} must be a string")

    if not value.endswith(".txt"):
        raise ValueError(f"{key.capitalize()} must end with .txt")


def validate_config(config: ConfigDict) -> ConfigDict:
    """
    Function that validates all params

    :param config: object that contains config params
    :return: validated config
    """
    missing_keys = REQUIRED_KEYS - set(config.keys())
    if missing_keys:
        raise ValueError(f"Missing config keys:{missing_keys}")

    for key in POSITIVE_INT:
        validate_positive_int(config, key)

    for key in BOOL:
        validate_bool(config, key)

    for key in TUPLES:
        validate_tuples(config, key)

    validate_str(config, "algorithm", ALGORITHMS)
    validate_str(config, "display", DISPLAYS)

    validate_file(config, "output_file")

    return config
