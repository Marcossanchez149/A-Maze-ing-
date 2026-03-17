#!/usr/bin/env python3

from config.parser import parse_config_file
from config.validator import validate_config
from core.maze import Maze
from generators.maze_generator import MazeGenerator
from render import AsciiRender, PygameRender


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
        algorithm = config.get("algorithm")
        seed = config.get("seed")

        maze = Maze(
            width=width,
            height=height,
            entry=entry,
            exit=exit
        )
        generator = MazeGenerator(seed)
        try:
            generator.set_logo_42(maze)
        except Exception:
            print("The entry or the exit are on an invalid position")
            return
        generator.generate_maze(maze, algorithm)
        ascii_render = AsciiRender()

        print("Maze in HEX:")
        maze.print_hex()

        print("\nMaze in Ascii:\n")
        ascii_render.draw_maze(maze)

        renderer = PygameRender(cell_size=32)
        renderer.draw_maze(maze)

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
