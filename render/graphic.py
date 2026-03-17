"""
Docstring for render.graphic
"""

from typing import List, Optional, Tuple

import pygame

from core.maze import Maze
from core.solver import shortest_path
from .render import Render
from generators.maze_generator import MazeGenerator, InvalidEntryOrExit

Pos = Tuple[int, int]

class PygameRender(Render):
    def __init__(
        self,
        cell_size: int = 32,
        wall_thickness: int = 5,
        margin: int = 20,
        fps: int = 60,
    ) -> None:
        self.cell_size = cell_size
        self.wall_thickness = wall_thickness
        self.margin = margin
        self.fps = fps

        # UI toggles
        self.show_path = False
        self.colorize_logo_42 = True

        # Path animation state
        self.path_animating = False
        self.path_anim_index = 0
        self.path_step_ms = 25
        self._last_path_step_ms = 0

        # Colors / palettes
        self.bg = (20, 20, 20)
        self.fixed_fill_default = (70, 70, 70)
        self.fixed_fill_42 = (120, 90, 220)
        self.path_color = (255, 215, 0)
        self.entry_color = (80, 200, 120)
        self.exit_color = (220, 120, 120)

        self.wall_palettes = [
            (240, 240, 240),
            (0, 200, 255),
            (255, 120, 120),
            (120, 255, 120),
            (255, 200, 0),
        ]
        self.wall_palette_index = 0

        self._cached_path: Optional[List[Pos]] = None

        self.menu_height = 90
        self.menu_bg = (10, 10, 10)
        self.menu_text = (230, 230, 230)
        self.menu_accent = (160, 160, 160)

    @property
    def wall(self):
        return self.wall_palettes[self.wall_palette_index]

    def _start_path_animation(self, maze: Maze) -> None:
        """
        Ensure cached path exists, then start animation from the beginning.
        Safe to call after regenerating.
        """
        if self._cached_path is None:
            self._cached_path = shortest_path(maze)

        # even if path is None/empty, keep state consistent
        self.path_animating = True
        self.path_anim_index = 0
        self._last_path_step_ms = pygame.time.get_ticks()

    def draw_maze(
        self,
        maze: Maze,
        *,
        generator: Optional[MazeGenerator] = None,
        algorithm: str = "dfs",
        seed: Optional[int] = None,
        apply_logo_42: bool = False,
    ) -> None:
        pygame.init()

        width_px = self.margin * 2 + maze.width * self.cell_size
        height_px = self.margin * 2 + maze.height * self.cell_size

        screen = pygame.display.set_mode((width_px, height_px + self.menu_height))
        pygame.display.set_caption("Maze (Pygame Render)")

        clock = pygame.time.Clock()

        running = True
        while running:
            # --- events ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    # Re-generate
                    if event.key == pygame.K_r:
                        if generator is None:
                            print("No generator provided to PygameRender.draw_maze(...). Can't regenerate.")
                        else:
                            new_maze = Maze(
                                width=maze.width,
                                height=maze.height,
                                perfect=maze.perfect,
                                seed=seed or maze.seed,
                                entry=maze.entry,
                                exit=maze.exit,
                            )

                            if apply_logo_42:
                                try:
                                    generator.set_logo_42(new_maze)
                                except InvalidEntryOrExit:
                                    print("Entry/Exit overlap with logo 42. Skipping logo.")

                            generator.generate_maze(new_maze, algorithm)

                            maze = new_maze
                            self._cached_path = None  # invalidate cache

                            # IMPORTANT: if path was enabled, recompute + restart animation
                            if self.show_path:
                                self._start_path_animation(maze)
                            else:
                                self.path_animating = False
                                self.path_anim_index = 0

                    # Show/Hide shortest path
                    if event.key == pygame.K_p:
                        self.show_path = not self.show_path

                        if not self.show_path:
                            self.path_animating = False
                            self.path_anim_index = 0
                        else:
                            self._start_path_animation(maze)

                    # Change wall colors
                    if event.key == pygame.K_c:
                        self.wall_palette_index = (self.wall_palette_index + 1) % len(self.wall_palettes)

                    # Toggle logo 42 color
                    if event.key == pygame.K_l:
                        self.colorize_logo_42 = not self.colorize_logo_42

            # --- draw ---
            screen.fill(self.bg)
            self._draw_grid_and_walls(screen, maze)

            if self.show_path:
                if self._cached_path is None:
                    self._cached_path = shortest_path(maze)

                if self._cached_path:
                    if self.path_animating:
                        now = pygame.time.get_ticks()
                        if now - self._last_path_step_ms >= self.path_step_ms:
                            self._last_path_step_ms = now
                            self.path_anim_index += 1

                            if self.path_anim_index >= len(self._cached_path):
                                self.path_anim_index = len(self._cached_path)
                                self.path_animating = False

                    partial_path = self._cached_path[: self.path_anim_index]
                    self._draw_path(screen, maze, partial_path)

            self._draw_entry_exit(screen, maze)
            self._draw_menu(screen, maze)

            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()

    def _draw_menu(self, screen: pygame.Surface, maze: Maze) -> None:
        maze_h_px = self.margin * 2 + maze.height * self.cell_size
        menu_rect = pygame.Rect(0, maze_h_px, screen.get_width(), self.menu_height)

        pygame.draw.rect(screen, self.menu_bg, menu_rect)
        pygame.draw.line(screen, self.menu_accent, (0, maze_h_px), (screen.get_width(), maze_h_px), 2)

        font = pygame.font.SysFont(None, 22)
        font_small = pygame.font.SysFont(None, 20)

        line1 = "R: Regenerate   P: Show/Hide shortest path"
        line2 = "C: Change color   L: Toggle 42 color   ESC: Quit"
        line3 = f"Path: {'ON' if self.show_path else 'OFF'}    Wall palette: {self.wall_palette_index + 1}"

        text1 = font.render(line1, True, self.menu_text)
        text2 = font.render(line2, True, self.menu_text)
        text3 = font_small.render(line3, True, self.menu_text)

        pad_x = 12
        pad_y = 10
        screen.blit(text1, (pad_x, maze_h_px + pad_y))
        screen.blit(text2, (pad_x, maze_h_px + pad_y + 28))
        screen.blit(text3, (pad_x, maze_h_px + pad_y + 56))

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

                if cell.is_fixed():
                    fill = self.fixed_fill_42 if self.colorize_logo_42 else self.fixed_fill_default
                    pygame.draw.rect(screen, fill, pygame.Rect(x0, y0, cs, cs))

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

        def cell_rect(pos: Pos) -> pygame.Rect:
            x, y = pos
            return pygame.Rect(m + x * cs, m + y * cs, cs, cs)

        if getattr(maze, "entry", None) is not None:
            pygame.draw.rect(
                screen,
                self.entry_color,
                cell_rect(maze.entry).inflate(-cs // 3, -cs // 3),
            )

        if getattr(maze, "exit", None) is not None:
            pygame.draw.rect(
                screen,
                self.exit_color,
                cell_rect(maze.exit).inflate(-cs // 3, -cs // 3),
            )

    def _draw_path(self, screen: pygame.Surface, maze: Maze, path: Optional[List[Pos]]) -> None:
        if not path:
            return

        cs = self.cell_size
        m = self.margin

        for (x, y) in path:
            x0 = m + x * cs
            y0 = m + y * cs
            rect = pygame.Rect(x0, y0, cs, cs).inflate(-cs // 2, -cs // 2)
            pygame.draw.rect(screen, self.path_color, rect)
