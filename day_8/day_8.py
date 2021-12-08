segments = []
outputs = []
with open("day_8/input.txt") as puzzle_input:
    for line in puzzle_input.readlines():
        left, right = line.strip().split(" | ", 2)
        segments.append(left.split(" "))
        outputs.append(right.split(" "))

output_lengths = []
for output in outputs:
    output_lengths.append(list(map(len, output)))

known_numbers = 0
for output_length in output_lengths:
    for length in output_length:
        if length == 2 or length == 3 or length == 4 or length == 7:
            known_numbers += 1

print("Part 1")
print(known_numbers)

# Part 2

def get_positions(active_wires: list[str]) -> dict[set, int]:
    # Get the known digits
    sorted_wires = sorted(active_wires, key=len)
    sorted_wires_set = list(map(frozenset, sorted_wires))
    one = sorted_wires_set[0]
    seven = sorted_wires_set[1]
    four = sorted_wires_set[2]
    eight = sorted_wires_set[9]
    
    # seven minus one is the top wire
    top = (one ^ seven)

    # find nine
    nine = frozenset()
    for remaining_wire in sorted_wires_set[3:9]:
        if len(remaining_wire) != 6:
            continue
        if len(remaining_wire - four) == 2:
            nine = remaining_wire
            break

    bottom_left = eight - nine

    # find three
    three = frozenset()
    for remaining_wire in sorted_wires_set[3:7]:
        if len(remaining_wire) != 5:
            continue
        if len(remaining_wire - seven) == 2:
            three = remaining_wire
            break

    # find the 5
    five = frozenset()
    for remaining_wire in sorted_wires_set[3:7]:
        if len(remaining_wire) != 5:
            continue
        if len(remaining_wire - nine) == 0 and remaining_wire != three:
            five = remaining_wire
            break

    # find the six
    six = frozenset()
    for remaining_wire in sorted_wires_set[3:9]:
        if len(remaining_wire) != 6:
            continue
        if five.union(bottom_left) == remaining_wire:
            six = remaining_wire
    if len(six) == 0:
        raise RuntimeError("Something went wrong")

    # find zero
    zero = frozenset()
    for remaining_wire in sorted_wires_set[3:9]:
        if len(remaining_wire) != 6:
            continue
        if remaining_wire != nine and remaining_wire != six:
            zero = remaining_wire
            break

    top_right = eight - six
    middle = eight - zero
    bottom = eight - four.union(top, bottom_left)

    # find the two
    two = frozenset()
    for remaining_wire in sorted_wires_set[3:7]:
        if len(remaining_wire) != 5:
            continue
        if top.union(top_right, middle, bottom, bottom_left) == remaining_wire:
            two = remaining_wire
    if len(two) == 0:
        raise RuntimeError("Something went wrong")

    return {
        zero: 0,
        one: 1,
        two: 2,
        three: 3,
        four: 4,
        five: 5,
        six: 6,
        seven: 7,
        eight: 8,
        nine: 9,
    }


total = 0
for segment, output in zip(segments, outputs):
    wire_mapping = get_positions(segment)
    numbers = []
    for digit in output:
        numbers.append(wire_mapping[frozenset(digit)])
    total += int("".join([str(number) for number in numbers]))

print(total)
