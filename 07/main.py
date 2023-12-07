from abc import ABC, abstractmethod
from collections import Counter
from pathlib import Path


class Card(ABC):
    representation: str

    @property
    @abstractmethod
    def value(self) -> int:
        ...

    @property
    def weight(self) -> str:
        return f"{self.value:x}"

    def __init__(self, representation: str):
        self.representation = representation

    def __str__(self) -> str:
        self.representation

    def __repr__(self) -> str:
        return self.representation


class CardRegular(Card):
    @property
    def value(self) -> int:
        if self.representation == "T":
            return 10
        elif self.representation == "J":
            return 11
        elif self.representation == "Q":
            return 12
        elif self.representation == "K":
            return 13
        elif self.representation == "A":
            return 14
        else:
            return int(self.representation)


class CardJoker(Card):
    @property
    def value(self) -> int:
        if self.representation == "T":
            return 10
        elif self.representation == "J":
            return 1
        elif self.representation == "Q":
            return 12
        elif self.representation == "K":
            return 13
        elif self.representation == "A":
            return 14
        else:
            return int(self.representation)


class Hand(ABC):
    cards: list[Card]
    bet: int

    @property
    @abstractmethod
    def value(self):
        ...

    @abstractmethod
    def __init__(self, cards: str, bet: str):
        ...

    @property
    def weight(self):
        weight = f"{self.value:x}" + "".join(map(lambda x: x.weight, self.cards))
        return weight

    @property
    def card_counts(self):
        return Counter(x.representation for x in self.cards)

    def card_counts_to_value(self, card_counts):
        if 5 in card_counts.values():
            # Five of a kind, where all five cards have the same label: AAAAA
            return 7
        elif 4 in card_counts.values():
            # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
            return 6
        elif 3 in card_counts.values() and 2 in card_counts.values():
            # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
            return 5
        elif 3 in card_counts.values():
            # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
            return 4
        elif 2 in card_counts.values() and len(card_counts) == 3:
            # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
            return 3
        elif 2 in card_counts.values():
            # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
            return 2
        # High card, where all cards' labels are distinct: 23456
        return 1

    def __str__(self):
        return "{} {} {}".format(
            self.weight, "".join(map(lambda x: x.weight, self.cards)), self.value
        )


class HandRegular(Hand):
    def __init__(self, cards: str, bet: str):
        self.cards = list(map(CardRegular, cards))
        self.bet = int(bet)

    @property
    def value(self):
        return self.card_counts_to_value(self.card_counts)


class HandJoker(Hand):
    def __init__(self, cards: str, bet: str):
        self.cards = list(map(CardJoker, cards))
        self.bet = int(bet)

    @property
    def value(self):
        card_counts_without_jokers = self.card_counts.copy()
        jokers_count = card_counts_without_jokers["J"]
        del card_counts_without_jokers["J"]

        try:
            most_common = card_counts_without_jokers.most_common(1)[0][0]
        except IndexError:
            most_common = "J"

        card_counts_without_jokers[most_common] += jokers_count
        return self.card_counts_to_value(card_counts_without_jokers)


def part1(filename: Path):
    hands = []
    with open(filename) as data_file:
        for line in data_file:
            cards, value = line.split(" ")
            hand = HandRegular(cards, value)
            hands.append(hand)
    return hands


def part2(filename: Path):
    hands = []
    with open(filename) as data_file:
        for line in data_file:
            cards, value = line.split(" ")
            hand = HandJoker(cards, value)
            hands.append(hand)
    return hands


def main():
    filename = Path(__file__).parent.absolute() / "data.txt"
    summary = 0
    # hands = part1(filename)
    hands = part2(filename)

    hands.sort(key=lambda x: x.weight, reverse=False)

    for weight, hand in enumerate(hands, start=1):
        summary += weight * hand.bet

    # part 1:
    # assert summary == 253603890
    # part 2:
    # assert summary == 253630098
    return summary


if __name__ == "__main__":
    print(main())
