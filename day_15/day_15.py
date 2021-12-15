from __future__ import annotations
from collections import defaultdict
from typing import NamedTuple
from copy import deepcopy
from heapq import heappop, heappush


class Coordinate(NamedTuple):
    row: int
    column: int

    def get_neighbors(self, far_corner: Coordinate) -> list[Coordinate]:
        neighbors = []

        # Exclude left if on left border
        if self.row != 0:
            neighbors.append(Coordinate(self.row - 1, self.column))

        # Exclude top if on border
        if self.column != 0:
            neighbors.append(Coordinate(self.row, self.column - 1))

        # Exclude if on right border
        if self.row != far_corner.row:
            neighbors.append(Coordinate(self.row + 1, self.column))

        if self.column != far_corner.column:
            neighbors.append(Coordinate(self.row, self.column + 1))

        return neighbors


puzzle_map: list[list[int]] = []

with open("day_15/input.txt") as puzzle_input:
    for line in puzzle_input.readlines():
        numbers_line = list(line.strip())
        numbers = list(map(int, numbers_line))
        puzzle_map.append(numbers)

# Part 1
# Let's just go for basic A*, thanks wikipedia


def reconstruct_path(
    came_from: dict[Coordinate, Coordinate], current: Coordinate
) -> list[Coordinate]:
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def manhattan_distance(node: Coordinate, goal: Coordinate) -> int:
    cost = 0
    cost += abs(goal.row - node.row)
    cost += abs(goal.column - node.column)
    return cost


def a_star(
    start: Coordinate, goal: Coordinate, puzzle_map: list[list[int]]
) -> list[Coordinate]:
    far_corner = Coordinate(len(puzzle_map) - 1, len(puzzle_map[0]) - 1)

    open_set: list[tuple[int, Coordinate]] = []
    heappush(open_set, (manhattan_distance(start, goal), start))

    came_from = dict()

    g_score: defaultdict[Coordinate, int] = defaultdict(lambda: 10 * len(puzzle_map) * len(puzzle_map[0]))
    g_score[start] = puzzle_map[start.row][start.column]

    f_score: defaultdict[Coordinate, int] = defaultdict(lambda: 10 * len(puzzle_map) * len(puzzle_map[0]))
    f_score[start] = g_score[start] + manhattan_distance(start, goal)

    while len(open_set) > 0:
        _, current = heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in current.get_neighbors(far_corner):
            weight = puzzle_map[neighbor.row][neighbor.column]
            tentative_g_score = g_score[current] + weight
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)
                if neighbor not in open_set:
                    heappush(open_set, (f_score[neighbor], neighbor))

    return []


def get_cost(path: list[Coordinate], puzzle_map: list[list[int]]) -> int:
    cost = 0
    for point in path:
        cost += puzzle_map[point.row][point.column]
    return cost


start = Coordinate(0, 0)
end = Coordinate(len(puzzle_map) - 1, len(puzzle_map[0]) - 1)

path = a_star(start, end, puzzle_map)

print("Part 1:")
print(get_cost(path, puzzle_map) - puzzle_map[0][0])

# Part 2

uber_map: list[list[list[list[int]]]] = list([[] for _ in range(5)] for _ in range(5))
uber_map[0][0] = puzzle_map

increment = [
    [0, 1, 2, 3, 4],
    [1, 2, 3, 4, 5],
    [2, 3, 4, 5, 6],
    [3, 4, 5, 6, 7],
    [4, 5, 6, 7, 8],
]


def increment_map(increment: int, puzzle_map: list[list[int]]) -> list[list[int]]:
    new_map = deepcopy(puzzle_map)
    for row in range(len(new_map)):
        for column in range(len(new_map[row])):
            new_map[row][column] = (((new_map[row][column] + increment) - 1) % 9) + 1

    return new_map


for row in range(len(increment)):
    for column in range(len(increment[0])):
        uber_map[row][column] = increment_map(increment[row][column], puzzle_map)


def join_maps_horizontally(*puzzle_maps: list[list[int]]) -> list[list[int]]:
    new_map = [[] for _ in range(len(puzzle_maps[0]))]
    for row in range(len(puzzle_maps[0])):
        for puzzle_map in puzzle_maps:
            new_map[row].extend(puzzle_map[row])
    return new_map


new_map = []
for row in range(len(increment)):
    new_map.extend(join_maps_horizontally(*uber_map[row]))


start = Coordinate(0, 0)
end = Coordinate(len(new_map) - 1, len(new_map[0]) - 1)

path = a_star(start, end, new_map)

print("Part 2:")
print(get_cost(path, new_map) - new_map[0][0])