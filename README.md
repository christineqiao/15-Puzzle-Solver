# 15-Puzzle-Solver
A Python implementation of a 15-puzzle solver that explores heuristic search algorithms and data structures to solve sliding-tile puzzles.

The 15-puzzle consists of a 4×4 grid containing 15 numbered tiles and one empty space. The objective is to rearrange the tiles into a target configuration by sliding adjacent tiles into the empty space.

## Features

- A* search algorithm
- Custom min-heap priority queue
- Manhattan distance heuristic
- Solvability checking

## How to Run

1. Install Python 3.
2. Create a `puzzles.txt` file.
3. Run the following command:

```bash
python3 15_puzzle_solver.py puzzles.txt
```

## Example Input

```text
123456789ABCDEF_
123456789ABCDE_F
```

## Technologies

- Python 3
- A* Search
- Heuristic Search
