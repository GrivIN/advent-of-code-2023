import dataclasses
from pathlib import Path
from typing import Optional


class SourceDestinationMap:
    source_range_start: int
    source_range_end: int

    destination_range_start: int
    destination_range_end: int
    default: bool = False

    def __init__(
        self,
        source_range_start,
        destination_range_start,
        range_length=None,
        destination_range_end=None,
        source_range_end=None,
        default=False,
    ):
        self.destination_range_start = destination_range_start
        self.destination_range_end = (
            destination_range_end
            if destination_range_end is not None
            else destination_range_start + range_length - 1
        )
        self.source_range_start = source_range_start
        self.source_range_end = (
            source_range_end
            if source_range_end is not None
            else source_range_start + range_length - 1
        )
        self.default = default

    @property
    def source(self):
        return f"{self.source_range_start}-{self.source_range_end}"

    @property
    def destination(self):
        return f"{self.destination_range_start}-{self.destination_range_end}"

    def __repr__(self):
        return f"{self.source} -{'D' if self.default else '-'}-> {self.destination}"

    def __eq__(self, other):
        return (
            self.source_range_start == other.source_range_start
            and self.source_range_end == other.source_range_end
            and self.destination_range_start == other.destination_range_start
            and self.destination_range_end == other.destination_range_end
            and self.default == other.default
        )

    def is_in_source_range(self, value: int):
        return self.source_range_start <= value <= self.source_range_end

    def is_in_destination_range(self, value: int):
        return self.destination_range_start <= value <= self.destination_range_end

    def transform(self, value: int):
        if self.is_in_source_range(value):
            result = value - self.source_range_start + self.destination_range_start
            return result
        return None

    def reverse_transform(self, value: int):
        if self.is_in_destination_range(value):
            result = value - self.destination_range_start + self.source_range_start
            return result
        return None

    def split_source(self, source_range_start, source_range_end):
        possible_source_range_start = max(source_range_start, self.source_range_start)
        possible_source_range_end = min(source_range_end, self.source_range_end)

        # outside of current range
        if (
            possible_source_range_start > self.source_range_end
            or possible_source_range_end < self.source_range_start
        ):
            # no split
            yield self
        elif (
            source_range_start <= self.source_range_start
            and source_range_end >= self.source_range_end
        ):
            # same range
            yield self
        elif source_range_start <= self.source_range_start:
            yield SourceDestinationMap(  # new
                source_range_start=self.source_range_start,
                destination_range_start=self.destination_range_start,
                source_range_end=source_range_end,
                destination_range_end=self.transform(source_range_end),
                default=self.default,
            )
            yield SourceDestinationMap(  # old
                source_range_start=source_range_end + 1,
                destination_range_start=self.transform(source_range_end + 1),
                source_range_end=self.source_range_end,
                destination_range_end=self.destination_range_end,
                default=self.default,
            )
            # split by two
        elif source_range_end >= self.source_range_end:
            # split by two
            yield SourceDestinationMap(  # old
                source_range_start=self.source_range_start,
                destination_range_start=self.destination_range_start,
                source_range_end=source_range_start - 1,
                destination_range_end=self.transform(source_range_start - 1),
                default=self.default,
            )
            yield SourceDestinationMap(  # new
                source_range_start=source_range_start,
                destination_range_start=self.transform(source_range_start),
                source_range_end=self.source_range_end,
                destination_range_end=self.destination_range_end,
                default=self.default,
            )
        else:
            # split by three
            yield SourceDestinationMap(  # old
                source_range_start=self.source_range_start,
                destination_range_start=self.destination_range_start,
                source_range_end=source_range_start - 1,
                destination_range_end=self.transform(source_range_start - 1),
                default=self.default,
            )
            yield SourceDestinationMap(  # new
                source_range_start=source_range_start,
                destination_range_start=self.transform(source_range_start),
                source_range_end=source_range_end,
                destination_range_end=self.transform(source_range_end),
                default=self.default,
            )
            yield SourceDestinationMap(  # new
                source_range_start=source_range_end + 1,
                destination_range_start=self.transform(source_range_end + 1),
                source_range_end=self.source_range_end,
                destination_range_end=self.destination_range_end,
                default=self.default,
            )

    def split_destination(self, destination_range_start, destination_range_end):
        possible_destination_range_start = max(
            destination_range_start, self.destination_range_start
        )
        possible_destination_range_end = min(
            destination_range_end, self.destination_range_end
        )

        if (
            possible_destination_range_start > self.destination_range_end
            or possible_destination_range_end < self.destination_range_start
        ):
            yield self
        elif (
            destination_range_start <= self.destination_range_start
            and destination_range_end >= self.destination_range_end
        ):
            yield self
        elif destination_range_start <= self.destination_range_start:
            # split by two
            yield SourceDestinationMap(  # new
                source_range_start=self.source_range_start,
                destination_range_start=self.destination_range_start,
                source_range_end=self.reverse_transform(destination_range_end),
                destination_range_end=destination_range_end,
                default=self.default,
            )
            yield SourceDestinationMap(  # old
                source_range_start=self.reverse_transform(destination_range_end + 1),
                destination_range_start=destination_range_end + 1,
                source_range_end=self.source_range_end,
                destination_range_end=self.destination_range_end,
                default=self.default,
            )
        elif destination_range_end >= self.destination_range_end:
            # split by two
            yield SourceDestinationMap(  # old
                source_range_start=self.source_range_start,
                destination_range_start=self.destination_range_start,
                source_range_end=self.reverse_transform(destination_range_start - 1),
                destination_range_end=destination_range_start - 1,
                default=self.default,
            )
            yield SourceDestinationMap(  # new
                source_range_start=self.reverse_transform(destination_range_start),
                destination_range_start=destination_range_start,
                source_range_end=self.source_range_end,
                destination_range_end=self.destination_range_end,
                default=self.default,
            )
        else:
            # split by three
            yield SourceDestinationMap(  # old
                source_range_start=self.source_range_start,
                destination_range_start=self.destination_range_start,
                source_range_end=self.reverse_transform(destination_range_start - 1),
                destination_range_end=destination_range_start - 1,
                default=self.default,
            )
            yield SourceDestinationMap(  # new
                source_range_start=self.reverse_transform(destination_range_start),
                destination_range_start=destination_range_start,
                source_range_end=self.reverse_transform(destination_range_end),
                destination_range_end=destination_range_end,
                default=self.default,
            )
            yield SourceDestinationMap(  # new
                source_range_start=self.reverse_transform(destination_range_start + 1),
                destination_range_start=destination_range_start + 1,
                source_range_end=self.source_range_end,
                destination_range_end=self.destination_range_end,
                default=self.default,
            )

    def insert(self, other: "SourceDestinationMap"):
        if (
            other.source_range_start > self.source_range_end
            or other.source_range_end < self.source_range_start
        ):
            yield self
        elif (
            other.source_range_start <= self.source_range_start
            and other.source_range_end >= self.source_range_end
        ):
            yield SourceDestinationMap(
                source_range_start=self.source_range_start,
                destination_range_start=other.transform(self.source_range_start),
                source_range_end=self.source_range_end,
                destination_range_end=other.transform(self.source_range_end),
            )
        elif other.source_range_start <= self.source_range_start:
            yield SourceDestinationMap(  # new
                source_range_start=self.source_range_start,
                destination_range_start=other.transform(self.source_range_start),
                source_range_end=other.source_range_end,
                destination_range_end=other.destination_range_end,
            )
            yield SourceDestinationMap(  # old
                source_range_start=other.source_range_end + 1,
                destination_range_start=self.transform(other.source_range_end + 1),
                source_range_end=self.source_range_end,
                destination_range_end=self.destination_range_end,
                default=self.default,
            )
        elif other.source_range_end >= self.source_range_end:
            yield SourceDestinationMap(  # old
                source_range_start=self.source_range_start,
                destination_range_start=self.destination_range_start,
                source_range_end=other.source_range_start - 1,
                destination_range_end=self.transform(other.source_range_start - 1),
                default=self.default,
            )
            yield SourceDestinationMap(  # new
                source_range_start=other.source_range_start,
                destination_range_start=other.destination_range_start,
                source_range_end=self.source_range_end,
                destination_range_end=other.transform(self.source_range_end),
            )
        else:
            # split by three
            yield SourceDestinationMap(  # old
                source_range_start=self.source_range_start,
                destination_range_start=self.destination_range_start,
                source_range_end=other.source_range_start - 1,
                destination_range_end=self.transform(other.source_range_start - 1),
                default=self.default,
            )
            yield SourceDestinationMap(  # new
                source_range_start=other.source_range_start,
                destination_range_start=other.destination_range_start,
                source_range_end=other.source_range_end,
                destination_range_end=other.destination_range_end,
            )
            yield SourceDestinationMap(  # old
                source_range_start=other.source_range_end + 1,
                destination_range_start=self.transform(other.source_range_end + 1),
                source_range_end=self.source_range_end,
                destination_range_end=self.destination_range_end,
                default=self.default,
            )


