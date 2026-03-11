from core.cell import Cell
from core.maze import Maze
import random


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

        start_x = random.randint(0, maze.width - 1)
        start_y = random.randint(0, maze.height - 1)

        start_cell = maze.get_cell(start_x, start_y)
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
                    if neighbor.visited:
                        visited_neighbors.append(neighbor)

            if visited_neighbors:
                chosen_neighbor = random.choice(visited_neighbors)
                maze.remove_wall_between(current_cell, chosen_neighbor)

            current_cell.visited = True
            add_frontier_neighbors(current_cell)
