import copy
import itertools


def get_input() -> tuple[list[int], list[list[int]]]:
    with open("day_20/input.txt") as file:
        raw_algo = file.readline()
        file.readline()
        raw_image = file.readlines()

    algo = list(map(lambda x: 0 if x == "." else 1, raw_algo.strip()))

    pixels = []
    for raw_line in raw_image:
        line = raw_line.strip()
        pixels.append(list(map(lambda x: 0 if x == "." else 1, line)))

    return algo, pixels


def enhance_image(image_input: list[list[int]], algo: list[int], iterations: int) -> list[list[int]]:
    for i in range(1, iterations+1):
        filler = 1 if algo[0] == 1 and algo[-1] == 0 and not i % 2 else 0
        image_input = pad(image_input, filler)
        image_input = enhance_image_step(image_input, algo, filler)
    return image_input


def enhance_image_step(image: list[list[int]], algo: list[int], filler: int) -> list[list[int]]:
    old_image = copy.deepcopy(image)
    for y, x in itertools.product(range(len(image)), range(len(image))):
        location = []
        for j, i in itertools.product(range(-1, 2), range(-1, 2)):
            try:
                location.append(old_image[y+j][x+i])
            except IndexError:
                location.append(filler)
        index = int("".join(str(x) for x in location), 2)
        image[y][x] = algo[index]
    return image


def pad(image_input: list[list[int]], padding: int) -> list[list[int]]:
    for y in range(len(image_input)):
        image_input[y].insert(0, padding)
        image_input[y].append(padding)

    current_size = len(image_input[0])
    image_input.insert(0, [padding for _ in range(current_size)])
    image_input.append([padding for _ in range(current_size)])
    return image_input


def output(image: list[list[int]]) -> None:
    for line in image:
        print("".join("." if x == 0 else "#" for x in line))


def illuminated(image: list[list[int]]) -> int:
    return sum(map(sum, image))


algo, image = get_input()

print("Part 1:")
pixels = enhance_image(copy.deepcopy(image), algo, 2)
print(illuminated(pixels))
print("Part 2:")
pixels = enhance_image(copy.deepcopy(image), algo, 50)
print(illuminated(pixels))