@dataclasses.dataclass
class Map:
    name: str
    source_destination_maps: list[SourceDestinationMap] = dataclasses.field(
        default_factory=lambda: [
            SourceDestinationMap(0, 0, 9_999_999_999, default=True)
        ]
    )
    _traverse: Optional[dict[str, SourceDestinationMap]] = None

    def traverse(self, source: str):
        if self._traverse is None:
            self._traverse = {
                f"{source_destination_map.destination}": source_destination_map
                for source_destination_map in self.source_destination_maps
            }
        return self._traverse.get(source)

    def add(self, new_source_destination_map: SourceDestinationMap):
        new_map = []
        for source_destination_map in self.source_destination_maps:
            new_map.extend(source_destination_map.insert(new_source_destination_map))
        self.source_destination_maps = new_map

    def split_source(self, source_range_start, source_range_end):
        new_map = []
        for source_destination_map in self.source_destination_maps:
            gen = list(
                source_destination_map.split_source(
                    source_range_start, source_range_end
                )
            )
            new_map.extend(gen)
        self.source_destination_maps = new_map

    def split_destination(self, destination_range_start, destination_range_end):
        new_map = []
        for source_destination_map in self.source_destination_maps:
            gen = list(
                source_destination_map.split_destination(
                    destination_range_start, destination_range_end
                )
            )
            new_map.extend(gen)
        self.source_destination_maps = new_map


