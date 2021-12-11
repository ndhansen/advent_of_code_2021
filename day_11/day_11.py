from __future__ import annotations
from typing import NamedTuple
from copy import deepcopy


class Coordinate(NamedTuple):
    row: int
    column: int

    def get_surrounding_coordinates(self, map_corner: Coordinate) -> list[Coordinate]:
        surrounding_points = []

        # Get top left
        if self.row != 0 and self.column != 0:
            surrounding_points.append(Coordinate(self.row - 1, self.column - 1))

        # Get top
        if self.row != 0:
            surrounding_points.append(Coordinate(self.row - 1, self.column))

        # Get top right
        if self.row != 0 and self.column != map_corner.column:
            surrounding_points.append(Coordinate(self.row - 1, self.column + 1))

        # Get right
        if self.column != map_corner.column:
            surrounding_points.append(Coordinate(self.row, self.column + 1))

        # Get bottom right
        if self.row != map_corner.row and self.column != map_corner.column:
            surrounding_points.append(Coordinate(self.row + 1, self.column + 1))

        # Get bottom
        if self.row != map_corner.row:
            surrounding_points.append(Coordinate(self.row + 1, self.column))

        # Get bottom left
        if self.row != map_corner.row and self.column != 0:
            surrounding_points.append(Coordinate(self.row + 1, self.column - 1))

        # Get left
        if self.column != 0:
            surrounding_points.append(Coordinate(self.row, self.column - 1))

        return surrounding_points


def pretty_print_map(puzzle_map: list[list[int]]) -> None:
    for line in puzzle_map:
        print("".join([str(number) for number in line]))
    print()


original_puzzle_map = []
with open("day_11/input.txt") as puzzle_input:
    for line in puzzle_input.readlines():
        cleaned_line = line.strip()
        line_as_letters = list(cleaned_line)
        original_puzzle_map.append(list(map(int, line_as_letters)))

# Part 1

puzzle_map = deepcopy(original_puzzle_map)
map_corner = Coordinate(len(puzzle_map) - 1, len(puzzle_map[0]) - 1)

times_flashed = 0
for step in range(10):
    # Add one to each item
    for line in puzzle_map:
        for i in range(len(line)):
            line[i] += 1

    # Start the avalance
    triggered: set[Coordinate] = set()
    bumped: set[Coordinate] = set()

    # Go through the map, trigger all the ones above 9
    for row in range(len(puzzle_map)):
        for column in range(len(puzzle_map[0])):
            point = Coordinate(row, column)
            if puzzle_map[point.row][point.column] > 9:
                bumped.add(point)
                triggered.add(point)

    while len(bumped) > 0:
        point = bumped.pop()

        # increment the surrounding points
        for surrounding_point in point.get_surrounding_coordinates(map_corner):
            puzzle_map[surrounding_point.row][surrounding_point.column] += 1

            # If the surrounding point is now past 9, add it to the list
            if (
                puzzle_map[surrounding_point.row][surrounding_point.column] > 9
                and surrounding_point not in triggered
            ):
                triggered.add(surrounding_point)
                bumped.add(surrounding_point)

    times_flashed += len(triggered)
    for point in triggered:
        puzzle_map[point.row][point.column] = 0

    # pretty_print_map(puzzle_map)

print("Part 1:")
print(times_flashed)

puzzle_map = deepcopy(original_puzzle_map)

# Part 2:
step = 1
while True:
    # Add one to each item
    for line in puzzle_map:
        for i in range(len(line)):
            line[i] += 1

    # Start the avalance
    triggered: set[Coordinate] = set()
    bumped: set[Coordinate] = set()

    # Go through the map, trigger all the ones above 9
    for row in range(len(puzzle_map)):
        for column in range(len(puzzle_map[0])):
            point = Coordinate(row, column)
            if puzzle_map[point.row][point.column] > 9:
                bumped.add(point)
                triggered.add(point)

    while len(bumped) > 0:
        point = bumped.pop()

        # increment the surrounding points
        for surrounding_point in point.get_surrounding_coordinates(map_corner):
            puzzle_map[surrounding_point.row][surrounding_point.column] += 1

            # If the surrounding point is now past 9, add it to the list
            if (
                puzzle_map[surrounding_point.row][surrounding_point.column] > 9
                and surrounding_point not in triggered
            ):
                triggered.add(surrounding_point)
                bumped.add(surrounding_point)

    for point in triggered:
        puzzle_map[point.row][point.column] = 0

    if len(triggered) == len(puzzle_map) * len(puzzle_map[0]):
        print("Part 2:")  # 214: too low
        print(step)
        # pretty_print_map(puzzle_map)
        break

    step += 1
