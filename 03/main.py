import dataclasses
import string
from collections import defaultdict
from functools import partial
from pathlib import Path
from typing import Generator, Iterable, Optional


@dataclasses.dataclass(eq=True, frozen=True)
class Position:
    row: int
    col: int


@dataclasses.dataclass
class Symbol:
    position: Position
    char: str


@dataclasses.dataclass
class Number:
    row: int
    cols: list[int] = dataclasses.field(default_factory=list)
    value: str = dataclasses.field(default_factory=str)

    @property
    def adjacents(self) -> list[Position]:
        col_wide = [self.cols[0] - 1, *self.cols, self.cols[-1] + 1]
        return [
            *[Position(self.row - 1, col) for col in col_wide],
            Position(self.row, self.cols[0] - 1),
            Position(self.row, self.cols[-1] + 1),
            *[Position(self.row + 1, col) for col in col_wide],
        ]

    @property
    def numeric(self) -> int:
        return int(self.value)

    def append(self, col: int, char: str):
        self.cols.append(col)
        self.value += char

    def __bool__(self) -> bool:
        return bool(self.value)


def get_symbols(filename: Path) -> Generator[Symbol, None, None]:
    # use separate file cursors
    with open(filename) as data_file:
        for row, line in enumerate(data_file):
            for col, char in enumerate(line):
                if char in string.digits + ".\n":
                    continue
                yield Symbol(Position(row, col), char)


def get_numbers(filename: Path) -> Generator[Number, None, None]:
    # use separate file cursors
    with open(filename) as data_file:
        for row, line in enumerate(data_file):
            number = Number(row)
            for col, char in enumerate(line):
                if char in string.digits:
                    number.append(col, char)
                    continue
                if number:
                    yield number
                number = Number(row)


def find_adjacent_symbols(
    number: Number,
    symbols: dict[Position, Symbol],
) -> Optional[Symbol]:
    for adjacent in number.adjacents:
        if adjacent in symbols:
            return symbols[adjacent]
    return None


def get_numbers_around_gears(
    numbers: Iterable[Number],
    gear_symbols: dict[Position, Symbol],
) -> Iterable[list[Number, Number]]:
    gear_numbers: dict[Position, list[Number]] = defaultdict(list)
    for number in numbers:
        adjacent_symbol = find_adjacent_symbols(number, gear_symbols)
        if adjacent_symbol:
            gear_numbers[adjacent_symbol.position].append(number)
    gear_number_pairs = filter(lambda values: len(values) == 2, gear_numbers.values())
    return gear_number_pairs


def part1(
    symbols: Iterable[Symbol],
    numbers: Iterable[Number],
) -> int:
    all_symbols = {symbol.position: symbol for symbol in symbols}
    adjacent_numbers = filter(
        partial(find_adjacent_symbols, symbols=all_symbols), numbers
    )
    summary = sum(number.numeric for number in adjacent_numbers)
    return summary


def part2(symbols: Iterable[Symbol], numbers: Iterable[Number]) -> int:
    gear_symbols = {
        symbol.position: symbol
        for symbol in filter(lambda symbol: symbol.char == "*", symbols)
    }
    gear_number_pairs = get_numbers_around_gears(numbers, gear_symbols)
    gear_number_products = map(
        lambda values: values[0].numeric * values[1].numeric, gear_number_pairs
    )
    summary = sum(gear_number_products)
    assert summary == 84900879, summary
    return summary


def main():
    filename = Path(__file__).parent.absolute() / "data.txt"
    symbols = get_symbols(filename)
    numbers = get_numbers(filename)
    # summary = part1(symbols, numbers)
    summary = part2(symbols, numbers)
    return summary


if __name__ == "__main__":
    print(main())

    # import timeit
    # t = timeit.Timer("main()", setup="from __main__ import main")
    # print(sorted(t.repeat(3, 1000)))
