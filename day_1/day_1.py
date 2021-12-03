# Part 1
with open("day_1/input.txt") as puzzle_input:
    data = puzzle_input.readlines()

sonar_numbers = [int(line) for line in data]

increase = 0
last_num = sonar_numbers[0]
for number in sonar_numbers[1:]:
    if number > last_num:
        increase += 1
    last_num = number

print("Part 1:")
print(increase)

# Part 2
window_increase = 0

last_window = sum(sonar_numbers[0:3])
for i in range(1, len(sonar_numbers)-2):
    window = sum(sonar_numbers[i:i+3])
    if window > last_window:
        window_increase += 1
    last_window = window

print("Part 2:")
print(window_increase)