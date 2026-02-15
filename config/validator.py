"""
validator.py
Contains functions to validate config file content
"""

from .types import ConfigDict
from .parser import parse_config_file


def validate_config(config: ConfigDict) -> ConfigDict:
    """
    Function that validates all params

    :param config: object that contains config params
    :return: validated config
    """
    pass
