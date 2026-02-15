"""
render.py
Defines contract for render
"""


from abc import ABC, abstractmethod


class Render(ABC):
    """
    Render
    Main Render class
    """
    @abstractmethod
    def draw_maze(self, maze):
        """
        Draw a maze

        :param self: own instance
        :param maze: maze to draw
        """
        pass

    @abstractmethod
    def draw_cell(self, cell):
        """
        Draw a cell

        :param self: own instance
        :param cell: cell to draw
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Clear the screen

        :param self: own instance
        """
        pass
