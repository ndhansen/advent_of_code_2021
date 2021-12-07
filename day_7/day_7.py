from functools import lru_cache
from typing import DefaultDict


with open("day_7/input.txt") as puzzle_input:
    raw_line = puzzle_input.readline()
    raw_numbers = raw_line.strip().split(",")
    numbers = list(map(int, raw_numbers))

number_assignments = DefaultDict(int)
for number in numbers:
    number_assignments[number] += 1

numbers = sorted(numbers)
mode = numbers[len(numbers) // 2]

fuel = 0
for number in numbers:
    fuel += abs(mode - number)

print("Part 1")
print(fuel)

# Part 2

@lru_cache
def fuel_cost(dist: int) -> int:
    if dist == 1:
        return 1
    else:
        return fuel_cost(dist - 1) + dist

median = sum(numbers) // len(numbers)

fuel = 0
for number in numbers:
    fuel += fuel_cost(abs(median - number))

print("Part 2")
print(fuel)