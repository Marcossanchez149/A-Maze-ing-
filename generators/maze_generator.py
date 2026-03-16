from core.cell import Cell
from core.maze import Maze
import random


class InvalidEntryOrExit(Exception):
    pass


class MazeGenerator:
    # Crear clase Algorithm aqui dentro con cada 1 de los alg = a un num
    # requiere importar enum y hacer un metodo de parseo o algo asi
    # a string pero más limpio y profesional
    def generate_maze(self, maze: Maze, algorithm: str) -> None:
        algorithm = algorithm.lower()

        if algorithm == "dfs" or algorithm == "backtracking":
            self._generate_dfs(maze)
        elif algorithm == "prim":
            self._generate_prim(maze)
        elif algorithm == "kruskal":
            self._generate_kruskal(maze)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    # definir los 1 a x algoritmos

    def _generate_dfs(self, maze: Maze):
        # Algoritmo de generacion backtracking
        # Va avanzando y mirando a los vecions aleatoriamente
        # abriendo paredes al azar
        rcellx = random.randint(0, maze.width - 1)
        rcelly = random.randint(0, maze.height - 1)

        current_cell = maze.get_cell(rcellx, rcelly)
        current_cell.visited = True

        stack = [current_cell]

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        while stack:
            current_cell = stack[-1]

            unvisited_neighbors: list[Cell] = []

            for dx, dy in directions:
                nx = current_cell.x + dx
                ny = current_cell.y + dy

                if 0 <= nx < maze.width and 0 <= ny < maze.height:
                    neighbor = maze.get_cell(nx, ny)
                    if not neighbor.visited:
                        unvisited_neighbors.append(neighbor)

            if unvisited_neighbors:
                chosen_neighbor = random.choice(unvisited_neighbors)

                maze.remove_wall_between(current_cell, chosen_neighbor)
                chosen_neighbor.visited = True
                stack.append(chosen_neighbor)
            else:
                stack.pop()

    def _generate_prim(self, maze: Maze):
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        check = True
        while check:
            start_x = random.randint(0, maze.width - 1)
            start_y = random.randint(0, maze.height - 1)

            start_cell = maze.get_cell(start_x, start_y)
            if (not start_cell.is_fixed()):
                check = False
        start_cell.visited = True
        frontier = []

        def add_frontier_neighbors(cell):
            for dx, dy in directions:
                nx = cell.x + dx
                ny = cell.y + dy
                if 0 <= nx < maze.width and 0 <= ny < maze.height:
                    neighbor = maze.get_cell(nx, ny)
                    if not neighbor.visited and neighbor not in frontier:
                        frontier.append(neighbor)

        add_frontier_neighbors(start_cell)
        while frontier:
            random_index = random.randrange(len(frontier))
            current_cell: Cell = frontier.pop(random_index)

            visited_neighbors = []
            for dx, dy in directions:
                nx = current_cell.x + dx
                ny = current_cell.y + dy
                if 0 <= nx < maze.width and 0 <= ny < maze.height:
                    neighbor = maze.get_cell(nx, ny)
                    if neighbor.visited and not neighbor.is_fixed():
                        visited_neighbors.append(neighbor)

            if visited_neighbors:
                chosen_neighbor = random.choice(visited_neighbors)
                maze.remove_wall_between(current_cell, chosen_neighbor)

            current_cell.visited = True
            add_frontier_neighbors(current_cell)

    def _generate_kruskal(self, maze: Maze):
        edges = []
        for y in range(maze.height):
            for x in range(maze.width):
                current_cell = maze.get_cell(x, y)
                if not current_cell.is_fixed():
                    if x < maze.width - 1:
                        right_neighbor = maze.get_cell(x + 1, y)
                        if not right_neighbor.is_fixed():
                            edges.append((current_cell, right_neighbor))

                    if y < maze.height - 1:
                        bottom_neighbor = maze.get_cell(x, y + 1)
                        if not bottom_neighbor.is_fixed():
                            edges.append((current_cell, bottom_neighbor))

        random.shuffle(edges)
        parent = {}
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                parent[cell] = cell

        def find(cell):
            if parent[cell] != cell:
                parent[cell] = find(parent[cell])
            return parent[cell]

        def union(cell1, cell2):
            root1 = find(cell1)
            root2 = find(cell2)
            if root1 != root2:
                parent[root2] = root1

        for cell1, cell2 in edges:
            if find(cell1) != find(cell2):
                union(cell1, cell2)

                maze.remove_wall_between(cell1, cell2)

                cell1.visited = True
                cell2.visited = True

    def set_logo_42(self, maze: Maze) -> bool:
        if (maze.width < 7 or maze.height < 5):
            return False
        pattern = [
                  [1, 0, 1, 0, 1, 1, 1],
                  [1, 0, 1, 0, 0, 0, 1],
                  [1, 1, 1, 0, 1, 1, 1],
                  [0, 0, 1, 0, 1, 0, 0],
                  [0, 0, 1, 0, 1, 1, 1]
                  ]
        p_height = len(pattern)
        p_width = len(pattern[0])
        start_x = (maze.width - p_width) // 2
        start_y = (maze.height - p_height) // 2
        for y in range(p_height):
            for x in range(p_width):
                if pattern[y][x] == 1:
                    if (maze.entry == (start_x + x, start_y + y)
                       or maze.exit == (start_x + x, start_y + y)):
                        raise InvalidEntryOrExit()
                    cell = maze.get_cell(start_x + x, start_y + y)
                    cell.set_as_fixed()
                    cell.visited = True
        return True
