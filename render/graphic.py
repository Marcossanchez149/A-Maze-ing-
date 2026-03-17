"""
Docstring for render.graphic
"""


import pygame
from core.maze import Maze
from .render import Render


class PygameRender(Render):
    def __init__(
        self,
        cell_size: int = 32,
        wall_thickness: int = 3,
        margin: int = 20,
        fps: int = 60,
    ) -> None:
        self.cell_size = cell_size
        self.wall_thickness = wall_thickness
        self.margin = margin
        self.fps = fps

        # Colors
        self.bg = (20, 20, 20)
        self.wall = (240, 240, 240)
        self.fixed_fill = (70, 70, 70)
        self.entry_color = (80, 200, 120)
        self.exit_color = (220, 120, 120)

    def draw_maze(self, maze: Maze) -> None:
        pygame.init()

        width_px = self.margin * 2 + maze.width * self.cell_size
        height_px = self.margin * 2 + maze.height * self.cell_size

        screen = pygame.display.set_mode((width_px, height_px))
        pygame.display.set_caption("Maze (Pygame Render)")

        clock = pygame.time.Clock()

        running = True
        while running:
            # --- events ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # optional: ESC closes
                if (event.type == pygame.KEYDOWN and
                   event.key == pygame.K_ESCAPE):
                    running = False

            # --- draw ---
            screen.fill(self.bg)
            self._draw_grid_and_walls(screen, maze)
            self._draw_entry_exit(screen, maze)

            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()

    def _draw_grid_and_walls(self, screen: pygame.Surface, maze: Maze) -> None:
        cs = self.cell_size
        m = self.margin
        t = self.wall_thickness

        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)

                x0 = m + x * cs
                y0 = m + y * cs
                x1 = x0 + cs
                y1 = y0 + cs

                # Fill fixed cells
                if cell.is_fixed():
                    pygame.draw.rect(screen, self.fixed_fill,
                                     pygame.Rect(x0, y0, cs, cs))

                # Draw walls if present
                fixed = cell.is_fixed()

                if fixed or cell.has_wall("N"):
                    pygame.draw.line(screen, self.wall, (x0, y0), (x1, y0), t)
                if fixed or cell.has_wall("S"):
                    pygame.draw.line(screen, self.wall, (x0, y1), (x1, y1), t)
                if fixed or cell.has_wall("W"):
                    pygame.draw.line(screen, self.wall, (x0, y0), (x0, y1), t)
                if fixed or cell.has_wall("E"):
                    pygame.draw.line(screen, self.wall, (x1, y0), (x1, y1), t)

    def _draw_entry_exit(self, screen: pygame.Surface, maze: Maze) -> None:
        cs = self.cell_size
        m = self.margin

        def cell_rect(pos):
            x, y = pos
            return pygame.Rect(m + x * cs, m + y * cs, cs, cs)

        # Entry
        if getattr(maze, "entry", None) is not None:
            pygame.draw.rect(screen, self.entry_color,
                             cell_rect(maze.entry).inflate(-cs // 3, -cs // 3))

        # Exit
        if getattr(maze, "exit", None) is not None:
            pygame.draw.rect(screen, self.exit_color,
                             cell_rect(maze.exit).inflate(-cs // 3, -cs // 3))
