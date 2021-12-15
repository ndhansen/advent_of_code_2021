from typing import NamedTuple
from collections import defaultdict


class Pair(NamedTuple):
    left: str
    right: str


def insert_pairs_into_polymer(polymer: str, rules: dict[Pair, str]) -> str:
    new_polymer = list()

    for i in range(len(polymer) - 1):
        new_polymer.append(polymer[i])
        polymer_pair = Pair(polymer[i], polymer[i + 1])
        if polymer_pair in rules.keys():
            new_polymer.append(rules[polymer_pair])

    new_polymer.append(polymer[-1])
    return "".join(new_polymer)


def count_letters(line: str) -> dict[int, str]:
    counter: defaultdict[str, int] = defaultdict(int)
    for letter in line:
        counter[letter] += 1

    return {value: key for key, value in counter.items()}


insertion_rules: dict[Pair, str] = {}

with open("day_14/input.txt") as puzzle_input:
    original_polymer_template = puzzle_input.readline().strip()

    for line in puzzle_input.readlines():
        if line.strip() == "":
            continue

        pair, insertion = line.strip().split(" -> ", 2)
        insertion_rules[Pair(pair[0], pair[1])] = insertion

polymer_template = original_polymer_template
for step in range(10):
    polymer_template = insert_pairs_into_polymer(polymer_template, insertion_rules)

letters = count_letters(polymer_template)
letter_counts = sorted(letters.keys())
smallest = letter_counts[0]
largest = letter_counts[-1]

print("Part 1:")
print(largest - smallest)

# Part 2

polymer_template_pairs: defaultdict[Pair, int] = defaultdict(int)
polymer = original_polymer_template
start_end_pair = Pair(original_polymer_template[0], original_polymer_template[-1])
for i in range(len(polymer) - 1):
    polymer_template_pairs[Pair(polymer[i], polymer[i + 1])] += 1


def insert_into_polymer_pairs(
    pairs: defaultdict[Pair, int], rules: dict[Pair, str]
) -> defaultdict[Pair, int]:
    new_pairs: defaultdict[Pair, int] = defaultdict(int)

    for pair, count in pairs.items():
        if pair in rules:
            insert_character = rules[pair]
            new_pairs[Pair(pair.left, insert_character)] += count
            new_pairs[Pair(insert_character, pair.right)] += count
        else:
            new_pairs[pair] += count

    return new_pairs


def count_elements(pairs: dict[Pair, int], start_end_pair: Pair) -> dict[int, str]:
    counter: defaultdict[str, int] = defaultdict(int)

    # Handle first and last element
    counter[start_end_pair.left] += 1
    counter[start_end_pair.right] += 1

    for pair, count in pairs.items():
        counter[pair.left] += count
        counter[pair.right] += count

    for key in counter.keys():
        counter[key] = counter[key] // 2

    return {value: key for key, value in counter.items()}


for step in range(40):
    polymer_template_pairs = insert_into_polymer_pairs(
        polymer_template_pairs, insertion_rules
    )

letters = count_elements(polymer_template_pairs, start_end_pair)
letter_counts = sorted(letters.keys())
smallest = letter_counts[0]
largest = letter_counts[-1]

print("Part 2:")
print(largest - smallest)
