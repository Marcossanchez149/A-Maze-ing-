from core.maze import Maze


class MazeGenerator:
    # Crear clase Algorithm con cada 1 de los alg = a un num
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
