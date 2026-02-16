# A-Maze-Ing

Project for maze generation, validation, and solving in Python, with support for ASCII and graphical rendering, animations, and unit tests.

---

## Project Structure

```text
project/
├── core/
│   ├── __init__.py
│   ├── cell.py
│   ├── constants.py
│   ├── maze.py
│   └── solver.py
├── generators/
│   ├── __init__.py
│   ├── maze_generator.py     
│   └── algorithms.py        
├── render/
│   ├── __init__.py
│   ├── render.py             
│   ├── ascii.py
│   └── graphic.py
├── config/
│   ├── __init__.py
│   ├── constants.py
│   ├── parser.py
│   ├── types.py
│   └── validator.py
├── animations/
│   ├── __init__.py
│   └── animator.py
├── tests/
│   ├── __init__.py
│   ├── test_maze.py
│   ├── test_cell.py
│   ├── test_generator.py
│   └── test_solver.py
├── a_maze_ing.py
├── config.txt
├── .gitignore
└── makefile

## Wall Combinations Table LSB

| Binary  | Decimal | Hexadecimal |    Closed Walls    |
| ------- | ------- | ----------- | ------------------ |
| 0000    | 0       | 0x0         | Ninguno            |
| 0001    | 1       | 0x1         | N                  |
| 0010    | 2       | 0x2         | E                  |
| 0011    | 3       | 0x3         | E, N               |
| 0100    | 4       | 0x4         | S                  |
| 0101    | 5       | 0x5         | S, N               |
| 0110    | 6       | 0x6         | S, E               |
| 0111    | 7       | 0x7         | S, E, N            |
| 1000    | 8       | 0x8         | W                  |
| 1001    | 9       | 0x9         | W, N               |
| 1010    | 10      | 0xA         | W, E               |
| 1011    | 11      | 0xB         | W, E, N            |
| 1100    | 12      | 0xC         | W, S               |
| 1101    | 13      | 0xD         | W, S, N            |
| 1110    | 14      | 0xE         | W, S, E            |
| 1111    | 15      | 0xF         | -All- (W, S, E, N) |
