from math import prod
from typing import Generator, NamedTuple


class Coordinate(NamedTuple):
    row: int
    column: int


heightmap = []
with open("day_9/input.txt") as puzzle_input:
    lines = puzzle_input.readlines()
    for line in lines:
        clean_line = line.strip()
        individual_numbers = list(clean_line)
        heightmap.append(list(map(int, individual_numbers)))

rightmost_column = len(heightmap[0]) - 1
bottommost_row = len(heightmap) - 1

known_not_lowest = set()
risk_level = 0

for row in range(len(heightmap)):
    for column in range(len(heightmap[0])):
        coord = Coordinate(row, column)

        # Skip if we're in the known not lowest
        if coord in known_not_lowest:
            continue

        value = heightmap[row][column]

        # Check each surrounding tile, adding them to the known not-lowest
        # If they are too small

        smallest = True
        # Skip top if we're on the top row
        if row != 0:
            if heightmap[row-1][column] <= value:
                smallest = False

        # Skip right if we're on the right border
        if column != rightmost_column:
            if heightmap[row][column+1] <= value:
                smallest = False
            else:
                known_not_lowest.add(Coordinate(row, column+1))

        # Skip the bottom if we're at the bottom
        if row != bottommost_row:
            if heightmap[row+1][column] <= value:
                smallest = False
            else:
                known_not_lowest.add(Coordinate(row+1, column))

        # Skip the left if we're on the leftmost column
        if column != 0:
            if heightmap[row][column-1] <= value:
                smallest = False

        if smallest is True:
            risk_level += 1 + value

print("Part 1:")
print(risk_level)  # 1198: too high

# Part 2

def get_all_basin_points(map: list[list[int]], start: Coordinate) -> set[Coordinate]:
    rightmost_column = len(map[0]) - 1
    bottommost_row = len(map) - 1

    def generate_surrounding_points(point: Coordinate) -> Generator[Coordinate, None, None]:
        if point.row != 0:
            yield Coordinate(point.row - 1, point.column)
        if point.column != rightmost_column:
            yield Coordinate(point.row, point.column + 1)
        if point.row != bottommost_row:
            yield Coordinate(point.row + 1, point.column)
        if point.column != 0:
            yield Coordinate(point.row, point.column - 1)

    basin_points = {start}
    stack = [start]

    while len(stack) != 0:
        current_point = stack.pop()
        for point in generate_surrounding_points(current_point):
            if point in basin_points:
                continue
            if map[point.row][point.column] == 9:
                continue
            basin_points.add(point)
            stack.append(point)

    return basin_points

basins: list[set[Coordinate]] = []

for row in range(len(heightmap)):
    for column in range(len(heightmap[0])):
        current_point = Coordinate(row, column)

        if heightmap[current_point.row][current_point.column] == 9:
            continue

        found = False
        for basin in basins:
            if current_point in basin:
                found = True
                break
        
        if found is True:
            continue

        basins.append(get_all_basin_points(heightmap, current_point))

basin_sizes = sorted(list(map(len, basins)), reverse=True)

print("Part 2:")
print(prod(basin_sizes[:3]))
