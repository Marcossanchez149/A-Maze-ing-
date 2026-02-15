"""
ascii.py
Draw a maze using ascii , based on Render class
"""


from .render import Render


# TO FIX
class AsciiRender(Render):
    """
    AsciiRender class that implements how to draw a maze
    with ascii characters
    """
    def draw_maze(self, maze):
        """
        Draw a maze

        :param self: own instance
        :param maze: maze to draw
        """
        pass

    def draw_cell(self, cell):
        """
        Draw a cell

        :param self: own instance
        :param cell: cell to draw
        """
        pass

    def clear(self):
        """
        Clear the screen

        :param self: own instance
        """
        pass
