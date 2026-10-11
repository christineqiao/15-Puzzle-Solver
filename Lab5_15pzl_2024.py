
import sys
import time


def inversion_count(state, goal, size=4):
    order = {tile: i for i, tile in enumerate(goal) if tile != '_'}
    tiles = [order[tile] for tile in state if tile != '_']
    inversions = sum(tiles[i] > tiles[j]
                     for i in range(len(tiles))
                     for j in range(i + 1, len(tiles)))

    if size % 2 == 1:
        return inversions % 2 == 0

    state_blank_from_bottom = size - state.index('_') // size
    goal_blank_from_bottom = size - goal.index('_') // size

    return (inversions + state_blank_from_bottom - goal_blank_from_bottom) % 2 == 0


def manhattan_distance(state, goal, size=4):
    positions = {tile: i for i, tile in enumerate(goal)}
    distance = 0

    for i, tile in enumerate(state):
        if tile != '_':
            j = positions[tile]
            distance += abs(i // size - j // size) + abs(i % size - j % size)

    return distance


def swap(state, i, j):
    chars = list(state)
    chars[i], chars[j] = chars[j], chars[i]
    return ''.join(chars)


def generate_children(state, size=4):
    blank = state.index('_')
    row, col = divmod(blank, size)
    children = []

    if row < size - 1:
        children.append(swap(state, blank, blank + size))
    if col < size - 1:
        children.append(swap(state, blank, blank + 1))
    if row > 0:
        children.append(swap(state, blank, blank - size))
    if col > 0:
        children.append(swap(state, blank, blank - 1))

    return children


def direction_of_move(state, child, size=4):
    old = state.index('_')
    new = child.index('_')

    if new == old + size:
        return 'D'
    if new == old - size:
        return 'U'
    if new == old + 1:
        return 'R'
    if new == old - 1:
        return 'L'

    raise ValueError('States are not one legal move apart')


class HeapPriorityQueue:
    def __init__(self):
        self.data = []

    def push(self, priority, puzzle, path):
        self.data.append((priority, puzzle, path))
        self.bubble_up(len(self.data) - 1)

    def pop(self):
        if not self.data:
            raise IndexError('pop from empty priority queue')

        if len(self.data) == 1:
            return self.data.pop()

        top = self.data[0]
        self.data[0] = self.data.pop()
        self.bubble_down(0)

        return top

    def bubble_up(self, index):
        while index > 0:
            parent = (index - 1) // 2

            if self.data[index][0] >= self.data[parent][0]:
                break

            self.data[index], self.data[parent] = (
                self.data[parent], self.data[index]
            )
            index = parent

    def bubble_down(self, index):
        while True:
            left = 2 * index + 1
            right = left + 1
            smallest = index

            if (left < len(self.data)
                    and self.data[left][0] < self.data[smallest][0]):
                smallest = left

            if (right < len(self.data)
                    and self.data[right][0] < self.data[smallest][0]):
                smallest = right

            if smallest == index:
                break

            self.data[index], self.data[smallest] = (
                self.data[smallest], self.data[index]
            )
            index = smallest

    def is_empty(self):
        return not self.data


def a_star(start, goal, size=4):
    if start == goal:
        return 'G'

    if not inversion_count(start, goal, size):
        return 'X'

    frontier = HeapPriorityQueue()
    frontier.push(manhattan_distance(start, goal, size), start, '')

    best_cost = {start: 0}

    while not frontier.is_empty():
        priority, current, path = frontier.pop()
        steps = len(path)

        if steps != best_cost.get(current):
            continue

        if current == goal:
            return path

        for child in generate_children(current, size):
            new_cost = steps + 1

            if new_cost < best_cost.get(child, float('inf')):
                best_cost[child] = new_cost

                new_path = path + direction_of_move(
                    current, child, size
                )

                estimate = manhattan_distance(child, goal, size)

                frontier.push(
                    new_cost + estimate,
                    child,
                    new_path
                )

    return 'X'


def validate_puzzle(state, goal, size=4):
    expected = size * size

    if len(state) != expected or len(goal) != expected:
        raise ValueError(
            f'Each puzzle must contain exactly {expected} characters'
        )

    if (state.count('_') != 1
            or goal.count('_') != 1
            or sorted(state) != sorted(goal)):
        raise ValueError(
            'Puzzle and goal must have the same unique tiles and one underscore'
        )

    if len(set(state)) != expected:
        raise ValueError('Puzzle tiles must be unique')


def main():
    if len(sys.argv) != 2:
        print('Usage: python 15_puzzle_solver.py puzzles.txt')
        return 1

    with open(sys.argv[1], encoding='utf-8') as file:
        puzzles = [
            ''.join(line.split())
            for line in file
            if line.strip()
        ]

    if not puzzles:
        print('Input file is empty')
        return 1

    goal = puzzles[0]

    for idx, puzzle in enumerate(puzzles):
        start_time = time.perf_counter()

        try:
            validate_puzzle(puzzle, goal)
            result = a_star(puzzle, goal)
        except ValueError as error:
            result = f'ERROR: {error}'

        elapsed = time.perf_counter() - start_time

        print(f'{idx}: {puzzle} {result} in {elapsed:.3f}s')

    return 0


if __name__ == '__main__':
    sys.exit(main())
