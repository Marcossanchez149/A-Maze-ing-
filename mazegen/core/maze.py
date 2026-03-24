from core.cell import Cell
from typing import Tuple, List


class Maze:

    def __init__(
        self,
        width: int,
        height: int,
        perfect: bool = True,
        seed: int = 1,
        entry: Tuple[int, int] = (0, 0),
        exit: Tuple[int, int] = (0, 0)
    ) -> None:

        self.width = width
        self.height = height
        self.perfect = perfect
        self.seed = seed
        self.entry = entry
        self.exit = exit or (width - 1, height - 1)

        self.grid: List[List[Cell]] = [
            [Cell(x, y) for x in range(width)] for y in range(height)
        ]

    def get_cell(self, x: int, y: int) -> Cell:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"Cell coordinates out of bounds: ({x}, {y})")
        return self.grid[y][x]

    def get_neighbors(self, cell: Cell) -> List[Cell]:
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = cell.x + dx, cell.y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append(self.get_cell(nx, ny))
        return neighbors

    def has_wall_between(self, cell1: Cell, cell2: Cell) -> bool:
        dx = cell2.x - cell1.x
        dy = cell2.y - cell1.y

        if dx == 1:
            return cell1.has_wall("E")
        elif dx == -1:
            return cell1.has_wall("W")
        elif dy == 1:
            return cell1.has_wall("S")
        elif dy == -1:
            return cell1.has_wall("N")

        return True

    def remove_wall_between(self, cell1: Cell, cell2: Cell) -> None:
        dx = cell2.x - cell1.x
        dy = cell2.y - cell1.y

        if dx == 1 and dy == 0:
            cell1.remove_wall("E")
            cell2.remove_wall("W")
        elif dx == -1 and dy == 0:
            cell1.remove_wall("W")
            cell2.remove_wall("E")
        elif dx == 0 and dy == 1:
            cell1.remove_wall("S")
            cell2.remove_wall("N")
        elif dx == 0 and dy == -1:
            cell1.remove_wall("N")
            cell2.remove_wall("S")
        else:
            raise ValueError("Cells are not adjacent")

    def add_wall_between(self, cell1: Cell, cell2: Cell) -> None:
        dx = cell2.x - cell1.x
        dy = cell2.y - cell1.y

        if dx == 1:
            cell1.add_wall("E")
            cell2.add_wall("W")
        elif dx == -1:
            cell1.add_wall("W")
            cell2.add_wall("E")
        elif dy == 1:
            cell1.add_wall("S")
            cell2.add_wall("N")
        elif dy == -1:
            cell1.add_wall("N")
            cell2.add_wall("S")

    def has_open_area(self, w: int, h: int) -> bool:
        for y in range(self.height - h + 1):
            for x in range(self.width - w + 1):

                open_area = True

                # horizontales
                for dy in range(h):
                    for dx in range(w - 1):
                        c1 = self.get_cell(x + dx, y + dy)
                        c2 = self.get_cell(x + dx + 1, y + dy)

                        if self.has_wall_between(c1, c2):
                            open_area = False
                            break
                    if not open_area:
                        break

                if not open_area:
                    continue

                # verticales
                for dy in range(h - 1):
                    for dx in range(w):
                        c1 = self.get_cell(x + dx, y + dy)
                        c2 = self.get_cell(x + dx, y + dy + 1)

                        if self.has_wall_between(c1, c2):
                            open_area = False
                            break
                    if not open_area:
                        break

                if open_area:
                    return True

        return False

    def has_invalid_room(self) -> bool:
        forbidden = [(3, 3), (2, 4), (4, 2)]

        for w, h in forbidden:
            if self.has_open_area(w, h):
                return True

        return False

    def save_hex(self, file_path: str) -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            for y in range(self.height):
                row = ""
                for x in range(self.width):
                    cell = self.get_cell(x, y)
                    row += cell.to_hex()
                f.write(row + "\n")
            f.write(f"\n{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.exit[0]},{self.exit[1]}\n")