def fill_maps(
    seed_to_soil_map: Map,
    soil_to_fertilizer_map: Map,
    fertilizer_to_water_map: Map,
    water_to_light_map: Map,
    light_to_temperature_map: Map,
    temperature_to_humidity_map: Map,
    humidity_to_plant_map: Map,
    humidity_to_location_map: Map,
):
    current_map = None
    while True:
        line = yield
        if ":" in line:
            section_name = line.split(":", 1)[0]
            match section_name:
                case "seed-to-soil map":
                    current_map = seed_to_soil_map
                case "soil-to-fertilizer map":
                    current_map = soil_to_fertilizer_map
                case "fertilizer-to-water map":
                    current_map = fertilizer_to_water_map
                case "water-to-light map":
                    current_map = water_to_light_map
                case "light-to-temperature map":
                    current_map = light_to_temperature_map
                case "temperature-to-humidity map":
                    current_map = temperature_to_humidity_map
                case "humidity-to-plant map":
                    current_map = humidity_to_plant_map
                case "humidity-to-location map":
                    current_map = humidity_to_location_map
                case _:
                    raise ValueError(f"Unknown section {section_name}")
            continue
        if not line.strip():
            continue
        destination_range_start, source_range_start, range_length = line.split(" ", 3)
        mapping = SourceDestinationMap(
            *map(int, [source_range_start, destination_range_start, range_length])
        )
        current_map.add(mapping)


