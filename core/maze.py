"""
maze.py
File that contains Maze class
"""

from core.cell import Cell
from typing import Tuple, List


class Maze:
    """
    Represents a rectangular maze with
    configurable size, entry/exit points,
    and optionally perfect maze properties
    (no loops, single path between cells).

    Attributes:
        width (int): The number of columns in the maze.
        height (int): The number of rows in the maze.
        perfect (bool): If True, the maze will have no loops (default: True).
        seed (int): Random seed for maze generation (default: 1).
        entry (Tuple[int, int]): Coordinates of
        the maze entry point (default: (0, 0)).
        exit (Tuple[int, int]): Coordinates of the maze exit point
        (default: bottom-right corner).
        grid (List[List[Cell]]): 2D list of Cell objects representing the maze.
    """

    def __init__(
        self,
        width: int,
        height: int,
        perfect: bool = True,
        seed: int = 1,
        entry: Tuple[int, int] = (0, 0),
        exit: Tuple[int, int] = None
    ):
        """
        Initializes a Maze instance with the given dimensions and options.

        Args:
            width (int): Number of columns in the maze.
            height (int): Number of rows in the maze.
            perfect (bool, optional): Whether the
            maze is perfect (default: True).
            seed (int, optional): Seed for random
            number generation (default: 1).
            entry (Tuple[int, int], optional): Entry point
            coordinates (default: (0, 0)).
            exit (Tuple[int, int], optional): Exit point coordinates
                                              (default: bottom-right corner).
        """
        self.width = width
        self.height = height
        self.perfect = perfect
        self.seed = seed
        self.entry = entry
        self.exit = exit or (width - 1, height - 1)

        self.grid: List[List[Cell]] = [
            [Cell(x, y) for x in range(width)] for y in range(height)
        ]

        self._open_external_walls()

    def get_cell(self, x: int, y: int) -> Cell:
        """
        Returns the Cell object at the specified coordinates.

        Args:
            x (int): Column index of the cell.
            y (int): Row index of the cell.

        Returns:
            Cell: The cell located at (x, y).

        Raises:
            IndexError: If the coordinates are outside the maze boundaries.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"Cell coordinates out of bounds: ({x}, {y})")
        return self.grid[y][x]

    def remove_wall_between(self, cell1: Cell, cell2: Cell) -> None:
        """
        Removes the wall between two adjacent cells to create a passage,
        ensuring consistency by removing the corresponding walls on both cells.

        The method checks the relative position of the two cells and removes
        the appropriate walls:
        - If cell2 is to the right of cell1, remove the east wall of cell1
        and the west wall of cell2.
        - If cell2 is to the left of cell1, remove the west wall of cell1
        and the east wall of cell2.
        - If cell2 is below cell1, remove the south wall of cell1 and the
        north wall of cell2.
        - If cell2 is above cell1, remove the north wall of cell1 and the
        south wall of cell2.

        Args:
            cell1 (Cell): The first cell.
            cell2 (Cell): The second cell, adjacent to the first one.

        Raises:
            ValueError: If the two cells are not adjacent.
        """

        dx = cell2.x - cell1.x
        dy = cell2.y - cell1.y

        if dx == 1 and dy == 0:  # cell2 derecha
            cell1.remove_wall("E")
            cell2.remove_wall("W")
        elif dx == -1 and dy == 0:  # cell2 izquierda
            cell1.remove_wall("W")
            cell2.remove_wall("E")
        elif dx == 0 and dy == 1:  # cell2 abajo
            cell1.remove_wall("S")
            cell2.remove_wall("N")
        elif dx == 0 and dy == -1:  # cell2 arriba
            cell1.remove_wall("N")
            cell2.remove_wall("S")
        else:
            raise ValueError("Cells are not adjacent")

    def _open_external_walls(self) -> None:
        """
        Adds walls to the outer border cells of the maze.

        Each cell on the edge of the maze will have a wall facing outward:
            - 'N' for north/top
            - 'S' for south/bottom
            - 'W' for west/left
            - 'E' for east/right
        """
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                if y == 0:
                    if x > 0:
                        cell.remove_wall("W")
                    if x < self.width - 1:
                        cell.remove_wall("E")
                    cell.remove_wall("S")

                elif y == self.height - 1:
                    if x > 0:
                        cell.remove_wall("W")
                    if x < self.width - 1:
                        cell.remove_wall("E")
                    cell.remove_wall("N")

                elif x == 0:
                    cell.remove_wall("E")
                    if y > 0:
                        cell.remove_wall("N")
                    if y < self.height - 1:
                        cell.remove_wall("S")

                elif x == self.width - 1:
                    cell.remove_wall("W")
                    if y > 0:
                        cell.remove_wall("N")
                    if y < self.height - 1:
                        cell.remove_wall("S")

    def print_hex(self) -> None:
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                cell = self.get_cell(x, y)
                row += cell.to_hex()
            print(row)
