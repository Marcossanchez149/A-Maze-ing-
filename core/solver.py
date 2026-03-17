"""
solver.py contains solvers
"""

from collections import deque
from typing import Optional, List, Tuple, Dict
from core.maze import Maze

Pos = Tuple[int, int]

def shortest_path(maze: Maze) -> Optional[List[Pos]]:
        start = maze.entry
        goal = maze.exit

        if maze.get_cell(*start).is_fixed() or maze.get_cell(*goal).is_fixed():
            return None

        q = deque([start])
        prev: Dict[Pos, Optional[Pos]] = {start: None}

        while q:
            x, y = q.popleft()
            if (x, y) == goal:
                break

            cell = maze.get_cell(x, y)
            candidates = [
                ("N", (x, y - 1)),
                ("S", (x, y + 1)),
                ("W", (x - 1, y)),
                ("E", (x + 1, y)),
            ]

            for d, (nx, ny) in candidates:
                if not (0 <= nx < maze.width and 0 <= ny < maze.height):
                    continue
                if cell.has_wall(d):
                    continue

                ncell = maze.get_cell(nx, ny)
                if ncell.is_fixed():
                    continue

                np = (nx, ny)
                if np in prev:
                    continue

                prev[np] = (x, y)
                q.append(np)

        if goal not in prev:
            return None

        path: List[Pos] = []
        cur: Optional[Pos] = goal
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return path