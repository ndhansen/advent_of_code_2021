from dataclasses import dataclass
from functools import partial
from typing import List, NamedTuple
from itertools import chain
from enum import Enum

@dataclass(frozen=True)
class Puzzle:
    rows: List[List[int]]
    columns: List[List[int]]
    lines: List[List[int]]

    @staticmethod
    def from_lines(lines: List[str]) -> "Puzzle":
        rows = []
        for line in lines:
            line = line.strip()
            split_line = line.split()
            rows.append(list(map(int, split_line)))

        columns = list(zip(*rows))
        return Puzzle(rows, columns, [*rows, *columns])

    def get_winning_sum(self, numbers_slice: List[int]) -> int:
        puzzle_numbers = chain(*self.rows)
        unused_numbers = filter(lambda x: x not in numbers_slice, puzzle_numbers)
        return sum(unused_numbers)


class Combination(NamedTuple):
    puzzle: Puzzle
    index: int
    number: int
    number_index: int


class Goal(Enum):
    WIN = "WIN"
    LOSE = "LOSE"


def get_winning_index(numbers: List[int], puzzle: Puzzle) -> int:
    def find_last_index(numbers: List[int], line: List[int]) -> int:
        indexes = []
        for number in line:
            indexes.append(numbers.index(number))
        return max(indexes)

    find_last_index_with_numbers = partial(find_last_index, numbers)
    indexes = map(find_last_index_with_numbers, puzzle.lines)
    return min(indexes)


def find_puzzle(puzzles: List[Puzzle], numbers: List[int], strategy: Goal = Goal.WIN) -> Combination:
    get_winning_index_with_numbers = partial(get_winning_index, numbers)
    winning_indexes = list(map(get_winning_index_with_numbers, puzzles))
    if strategy == Goal.WIN:
        selector = min
    elif strategy == Goal.LOSE:
        selector = max
    number_index = selector(winning_indexes)
    puzzle_index = winning_indexes.index(number_index)
    winning_number = numbers[number_index]
    return Combination(puzzles[puzzle_index], puzzle_index, winning_number, number_index)


with open("day_4/input.txt") as puzzle_input:
    random_numbers_raw = puzzle_input.readline().strip().split(",")
    random_numbers = list(map(int, random_numbers_raw))
    _ = puzzle_input.readline() # ignore blank line

    puzzle_rows = puzzle_input.readlines()

puzzles: List[Puzzle] = []
puzzle_lines = []
for puzzle_row in puzzle_rows:
    if puzzle_row.strip() == "":
        puzzles.append(Puzzle.from_lines(puzzle_lines))
        puzzle_lines = []
    else:
        puzzle_lines.append(puzzle_row)

# Get the index of the winning puzzle
winning_puzzle = find_puzzle(puzzles, random_numbers)

# Get the winning sum
winning_numbers_slice = random_numbers[:winning_puzzle.number_index+1]
winning_sum = winning_puzzle.puzzle.get_winning_sum(winning_numbers_slice)

print("Part 1:")
print(winning_sum * winning_puzzle.number)

# Part two

# Get the losing puzzle index
losing_puzzle = find_puzzle(puzzles, random_numbers, Goal.LOSE)

# Get the winning sum
winning_numbers_slice = random_numbers[:losing_puzzle.number_index+1]
losing_sum = losing_puzzle.puzzle.get_winning_sum(winning_numbers_slice)

print("Part 2:")
print(losing_sum * losing_puzzle.number)