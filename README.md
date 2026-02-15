# A-Maze-Ing

Proyecto de generación, validación y resolución de laberintos en Python, con soporte para renderizado ASCII y gráfico, animaciones y pruebas unitarias.

---

## Estructura del proyecto

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

##Tabla de combinaciones de paredes

| Binario | Decimal | Hexadecimal | Muros cerrados     |
| ------- | ------- | ----------- | ------------------ |
| 0000    | 0       | 0x0         | Ninguno            |
| 0001    | 1       | 0x1         | N                  |
| 0010    | 2       | 0x2         | E                  |
| 0011    | 3       | 0x3         | N, E               |
| 0100    | 4       | 0x4         | S                  |
| 0101    | 5       | 0x5         | N, S               |
| 0110    | 6       | 0x6         | E, S               |
| 0111    | 7       | 0x7         | N, E, S            |
| 1000    | 8       | 0x8         | O                  |
| 1001    | 9       | 0x9         | N, O               |
| 1010    | 10      | 0xA         | E, O               |
| 1011    | 11      | 0xB         | N, E, O            |
| 1100    | 12      | 0xC         | S, O               |
| 1101    | 13      | 0xD         | N, S, O            |
| 1110    | 14      | 0xE         | E, S, O            |
| 1111    | 15      | 0xF         | Todos (N, E, S, O) |
