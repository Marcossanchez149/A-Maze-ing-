"""
validator.py
Contains functions to validate config file content.
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
    """
    Validate that a config key contains a positive integer.

    Args:
        config (ConfigDict): The configuration dictionary.
        key (str): The key to validate in the config.

    Raises:
        ValueError: If the value is not an integer or is negative.
    """
    value = config[key]

    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{key.capitalize()} must be a positive integer")


def validate_bool(config: ConfigDict, key: str) -> None:
    """
    Validate that a config key contains a boolean value.

    Args:
        config (ConfigDict): The configuration dictionary.
        key (str): The key to validate in the config.

    Raises:
        ValueError: If the value is not a boolean.
    """
    value = config[key]

    if not isinstance(value, bool):
        raise ValueError(f"{key.capitalize()} must be a boolean")


def validate_tuples(config: ConfigDict, key: str) -> None:
    """
    Validate that a config key contains a tuple of two positive integers.

    Args:
        config (ConfigDict): The configuration dictionary.
        key (str): The key to validate in the config.

    Raises:
        ValueError: If the value is not a tuple of length 2,
        or any element is not a positive integer.
    """
    value = config[key]

    if not (isinstance(value, tuple) and len(value) == 2):
        raise ValueError(f"{key.capitalize()} must be a tuple of 2 integers")

    for elem in value:
        if not isinstance(elem, int) or elem < 0:
            raise ValueError(f"Elements of {key} must be positive integers")


def validate_str(config: ConfigDict, key: str, allowed: set[str]) -> None:
    """
    Validate that a config key contains a
    string within a set of allowed values.

    Args:
        config (ConfigDict): The configuration dictionary.
        key (str): The key to validate in the config.
        allowed (set[str]): A set of allowed string values for this key.

    Raises:
        ValueError: If the value is not a string or not in the allowed set.
    """
    value = config[key]

    if not isinstance(value, str):
        raise ValueError(f"{key.capitalize()} must be a string")

    if value not in allowed:
        raise ValueError(f"Invalid {key}: {value}. Allowed values: {allowed}")


def validate_file(config: ConfigDict, key: str) -> None:
    """
    Validate that a config key contains a string ending with '.txt'.

    Args:
        config (ConfigDict): The configuration dictionary.
        key (str): The key to validate in the config.

    Raises:
        ValueError: If the value is not a string or does not end with '.txt'.
    """
    value = config[key]

    if not isinstance(value, str):
        raise ValueError(f"{key.capitalize()} must be a string")

    if not value.endswith(".txt"):
        raise ValueError(f"{key.capitalize()} must end with .txt")


def validate_config(config: ConfigDict) -> ConfigDict:
    """
    Validate an entire configuration dictionary.

    This function checks for missing required keys and validates each
    configuration parameter according to its expected type and allowed values.

    Args:
        config (ConfigDict): The configuration dictionary to validate.

    Returns:
        ConfigDict: The validated configuration dictionary.

    Raises:
        ValueError: If any required key is missing or if any validation fails.
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
