from pathlib import Path

# only 12 red cubes, 13 green cubes, and 14 blue cubes
BLUE_ALLOWED = 14
RED_ALLOWED = 12
GREEN_ALLOWED = 13


class Game:
    game_number: int
    max_blue: int = 0
    max_red: int = 0
    max_green: int = 0

    @property
    def possible(self):
        return (
            self.max_blue <= BLUE_ALLOWED
            and self.max_red <= RED_ALLOWED
            and self.max_green <= GREEN_ALLOWED
        )

    @property
    def power(self):
        return self.max_blue * self.max_red * self.max_green

    def __set_game_number(self, name: str):
        game_number = int(name.split(" ", 1)[1])
        self.game_number = game_number

    def __set_game_sets(self, sets: str):
        self.sets = []
        for game_set in sets.split(";"):
            for cube in game_set.split(","):
                count, color = cube.strip().split(" ", 1)
                count = int(count)
                self.__set_max(color, count)

    def __set_max(self, color: str, count: int):
        current_count = getattr(self, f"max_{color}")
        if count > current_count:
            setattr(self, f"max_{color}", count)

    def __init__(self, name: str, sets: str):
        self.__set_game_number(name)
        self.__set_game_sets(sets)

    def __str__(self):
        return (
            f"Game {self.game_number}: POSSIBLE: {self.possible} POWER: {self.power}\n"
            f"Max Blue: {self.max_blue}/{BLUE_ALLOWED} Max Red: {self.max_red}/{RED_ALLOWED} Max Green: {self.max_green}/{GREEN_ALLOWED}"
        )


def main():
    current_dir = Path(__file__).parent.absolute()
    summary = 0
    with open(current_dir / "data.txt") as data_file:
        for line in data_file:
            game, all_game_sets = line.split(":", 1)
            game = Game(game, all_game_sets)
            summary += game.power
            # if game.possible:
            #     summary += game.game_number
            print(f"Summary: {summary}")


if __name__ == "__main__":
    print(main())

    # import timeit
    # t = timeit.Timer("main()", setup="from __main__ import main")
    # print(sorted(t.repeat(3, 1000)))
