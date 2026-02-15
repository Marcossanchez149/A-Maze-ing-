"""
Package manager
"""


__version__ = "1.0.0"

from .parser import parse_config_file
from .validator import validate_config

__all__ = ["parse_config_file", "validate_config"]