"""
ascii.py
File that contains AsciiRender class
"""
from .render import Render


class AsciiRender(Render):
    """
    ASCII-based maze renderer.

    This renderer outputs a maze representation to the console
    using ASCII characters. Walls are represented using '+', '-',
    and '|' characters, while empty spaces represent open paths.
    """

    def draw_maze(self, maze):
        """
        Render the maze to the console using ASCII characters.

        The maze is drawn with:
        - '+' representing corners
        - '---' representing horizontal walls
        - '|' representing vertical walls
        - Spaces representing open paths

        The maze object is expected to provide:
        - width (int): number of columns
        - height (int): number of rows
        - get_cell(x, y): returns a cell object
        - cell.has_wall(direction): returns True if a wall exists
          in the given direction ("N", "S", "E", "W")

        Args:
            maze: The maze instance to render.
        """

        # Draw the top border
        top_line = "+"
        for x in range(maze.width):
            cell = maze.get_cell(x, 0)
            top_line += "---+" if cell.has_wall("N") else "   +"
        print(top_line)

        # Draw each row of cells
        for y in range(maze.height):
            # Middle line (cell content with walls)
            middle_line = ""
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                # Add left wall if exists, otherwise space
                middle_line += "|" if cell.has_wall("W") else " "
                # Add cell content (3 spaces)
                middle_line += "   "

            # Add right wall for the last cell
            last_cell = maze.get_cell(maze.width - 1, y)
            middle_line += "|" if last_cell.has_wall("E") else " "
            print(middle_line)

            # Draw bottom border for this row
            bottom_line = "+"
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                bottom_line += "---+" if cell.has_wall("S") else "   +"
            print(bottom_line)
