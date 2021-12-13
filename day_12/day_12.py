from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Mapping, NamedTuple


class Cave(NamedTuple):
    name: str
    big: bool


@dataclass
class Path():
    visited: list[Cave]
    current: Cave
    next_caves: list[Cave] = field(default_factory=list)


paths: defaultdict[Cave, set[Cave]] = defaultdict(set)

with open("day_12/input.txt") as puzzle_input:
    for line in puzzle_input.readlines():
        first, second = line.strip().split("-")
        first_cave = Cave(first, first.isupper())
        second_cave = Cave(second, second.isupper())
        paths[first_cave].add(second_cave)
        paths[second_cave].add(first_cave)

start = Cave("start", False)
end = Cave("end", False)


def get_next_caves(paths: list[Path], path_map: Mapping[Cave, set[Cave]]) -> None:
    for path in paths:
        # If we're at the end, stop
        if path.current == end:
            path.next_caves = []
        else:
            caves_cant_revisit = {cave for cave in path.visited if cave.big is False}
            path.next_caves = list(path_map[path.current] - caves_cant_revisit)


def advance_paths(paths: list[Path]) -> list[Path]:
    new_paths: list[Path] = []
    for path in paths:
        if len(path.next_caves) == 0:
            new_paths.append(path)
        else:
            # Add the current path to the visited ones
            visited = [*path.visited, path.current]

            # Get the next cave, and make it the current one
            for next_cave in path.next_caves:
                new_paths.append(Path(visited.copy(), next_cave))

    return new_paths


def done(paths: list[Path]) -> bool:
    has_paths_left = map(lambda path: len(path.next_caves) == 0, paths)
    return all(has_paths_left)


def generate_paths(
    paths: Mapping[Cave, list[Cave]]
) -> list[list[Cave]]:
    open_paths: list[Path] = [Path([], start, list(paths[start]))]
    get_next_caves(open_paths, paths)
    while done(open_paths) is False:
        open_paths = advance_paths(open_paths)
        get_next_caves(open_paths, paths)

    final_paths = []
    for path in open_paths:
        if path.current != end:
            continue
        final_paths.append([*path.visited, path.current])
    
    return final_paths


all_paths = generate_paths(paths)
for path in all_paths:
    print(",".join([cave.name for cave in path]))

print("Part 1:")
print(len(all_paths))


def get_next_caves_small_twice(paths: list[Path], path_map: Mapping[Cave, set[Cave]]) -> None:
    for path in paths:
        # If we're at the end, stop
        if path.current == end:
            path.next_caves = []
        else:
            caves_cant_revisit = set()
            total_path = [*path.visited, path.current]
            
            # check if we have a small path here twice
            small_paths = []
            for cave in total_path:
                if cave == start or cave == end:
                    continue
                if cave.big is True:
                    continue
                small_paths.append(cave)

            unique_paths = set(small_paths)
            seen_small_path_twice = False
            if len(unique_paths) < len(small_paths):
                seen_small_path_twice = True

            for cave in total_path:
                if cave.big == True:
                    continue

                if cave == start or cave == end:
                    caves_cant_revisit.add(cave)
                elif seen_small_path_twice is True:
                    caves_cant_revisit.add(cave)

            path.next_caves = list(path_map[path.current] - caves_cant_revisit)


def generate_paths_part_two(
    paths: Mapping[Cave, list[Cave]]
) -> list[list[Cave]]:
    open_paths: list[Path] = [Path([], start, list(paths[start]))]
    get_next_caves_small_twice(open_paths, paths)
    while done(open_paths) is False:
        open_paths = advance_paths(open_paths)
        get_next_caves_small_twice(open_paths, paths)

    final_paths = []
    for path in open_paths:
        if path.current != end:
            continue
        final_paths.append([*path.visited, path.current])
    
    return final_paths


all_paths = generate_paths_part_two(paths)
for path in all_paths:
    print(",".join([cave.name for cave in path]))

print("Part 2:")
print(len(all_paths))