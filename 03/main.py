from pathlib import Path

def main():
    current_dir = Path(__file__).parent.absolute()
    summary = 0
    with open(current_dir / "data.txt") as data_file:
        pass
    return summary


if __name__ == "__main__":
    print(main())

    # import timeit
    # t = timeit.Timer("main()", setup="from __main__ import main")
    # print(sorted(t.repeat(3, 1000)))
