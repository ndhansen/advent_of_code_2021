from collections import defaultdict
from typing import DefaultDict, Generator, NamedTuple
from enum import Enum, auto


class Coordinate(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()
    DIAGONAL = auto()


class Line(NamedTuple):
    start: Coordinate
    end: Coordinate

    @property
    def direction(self) -> Direction:
        if self.start.x == self.end.x:
            return Direction.VERTICAL
        elif self.start.y == self.end.y:
            return Direction.HORIZONTAL
        return Direction.DIAGONAL

    @property
    def points(self) -> Generator[Coordinate, None, None]:
        """Get all the points between the start and the end, inclusive. """
        match self.direction:
            case Direction.VERTICAL:
                if self.start.y < self.end.y:
                    step = 1
                else:
                    step = -1

                for y in range(self.start.y, self.end.y + step, step):
                    yield Coordinate(self.start.x, y)

            case Direction.HORIZONTAL:
                if self.start.x < self.end.x:
                    step = 1
                else:
                    step = -1

                for x in range(self.start.x, self.end.x + step, step):
                    yield Coordinate(x, self.start.y)

            case Direction.DIAGONAL:
                if self.start.x < self.end.x:
                    x_step = 1
                else:
                    x_step = -1

                if self.start.y < self.end.y:
                    y_step = 1
                else:
                    y_step = -1

                for x, y in zip(
                    range(self.start.x, self.end.x + x_step, x_step),
                    range(self.start.y, self.end.y + y_step, y_step)
                ):
                    yield Coordinate(x, y)


lines: list[Line] = []
with open("day_5/input.txt") as puzzle_file:
    for line in puzzle_file.readlines():
        raw_coordinates = line.strip().split(" -> ")
        start_raw = raw_coordinates[0].split(",")
        end_raw = raw_coordinates[1].split(",")
        start = Coordinate(int(start_raw[0]), int(start_raw[1]))
        end = Coordinate(int(end_raw[0]), int(end_raw[1]))
        lines.append(Line(start, end))

points: DefaultDict[Coordinate, int] = defaultdict(int)
for line in lines:
    if line.direction == Direction.DIAGONAL:
        continue
    for point in line.points:
        points[point] += 1

number_of_points_above_1 = 0
for point in points.values():
    if point >= 2:
        number_of_points_above_1 += 1

print("Part 1:")
print(number_of_points_above_1)

# Part 2

points: DefaultDict[Coordinate, int] = defaultdict(int)
for line in lines:
    for point in line.points:
        points[point] += 1

number_of_points_above_1 = 0
for point in points.values():
    if point >= 2:
        number_of_points_above_1 += 1

print("Part 2:")
print(number_of_points_above_1)
