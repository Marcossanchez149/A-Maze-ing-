# A-Maze-Ing

Proyecto de generación, validación y resolución de laberintos en Python, con soporte para renderizado ASCII y gráfico, animaciones y pruebas unitarias.

---

## Estructura del proyecto

```text
project/
├── core/
│   ├── __init__.py
│   ├── cell.py
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
├── validations/
│   ├── __init__.py
│   └── maze_validation.py
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
