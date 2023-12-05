import dataclasses
from functools import reduce
from pathlib import Path
from pprint import pprint
from time import sleep

CARD = (0, 8)
WINING = (10, 39)
NUMBERS = (42, 116)
NUMBER_WIDTH = 3


@dataclasses.dataclass
class Card:
    name: str
    numbers: list[int]
    winning_numbers: set[int]

    @property
    def matches(self):
        return list(filter(lambda x: x in self.winning_numbers, self.numbers))

    @property
    def matches_count(self):
        return len(self.matches)

    @property
    def value(self):
        return reduce(lambda x, _: 1 if x == 0 else x * 2, self.matches, 0)


def split(input_string, width=NUMBER_WIDTH):
    yield from (
        int(input_string[i : i + width]) for i in range(0, len(input_string), width)
    )


def part1(filename: Path):
    summary = 0
    with open(filename) as data_file:
        for line in data_file:
            card_name = line[CARD[0] : CARD[1]]
            winning_numbers = set(split(line[WINING[0] : WINING[1]]))
            numbers = list(split(line[NUMBERS[0] : NUMBERS[1]]))

            card = Card(card_name, numbers, winning_numbers)

            summary += card.value
    assert summary == 20107
    return summary


def part2(filename: Path):
    card_sets: list[list[Card]] = []
    summary = 0
    with open(filename) as data_file:
        for line in data_file:
            card_name = line[CARD[0] : CARD[1]]
            winning_numbers = set(split(line[WINING[0] : WINING[1]]))
            numbers = list(split(line[NUMBERS[0] : NUMBERS[1]]))

            card = Card(card_name, numbers, winning_numbers)
            card_sets.append([card])

    for set_idx, card_set in enumerate(card_sets):
        for card in card_set:
            if not card.matches_count:
                continue
            for shift in range(1, card.matches_count +1):
                card_sets[set_idx + shift].append(card_sets[set_idx + shift][0])

    summary = sum(map(len, card_sets))
    assert summary == 8172507
    return summary

def main():
    filename = Path(__file__).parent.absolute() / "data.txt"
    # summary = part1(filename)
    summary = part2(filename)
    return summary


if __name__ == "__main__":
    print(main())
