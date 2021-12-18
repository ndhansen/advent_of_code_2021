from __future__ import annotations
from typing import Optional, Union
from dataclasses import dataclass


@dataclass
class Pair:
    left: Union[Pair, int]
    right: Union[Pair, int]
    parent: Optional[Pair]

    def add_parents(self, parent: Optional[Pair] = None) -> None:
        self.parent = parent
        if isinstance(self.left, Pair):
            self.left.add_parents(self)
        if isinstance(self.right, Pair):
            self.right.add_parents(self)

    def is_primitive(self) -> bool:
        return isinstance(self.left, int) and isinstance(self.right, int)

    @staticmethod
    def from_string(line: str) -> Pair:
        as_list: list = eval(line)
        pair = Pair.from_list(as_list)
        pair.add_parents()
        return pair

    @staticmethod
    def from_list(line: list) -> Pair:
        if isinstance(line[0], int):
            left = line[0]
        else:
            left = Pair.from_list(line[0])

        if isinstance(line[1], int):
            right = line[1]
        else:
            right = Pair.from_list(line[1])

        return Pair(left, right)


def split_number(number: int) -> Pair:
    assert number > 9
    return Pair(number // 2, (number // 2) + (number % 2))


def add(left: Pair, right: Pair) -> Pair:
    return Pair(left, right)


def try_to_explode(pair: Pair, depth = 0) -> bool:
    # Find the first pair to explode
    if depth >= 4 and pair.is_primitive():
        # Search left for a number to increase

        # Search right for a number to increase

        # Replace the pair with a 0
        pass
    
    else:
        if isinstance(pair.left, Pair):
            exploded_left = try_to_explode(pair.left, depth + 1)
            if exploded_left is True:
                return True
        if isinstance(pair.right, Pair):
            exploded_right = try_to_explode(pair.right, depth + 1)
            return exploded_right
        return False


def split(pair: Pair) -> None:
    pass


with open("day_18/test.txt") as puzzle_input:
    for line in puzzle_input.readlines():
        pass