from typing import List, NamedTuple

class Order(NamedTuple):
    command: str
    amount: int

orders: List[Order] = []
with open("day_2/input.txt") as puzzle_input:
    for line in puzzle_input.readlines():
        line = line.split()
        orders.append(Order(line[0], int(line[1])))

horizontal = 0
vertical = 0

order: Order
for order in orders:
    if order.command == "forward":
        horizontal += order.amount
    elif order.command == "down":
        vertical += order.amount
    elif order.command == "up":
        vertical -= order.amount
    else:
        RuntimeError(f"Unhandled command: {order.command}")

print("Part 1:")
print(horizontal * vertical)

# Part 2

aim = 0
horizontal = 0
vertical = 0

for order in orders:
    if order.command == "down":
        aim += order.amount
    elif order.command == "up":
        aim -= order.amount
    elif order.command == "forward":
        horizontal += order.amount
        vertical += order.amount * aim

print("Part 2:")
print(horizontal * vertical)
