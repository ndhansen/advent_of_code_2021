from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Area():
    x_left: int
    x_right: int
    y_top: int
    y_bottom: int

    def in_range(self, x: int, y: int) -> bool:
        if x >= self.x_left and x <= self.x_right:
            if y >= self.y_bottom and y <= self.y_top:
                return True
        return False

    @staticmethod
    def from_target(target: str) -> Area:
        target = target.split(": ")[1].strip()
        x_str, y_str = target.split(", ")
        x_str = x_str.split("=")[1]
        y_str = y_str.split("=")[1]
        x_first_str, x_second_str = x_str.split("..")
        y_first_str, y_second_str = y_str.split("..")
        x_first = int(x_first_str)
        x_second = int(x_second_str)
        y_first = int(y_first_str)
        y_second = int(y_second_str)

        x_left = min(x_first, x_second)
        x_right = max(x_first, x_second)
        y_top = max(y_first, y_second)
        y_bottom = min(y_first, y_second)

        return Area(x_left, x_right, y_top, y_bottom)


with open("day_17/input.txt") as puzzle_input:
    line = puzzle_input.readline().strip()
target = Area.from_target(line)

# Calculate the minimum and maximum x velocity
# 1 + 2 + 3 + ... + ? = x_left, for example

def get_slowest_x_velocity(target: int) -> int:
    last_num = 1
    total = 1
    while total < target:
        last_num += 1
        total += last_num

    return last_num


def get_fastest_x_velocity(target: int) -> int:
    last_num = 1
    total = 1
    while True:
        next_num = last_num + 1
        if next_num + total > target:
            return last_num
        last_num = next_num
        total += last_num


max_y_velocity = abs(target.y_bottom) - 1
max_y = sum(x for x in range(max_y_velocity + 1))

print("Part 1:")
print(max_y)

# Part 2

min_y_velocity = target.y_bottom
min_x_velocity = get_slowest_x_velocity(target.x_left)
max_x_velocity = target.x_right

max_number_of_steps = max((2 * max_y_velocity) + 2, max_x_velocity + 1)

total_count = 0
for x in range(min_x_velocity, max_x_velocity + 1):
    for y in range(min_y_velocity, max_y_velocity + 1):
        current_x = x
        x_vel = x
        current_y = y
        y_vel = y

        steps = 0
        while steps < max_number_of_steps:
            if target.in_range(current_x, current_y):
                total_count += 1
                break
            steps += 1
            x_vel = max(0, x_vel - 1)
            y_vel -= 1
            current_x += x_vel
            current_y += y_vel

print("Part 2:")
print(total_count)
