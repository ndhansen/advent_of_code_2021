from collections import defaultdict
from typing import DefaultDict


lantern_fish: DefaultDict[int, int] = defaultdict(int)

DURATION = 3650

with open("day_6/input.txt") as puzzle_input:
    fish_line = puzzle_input.readline().strip()
    all_fish = list(map(int, fish_line.split(",")))

for fish in all_fish:
    lantern_fish[fish] += 1

for day in range(DURATION):
    # I could do an in-place shuffle, but urgh, I don't want to
    updated_lantern_fish = defaultdict(int)
    
    # Give birth
    updated_lantern_fish[8] = lantern_fish[0]
    updated_lantern_fish[6] = lantern_fish[0]

    for i in range(8, 0, -1):
        updated_lantern_fish[i-1] += lantern_fish[i]

    lantern_fish = updated_lantern_fish

print("Part 1:")
print(sum(lantern_fish.values()))