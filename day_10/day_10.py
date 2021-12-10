lines = []
with open("day_10/input.txt") as puzzle_input:
    for line in puzzle_input.readlines():
        lines.append(line.strip())


points = {")": 3, "]": 57, "}": 1197, ">": 25137}
closing_bracket_pairs = {")": "(", "]": "[", "}": "{", ">": "<"}
opening_bracket_pairs = {value: key for key, value in closing_bracket_pairs.items()}
opening_brackets = {"(", "[", "{", "<"}
closing_brackets = {")", "]", "}", ">"}

score = 0
for line in lines:
    brackets = []
    for bracket in line:
        if bracket in opening_brackets:
            brackets.append(bracket)
        else:
            if brackets[-1] != closing_bracket_pairs[bracket]:
                score += points[bracket]
                break
            else:
                brackets.pop()

print("Part 1:")
print(score)

# Part 2

points = {")": 1, "]": 2, "}": 3, ">": 4}

remaining_brackets = []
for line in lines:
    brackets = []
    for bracket in line:
        if bracket in opening_brackets:
            brackets.append(bracket)
        else:
            if brackets[-1] != closing_bracket_pairs[bracket]:
                break
            else:
                brackets.pop()
    else:
        remaining_brackets.append([opening_bracket_pairs[x] for x in brackets[::-1]])


def calculate_score(brackets: list[str]) -> int:
    score = 0
    for bracket in brackets:
        score *= 5
        score += points[bracket]
    return score

scores = list(map(calculate_score, remaining_brackets))
scores.sort()
median = len(scores) // 2

print("Part 2:")
print(scores[median])
