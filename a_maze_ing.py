# a_maze_ing.py

from config.parser import parse_config_file
from config.validator import validate_config
from core.maze import Maze

def main():
    print("A-Maze-Ing\n")
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

    print("Maze in HEX:")
    maze.print_hex()

if __name__ == "__main__":
    main()
