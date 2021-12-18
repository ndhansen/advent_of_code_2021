from __future__ import annotations
from dataclasses import dataclass
from functools import reduce
from typing import Optional
from enum import Enum
from itertools import combinations


class Side(Enum):
    LEFT = 3
    RIGHT = 2


@dataclass
class Leaf:
    value: int
    depth: int
    side: Optional[Side] = None
    left: Optional[Leaf] = None
    right: Optional[Leaf] = None

    def copy(self) -> Leaf:
        start = Leaf(self.value, self.depth, self.side)
        last = start
        current = self.right
        while current is not None:
            last = Leaf(current.value, current.depth, current.side, last)
            current = current.right
        last.add_right(None)
        return start

    def add_right(self, last: Optional[Leaf]) -> None:
        self.right = last
        if self.left is not None:
            self.left.add_right(self)

    @staticmethod
    def from_str(line: str) -> Leaf:
        depth = 0
        last = None
        for character in line:
            if character == "[":
                depth += 1
            elif character == "]":
                depth -= 1
            elif character == ",":
                continue
            else:
                current = Leaf(int(character), depth, left=last)
                last = current
        last.add_right(None)

        # Get the left-most leaf
        current = last
        while current.left != None:
            current = current.left

        return current


def try_to_explode(start: Leaf) -> tuple(bool, Leaf):
    current = start
    while current.right is not None:
        if current.depth < 5:
            current = current.right
            continue

        if current.depth == current.right.depth:  # We have a pair
            right = current.right
            if current.left is not None:
                current.left.value += current.value
            if right.right is not None:
                right.right.value += right.value

            # if current.left is None:
            #     side = Side.LEFT
            # elif right.right is None:
            #     side = Side.RIGHT
            # elif current.left.depth == current.depth - 1:
            #     side = Side.RIGHT
            # elif right.right.depth == current.depth - 1:
            #     side = Side.LEFT
            # elif current.left.depth < current.depth:
            #     side = Side.LEFT
            # else:
            #     side = Side.RIGHT
            new_node = Leaf(0, current.depth - 1, left=current.left, right=right.right)

            # Point the left and right nodes to the new node
            # god bless I'm not doing this in rust 🙏
            if current.left is not None:
                current.left.right = new_node
            else:
                start = new_node

            if right.right is not None:
                right.right.left = new_node

            return (True, start)

        current = current.right

    return (False, start)


def split_number(current: Leaf) -> tuple(Leaf, Leaf):
    assert current.value > 9
    left = Leaf(current.value // 2, current.depth + 1, left=current.left)
    right = Leaf((current.value // 2) + (current.value % 2), current.depth + 1, left=left, right=current.right)
    left.right = right
    return (left, right)


def try_to_split(start: Leaf) -> tuple(bool, Leaf):
    current = start
    while True:
        if current.value > 9:
            left, right = split_number(current)

            # Set the next node to point to our "right" node
            if current.right is not None:
                current.right.left = right

            if current.left is not None:
                current.left.right = left
            else:
                start = left

            return (True, start)

        if current.right is None:
            break

        current = current.right

    return (False, start)


def add(left_start: Leaf, right_start: Leaf) -> Leaf:
    # Go through left, adding one to depth
    current = left_start
    while current.right != None:
        current.depth += 1
        current = current.right
    current.depth += 1

    # Map the last left node to the start of right
    current.right = right_start

    # Map the first right node to the end of the left
    right_start.left = current

    # Go through the right, adding one to the depth
    current = right_start
    while current.right != None:
        current.depth += 1
        current = current.right
    current.depth += 1

    return left_start


def try_to_apply_rules(start: Leaf) -> tuple[bool, Leaf]:
    changed, start = try_to_explode(start)
    if changed is True:
        return (True, start)
    changed, start = try_to_split(start)
    if changed is True:
        return (True, start)
    return (False, start)


def reduce(start: Leaf) -> Leaf:
    changed = True
    while changed is True:
        changed, start = try_to_apply_rules(start)
        
    return start


def calculate_side(start: Optional[Leaf], last_pair_depth: Optional[int] = None) -> None:
    if start is None:
        return

    start.side = Side.LEFT
    if start.right is None:
        # THis is __totally__ wrong, but w/e
        start.side = Side.RIGHT
        return

    if start.depth == start.right.depth:
        start.right.side = Side.RIGHT
        adjacent = start.right.right

        # Check if this pair closes out an alread open pair
        if adjacent is None:
            return

        if last_pair_depth is not None and last_pair_depth == start.depth:
            return calculate_side(adjacent)
        elif start.left is not None and start.left.side == Side.LEFT and start.left.depth == start.depth - 1:
            return calculate_side(adjacent)
        else:
            if adjacent.depth == start.depth:
                return calculate_side(adjacent, start.depth)

        last = start.right
        while adjacent is not None:
            if adjacent.depth == last.depth - 1:
                adjacent.side = Side.RIGHT
                last = adjacent
                adjacent = adjacent.right
            else:
                return calculate_side(adjacent)
    else:
        return calculate_side(start.right)


def wipe_sides(start: Leaf) -> None:
    start.side = None
    current = start.right
    while current is not None:
        current.side = None
        current = current.right


def consolidate_nodes(start: Leaf) -> Leaf:
    current_leaf = start
    while True:
        if current_leaf.right is None:
            break
        next_leaf = current_leaf.right

        if current_leaf.depth == next_leaf.depth and current_leaf.side == Side.LEFT and next_leaf.side == Side.RIGHT:
            new_leaf = Leaf(
                3 * current_leaf.value + 2 * next_leaf.value,
                current_leaf.depth - 1,
                left=current_leaf.left,
                right=next_leaf.right
            )
            if current_leaf.left is not None:
                current_leaf.left.right = new_leaf
            else:
                start = new_leaf
            
            if next_leaf.right is not None:
                next_leaf.right.left = new_leaf

            return start

        current_leaf = next_leaf

    return start

def get_magnitude(start: Leaf) -> int:
    while start.right is not None:
        wipe_sides(start)
        calculate_side(start)
        start = consolidate_nodes(start)
    return start.value


numbers: list[Leaf] = []
with open("day_18/input.txt") as puzzle_input:
    for line in puzzle_input.readlines():
        numbers.append(Leaf.from_str(line.strip()))

current = numbers[0]
current = reduce(current)
for number in numbers[1:]:
    current = add(current, number)
    current = reduce(current)

print("Part 1:")
print(get_magnitude(current))

# Part 2

numbers: list[Leaf] = []
with open("day_18/input.txt") as puzzle_input:
    for line in puzzle_input.readlines():
        numbers.append(Leaf.from_str(line.strip()))

# magnitudes = []
# for index, number in enumerate(numbers):
#     magnitudes.append((index, get_magnitude(number)))
# magnitudes = sorted(magnitudes, key=lambda x: x[1], reverse=True)
# print(magnitudes)

largest = 0
for left, right in combinations(numbers, 2):
    first = add(left.copy(), right.copy())
    first = reduce(first)
    largest = max(get_magnitude(first), largest)
    second = add(right.copy(), left.copy())
    second = reduce(second)
    largest = max(get_magnitude(second), largest)

print("Part 2:")
print(largest)  # 10000 too high
