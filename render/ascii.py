from .render import Render


class AsciiRender(Render):
    """
    AsciiRender class that implements how to draw a maze with ASCII characters.
    """

    def draw_cell(self, cell, is_right_edge=False):
        return

    def draw_maze(self, maze):
        """
        Draw the maze in proper ASCII, fully aligned.
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

    def clear(self):
        """
        Clear the screen

        :param self: own instance
        """
        print("\033c", end="")  # Esta secuencia de escape limpia la terminal.
