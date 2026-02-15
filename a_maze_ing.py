# a_maze_ing.py

from config.parser import parse_config_file
from config.validator import validate_config
from core.maze import Maze
from render import AsciiRender


def main():
    print("A-Maze-Ing\n")
    try:
        config = parse_config_file("config.txt")
        config = validate_config(config)

        print("-------Config-------")
        print(config)
        print()
        width = config.get("width", 10)
        height = config.get("height", 10)

        maze = Maze(
            width=width,
            height=height,
        )

        ascii_render = AsciiRender()

        print("Maze in HEX:")
        maze.print_hex()

        print("\nMaze in Ascii:\n")
        ascii_render.draw_maze(maze)

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
