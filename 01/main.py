from pathlib import Path

MAPPING = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]
SHORT_MAPPING = {
    # short mapping, translates 2 letters for digit name to digit
    value[0:2]: str(index)
    for index, value in enumerate(MAPPING)
}


def mapping(line, start, stop, step):
    # yield digit from its name or itself (if digit)
    for ix in range(start, stop, step):
        if any(line[ix:].startswith(x) for x in MAPPING):
            yield SHORT_MAPPING[line[ix : ix + 2]]
            break
        if line[ix].isdigit():
            yield line[ix]
            break


def fst_lst_oo(line):
    # first digit, last digit, default 00
    length = len(line) - 1
    yield from mapping(line, 0, length, 1)
    yield from mapping(line, length, -1, -1)
    yield from "00"


def summarize(line):
    digits = fst_lst_oo(line)
    xx = next(digits) + next(digits)
    return int(xx)


def main():
    current_dir = Path(__file__).parent.absolute()
    with open(current_dir / "data.txt") as data_file:
        return sum(map(summarize, data_file))


if __name__ == "__main__":
    print(main())

    import timeit

    t = timeit.Timer("main()", setup="from __main__ import main")
    print(sorted(t.repeat(3, 1000)))
