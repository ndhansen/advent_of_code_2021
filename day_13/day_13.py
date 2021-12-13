from typing import NamedTuple
from enum import Enum, auto


class Coordinate(NamedTuple):
    row: int
    column: int


class FoldDirection(Enum):
    ROW = auto()
    COLUMN = auto()


class Fold(NamedTuple):
    fold_axis: FoldDirection
    place: int


matrix: set[Coordinate] = set()
fold_instructions: list[Fold] = []


with open("day_13/input.txt") as puzzle_input:
    coordinates, raw_fold_instructions = puzzle_input.read().strip().split("\n\n", 2)

for line in coordinates.split("\n"):
    column, row = line.strip().split(",")
    matrix.add(Coordinate(int(row), int(column)))

for instruction in raw_fold_instructions.split("\n"):
    instruction = instruction.rsplit(" ", 1)
    axis, place = instruction[1].split("=")
    fold_direction: FoldDirection
    if axis == "x":
        fold_direction = FoldDirection.COLUMN
    elif axis == "y":
        fold_direction = FoldDirection.ROW
    fold_instructions.append(Fold(fold_direction, int(place)))

# Part 1

def fold_matrix(matrix: set[Coordinate], fold_instructions: list[FoldDirection]) -> set[Coordinate]:
    for fold_instruction in fold_instructions:
        index: int
        if fold_instruction.fold_axis == FoldDirection.ROW:
            index = 0
        elif fold_instruction.fold_axis == FoldDirection.COLUMN:
            index = 1

        new_matrix: set[Coordinate] = set()
        for coordinate in matrix:
            if coordinate[index] > fold_instruction.place:
                diff = coordinate[index] - fold_instruction.place

                new_coord: Coordinate
                if fold_instruction.fold_axis == FoldDirection.ROW:
                    row = coordinate.row - (2 * diff)
                    new_coord = Coordinate(row, coordinate.column)
                elif fold_instruction.fold_axis == FoldDirection.COLUMN:
                    column = coordinate.column - (2 * diff)
                    new_coord = Coordinate(coordinate.row, column)

                new_matrix.add(new_coord)

            else:
                new_matrix.add(coordinate)

        matrix = new_matrix

    return new_matrix


matrix = fold_matrix(matrix, [fold_instructions.pop(0)])

print("Part 1:")
print(len(matrix))

# Part 2:

matrix = fold_matrix(matrix, fold_instructions)

display: list[list[str]] = [[" " for _ in range(40)] for _ in range(6)]
for coordinate in matrix:
    display[coordinate.row][coordinate.column] = "x"

for line in display:
    print("".join(line))