def seeds_range(seeds: list[int]):
    for start_idx in range(0, len(seeds), 2):
        start = seeds[start_idx]
        size = seeds[start_idx + 1]
        yield start, size


def sync(left: Map, right: Map):
    for mmap in left.source_destination_maps:
        right.split_source(mmap.destination_range_start, mmap.destination_range_end)
    for mmap in right.source_destination_maps:
        left.split_destination(mmap.source_range_start, mmap.source_range_end)


def main():
    current_dir = Path(__file__).parent.absolute()
    summary = 0

    seed_to_soil_map = Map("soil")  # seed-to-
    soil_to_fertilizer_map = Map("fertilizer")  # soil-to-
    fertilizer_to_water_map = Map("water")  # fertilizer-to-
    water_to_light_map = Map("light")  # water-to-
    light_to_temperature_map = Map("temperature")  # light-to-
    temperature_to_humidity_map = Map("humidity")  # temperature-to-
    humidity_to_plant_map = Map("plant")  # humidity-to-
    humidity_to_location_map = Map("location")  # humidity-to-

    with open(current_dir / "data.txt") as data_file:
        seeds: list[int] = list(
            map(int, data_file.readline().split(":", 1)[1].strip(" ").split(" "))
        )
        map_filler = fill_maps(
            seed_to_soil_map,
            soil_to_fertilizer_map,
            fertilizer_to_water_map,
            water_to_light_map,
            light_to_temperature_map,
            temperature_to_humidity_map,
            humidity_to_plant_map,
            humidity_to_location_map,
        )
        next(map_filler)
        for line in data_file:
            map_filler.send(line)

    seed_map = Map("seed")
    # part 1
    # for seed in seeds:
    #     seed_map.add(SourceDestinationMap(seed, seed, 1))
    # part 2
    for seed, size in seeds_range(seeds):
        seed_map.add(SourceDestinationMap(seed, seed, size))

    sync(seed_map, seed_to_soil_map)
    sync(seed_to_soil_map, soil_to_fertilizer_map)
    sync(soil_to_fertilizer_map, fertilizer_to_water_map)
    sync(fertilizer_to_water_map, water_to_light_map)
    sync(water_to_light_map, light_to_temperature_map)
    sync(light_to_temperature_map, temperature_to_humidity_map)
    sync(temperature_to_humidity_map, humidity_to_location_map)
    sync(light_to_temperature_map, temperature_to_humidity_map)
    sync(water_to_light_map, light_to_temperature_map)
    sync(fertilizer_to_water_map, water_to_light_map)
    sync(soil_to_fertilizer_map, fertilizer_to_water_map)
    sync(seed_to_soil_map, soil_to_fertilizer_map)
    sync(seed_map, seed_to_soil_map)

    candidates = []
    # traverse
    for location in humidity_to_location_map.source_destination_maps:
        temperature = temperature_to_humidity_map.traverse(
            location.source if location else ""
        )
        light = light_to_temperature_map.traverse(
            temperature.source if temperature else ""
        )
        water = water_to_light_map.traverse(light.source if light else "")
        fertilizer = fertilizer_to_water_map.traverse(water.source if water else "")
        soil = soil_to_fertilizer_map.traverse(fertilizer.source if fertilizer else "")
        seed = seed_to_soil_map.traverse(soil.source if soil else "")
        input_seed = seed_map.traverse(seed.source if seed else "")
        if input_seed is not None and not input_seed.default:
            candidates.append(
                location.destination_range_start,
            )
    summary = sorted(candidates)[0]
    # part 1
    # assert summary == 379811651
    # part 2
    # assert summary == 27992443
    return summary


if __name__ == "__main__":
    print(main())
