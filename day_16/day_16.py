from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from math import prod
from typing import Union


with open("day_16/test.txt") as puzzle_input:
    transmission_hex = puzzle_input.readline().strip()


def zeroes_to_prepend(hex_string: str) -> int:
    counter = 0
    for hex in hex_string:
        if hex == "0":
            counter += 4
        else:
            bits = len(bin(int(hex, 16))[2:])
            counter += 4 - bits
            return counter


bits = bin(int(transmission_hex, 16))[2:]
bits = ("0" * zeroes_to_prepend(transmission_hex)) + bits
bits = bits.rstrip("0")


class PacketType(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    VALUE = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL = 7


@dataclass
class Transmission:
    version: int
    packet_type: PacketType

    @staticmethod
    def from_raw_transmission(bits: str) -> Transmission:
        transmission, remaining = Transmission.from_bits(bits)
        if len(remaining) != 0:
            raise RuntimeError("Remaining bits!")
        return transmission

    @staticmethod
    def from_bits(bits: str) -> tuple[Union[OperatorTransmission, LiteralTransmission], str]:
        version_bits, bits = bits[:3], bits[3:]
        version = int(version_bits, 2)

        type_bits, bits = bits[:3], bits[3:]
        packet_type_number = int(type_bits, 2)
        packet_type = PacketType(packet_type_number)

        if packet_type == PacketType.VALUE:
            return LiteralTransmission.from_bits(version, packet_type, bits)
        else:
            return OperatorTransmission.from_bits(version, packet_type, bits)

    @abstractmethod
    def get_version_sum(self) -> int:
        raise NotImplemented()

    @abstractmethod
    def get_value(self) -> int:
        raise NotImplemented()


@dataclass
class LiteralTransmission(Transmission):
    data: int

    def get_version_sum(self) -> int:
        return self.version

    def get_value(self) -> int:
        return self.data

    @staticmethod
    def read_bits(bits: str) -> tuple[int, str]:
        chunk = bits[:5]
        bits = bits[5:]
        final_bits = []

        while True:
            if chunk[0] == "0":
                final_bits.append(chunk[1:])
                break

            final_bits.append(chunk[1:])
            chunk = bits[:5]
            bits = bits[5:]

        number_bits = "".join(final_bits)
        return (int(number_bits, 2), bits)

    @staticmethod
    def from_bits(
        version: int, packet_type: int, bits: str
    ) -> tuple[LiteralTransmission, str]:
        number, remaining = LiteralTransmission.read_bits(bits)
        return (LiteralTransmission(version, packet_type, number), remaining)


class LengthType(Enum):
    BITS = auto()
    NUMBER = auto()

    @staticmethod
    def get_length_type(bit: str) -> LengthType:
        if bit == "1":
            return LengthType.NUMBER
        return LengthType.BITS


@dataclass
class OperatorTransmission(Transmission):
    length_type: LengthType
    length: int
    children: list[Transmission]

    def get_version_sum(self) -> int:
        child_versions = sum([child.get_version_sum() for child in self.children])
        return self.version + child_versions

    def get_value(self) -> int:
        match self.packet_type:
            case PacketType.SUM:
                return sum([child.get_value() for child in self.children])
            case PacketType.PRODUCT:
                return prod([child.get_value() for child in self.children])
            case PacketType.MINIMUM:
                return min([child.get_value() for child in self.children])
            case PacketType.MAXIMUM:
                return max([child.get_value() for child in self.children])
            case PacketType.GREATER_THAN:
                first = self.children[0].get_value()
                second = self.children[1].get_value()
                return 1 if first > second else 0
            case PacketType.LESS_THAN:
                first = self.children[0].get_value()
                second = self.children[1].get_value()
                return 1 if first < second else 0
            case PacketType.EQUAL:
                first = self.children[0].get_value()
                second = self.children[1].get_value()
                return 1 if first == second else 0
            case _:
                raise RuntimeError("Invalid packet type!")

    @staticmethod
    def from_bits(version: int, packet_type: int, bits: str) -> tuple[Transmission, str]:
        length_type_bit = bits[:1]
        bits = bits[1:]
        length_type = LengthType.get_length_type(length_type_bit)

        if length_type == LengthType.NUMBER:
            length_bits = bits[:11]
            bits = bits[11:]
        else:
            length_bits = bits[:15]
            bits = bits[15:]

        length = int(length_bits, 2)

        children = []

        rest: str
        if length_type == LengthType.NUMBER:
            rest = bits
            for _ in range(length):
                child, rest = Transmission.from_bits(rest)
                children.append(child)

        else:
            current, rest = bits[:length], bits[length:]
            while len(current) != 0:
                child, current = Transmission.from_bits(current)
                children.append(child)

        return (OperatorTransmission(version, packet_type, length_type, length, children), rest)

transmission = Transmission.from_raw_transmission(bits)

print("Part 1:")
print(transmission.get_version_sum())

# Part 2

print("Part 2:")
print(transmission.get_value())