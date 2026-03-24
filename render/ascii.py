import time
from typing import List, Optional, Tuple

from core.maze import Maze
from core.solver import shortest_path, save_solution
from .render import Render

from mazegen.maze_generator import MazeGenerator, InvalidEntryOrExit

Pos = Tuple[int, int]


class AsciiRender(Render):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        # toggles
        self.show_path = False
        self.use_color = True
        self.colorize_logo_42 = True

        # animation
        self.animate_path = True
        self.path_delay = 0.02  # seconds per step

        # wall color palettes (ANSI)
        self.wall_palettes = [
            "\x1b[37m",  # white
            "\x1b[36m",  # cyan
            "\x1b[31m",  # red
            "\x1b[32m",  # green
            "\x1b[33m",  # yellow
        ]
        self.wall_palette_index = 0

        # extra colors
        self.reset = "\x1b[0m"
        self.logo_42_color = "\x1b[35m"  # magenta
        self.path_color = "\x1b[93m"     # bright yellow

        self._cached_path: Optional[List[Pos]] = None

    def run(
        self,
        maze: Maze,
        *,
        generator: MazeGenerator,
        algorithm: str = "dfs",
        seed: int = 1,
        apply_logo_42: bool = False,
    ) -> None:
        """
        Interactive ASCII loop:
          r = regenerate
          p = show/hide shortest path (animated if enabled)
          c = change wall color
          l = toggle 42 color
          a = toggle path animation
          q = quit
        """
        save_solution(maze, shortest_path(maze), self.file_path)
        while True:
            self._clear()

            path = None
            if self.show_path:
                if self._cached_path is None:
                    self._cached_path = shortest_path(maze)
                path = self._cached_path

            self.draw_maze(maze, path=path)
            self._print_menu()

            cmd = input("> ").strip().lower()
            if cmd in ("q", "quit", "exit"):
                return
            if cmd == "r":
                new_maze = Maze(
                    width=maze.width,
                    height=maze.height,
                    perfect=maze.perfect,
                    seed=maze.seed,
                    entry=maze.entry,
                    exit=maze.exit,
                )

                if apply_logo_42:
                    try:
                        generator.set_logo_42(new_maze)
                    except InvalidEntryOrExit:
                        pass

                generator.generate_maze(new_maze, algorithm)
                maze = new_maze
                self._cached_path = None
                save_solution(maze, shortest_path(maze), self.file_path)
                if self.show_path:
                    self._cached_path = shortest_path(maze)
                    if self.animate_path and self._cached_path:
                        self._animate_path_once(maze, self._cached_path)

            elif cmd == "p":
                self.show_path = not self.show_path

                if self.show_path:
                    self._cached_path = shortest_path(maze)
                    if self.animate_path and self._cached_path:
                        self._animate_path_once(maze, self._cached_path)
                # if turning off, nothing special

            elif cmd == "c":
                self.wall_palette_index = ((self.wall_palette_index + 1) %
                                           len(self.wall_palettes))

            elif cmd == "l":
                self.colorize_logo_42 = not self.colorize_logo_42

            elif cmd in ("color", "ansi"):
                self.use_color = not self.use_color

            elif cmd == "a":
                self.animate_path = not self.animate_path

    def draw_maze(self, maze: Maze, *,
                  path: Optional[List[Pos]] = None) -> None:
        path_set = set(path or [])

        wall_color = self.wall_palettes[self.wall_palette_index] if (
            self.use_color) else ""
        reset = self.reset if self.use_color else ""
        path_color = self.path_color if self.use_color else ""
        logo_color = (self.logo_42_color if (self.use_color and
                                             self.colorize_logo_42) else "")

        def w(s: str) -> str:
            return f"{wall_color}{s}{reset}" if self.use_color else s

        def logo(s: str) -> str:
            return f"{logo_color}{s}{reset}" if logo_color else s

        def pch(s: str) -> str:
            return f"{path_color}{s}{reset}" if self.use_color else s

        # --- top border ---
        top_line = w("+")
        for x in range(maze.width):
            cell = maze.get_cell(x, 0)
            if cell.is_fixed():
                top_line += logo("---") + w("+")
            else:
                top_line += w("---+") if cell.has_wall("N") else w("   +")
        print(top_line)

        # --- rows ---
        for y in range(maze.height):
            middle_line = ""
            for x in range(maze.width):
                cell = maze.get_cell(x, y)

                # left wall
                if cell.is_fixed():
                    middle_line += w("|")
                else:
                    middle_line += w("|") if cell.has_wall("W") else " "

                # content
                pos = (x, y)
                if pos == maze.entry:
                    middle_line += " x "
                elif pos == maze.exit:
                    middle_line += " o "
                elif pos in path_set and not cell.is_fixed():
                    middle_line += pch(" . ")
                else:
                    if cell.is_fixed():
                        middle_line += logo("***")
                    else:
                        middle_line += "   "

            last_cell = maze.get_cell(maze.width - 1, y)
            middle_line += w("|") if last_cell.has_wall("E") else " "
            print(middle_line)

            # bottom border
            bottom_line = w("+")
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if cell.is_fixed():
                    bottom_line += logo("---") + w("+")
                else:
                    bottom_line += w("---+") if (
                        cell.has_wall("S")) else w("   +")
            print(bottom_line)

    def _animate_path_once(self, maze: Maze, path: List[Pos]) -> None:
        """
        Reveal the path progressively (ASCII animation).
        """
        for k in range(1, len(path) + 1):
            self._clear()
            self.draw_maze(maze, path=path[:k])
            self._print_menu()
            time.sleep(self.path_delay)

    def _print_menu(self) -> None:
        print()
        print(
            "Commands: [r] regenerate | [p] path"
            " on/off | [a] path anim on/off | "
            "[c] wall color | [l] 42 color | [color] ansi on/off | [q] quit"
        )

    def _clear(self) -> None:
        # ANSI clear screen + cursor home
        print("\x1b[2J\x1b[H", end="")
