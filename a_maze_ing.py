#!/usr/bin/env python3

from config.parser import parse_config_file
from config.validator import validate_config
from core.maze import Maze
from render import AsciiRender
import random


def generate_maze(maze: Maze) -> None:
    """Genera un laberinto eliminando paredes entre celdas adyacentes."""
    directions = ['N', 'E', 'S', 'W']  # Norte, Este, Sur, Oeste
    stack = [(maze.entry[0], maze.entry[1])]  # Empezamos desde la entrada

    # Utilizamos un conjunto para llevar un registro de las celdas visitadas
    visited = set()
    visited.add((maze.entry[0], maze.entry[1]))

    while stack:
        x, y = stack[-1]
        current_cell = maze.get_cell(x, y)
        # Buscamos las celdas vecinas
        random.shuffle(directions)  # Mezclamos las direcciones aleatoriamente
        for direction in directions:
            if direction == 'N' and y > 0:
                neighbor = maze.get_cell(x, y - 1)
                if (x, y - 1) not in visited:
                    maze.remove_wall_between(current_cell, neighbor)
                    stack.append((x, y - 1))
                    visited.add((x, y - 1))
                    break
            elif direction == 'E' and x < maze.width - 1:
                neighbor = maze.get_cell(x + 1, y)
                if (x + 1, y) not in visited:
                    maze.remove_wall_between(current_cell, neighbor)
                    stack.append((x + 1, y))
                    visited.add((x + 1, y))
                    break
            elif direction == 'S' and y < maze.height - 1:
                neighbor = maze.get_cell(x, y + 1)
                if (x, y + 1) not in visited:
                    maze.remove_wall_between(current_cell, neighbor)
                    stack.append((x, y + 1))
                    visited.add((x, y + 1))
                    break
            elif direction == 'W' and x > 0:
                neighbor = maze.get_cell(x - 1, y)
                if (x - 1, y) not in visited:
                    maze.remove_wall_between(current_cell, neighbor)
                    stack.append((x - 1, y))
                    visited.add((x - 1, y))
                    break
        else:
            stack.pop()


def main():
    print("A-Maze-Ing\n")
    try:
        config = parse_config_file("config.txt")
        validate_config(config)

        print("-------Config-------")
        print(config)
        print()
        width = config.get("width")
        height = config.get("height")
        entry = config.get("entry")
        exit = config.get("exit")

        maze = Maze(
            width=width,
            height=height,
            entry=entry,
            exit=exit
        )
        generate_maze(maze)
        ascii_render = AsciiRender()

        print("Maze in HEX:")
        maze.print_hex()

        print("\nMaze in Ascii:\n")
        ascii_render.draw_maze(maze)

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
