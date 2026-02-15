"""
Package manager for core
"""


__version__ = "1.0.0"

from .cell import Cell
from .maze import Maze

from .constants import WALL_MASKS

__all__ = ["Cell", "Maze", "WALL_MASKS"]
