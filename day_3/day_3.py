from functools import partial
from typing import List

raw_data = []
with open("day_3/input.txt") as puzzle_file:
    for line in puzzle_file.readlines():
        raw_data.append(line.strip())

data_length = len(raw_data)
data = map(list, raw_data)
data = zip(*data)
data = map(lambda x: [int(y) for y in x], data)
data = map(sum, data)
data = map(lambda x: x - (data_length // 2), data)
data = map(lambda x: 1 if x > 0 else 0, data)
final_number = list(data)
epsilon_str = map(lambda x: 0 if x == 1 else 1, final_number)
gamma = int("".join([str(bit) for bit in final_number]), base=2)
epsilon = int("".join([str(bit) for bit in epsilon_str]), base=2)
print("Part 1:")
print(gamma * epsilon)

# Part 2

def get_largest_occurrence(data: List[str]) -> str:
    zeroes = data.count("0")
    ones = data.count("1")
    if ones == 0:
        return "0"
    if zeroes == 0:
        return "1"
    if zeroes > ones:
        return "0"
    return "1"

def get_smallest_occurrence(data: List[str]) -> str:
    zeroes = data.count("0")
    ones = data.count("1")
    if ones == 0:
        return "0"
    if zeroes == 0:
        return "1"
    if ones >= zeroes:
        return "0"
    return "1"

# Oxygen rating
oxygen = list(map(list, raw_data))
oxygen_reading = []
co_two = list(map(list, raw_data))
co_two_reading = []

for i in range(len(raw_data[0])):
    largest = get_largest_occurrence(list(zip(*oxygen))[i])
    smallest = get_smallest_occurrence(list(zip(*co_two))[i])

    oxygen_reading.append(largest)
    co_two_reading.append(smallest)

    oxygen = list(filter(lambda x: x[i] == largest, oxygen))
    co_two = list(filter(lambda x: x[i] == smallest, co_two))

oxygen_int = int("".join(oxygen_reading), base=2)
co_two_int = int("".join(co_two_reading), base=2)

print("Part 2:")
print(oxygen_int  * co_two_int)
    