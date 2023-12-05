import dataclasses
from pathlib import Path
from pprint import pprint
from typing import Iterable
import numpy as np


@dataclasses.dataclass
class SourceDestinationMap:
    destination_range_start: int
    source_range_start: int
    range_length: int

    @property
    def source_range_end(self):
        return self.source_range_start + self.range_length

    def is_in_source_range(self, value: int):
        return self.source_range_start <= value < self.source_range_end

    def transform(self, value: int):
        if self.is_in_source_range(value):
            result = value - self.source_range_start + self.destination_range_start
            return result
        return None


@dataclasses.dataclass
class Map:
    name: str
    source_destination_maps: list[SourceDestinationMap] = dataclasses.field(
        default_factory=list
    )

    def add(self, source_destination_map: SourceDestinationMap):
        self.source_destination_maps.append(source_destination_map)
        self.source_destination_maps.sort(key=lambda x: x.source_range_start)

    def transform(self, value: int):
        for source_destination_map in self.source_destination_maps:
            transformed_value = source_destination_map.transform(value)
            if transformed_value is not None:
                return transformed_value
        return value


def part1(
    seeds: Iterable[int],
    seed_to_soil_map: Map,
    soil_to_fertilizer_map: Map,
    fertilizer_to_water_map: Map,
    water_to_light_map: Map,
    light_to_temperature_map: Map,
    temperature_to_humidity_map: Map,
    humidity_to_plant_map: Map,
    humidity_to_location_map: Map,
):
    min_location = None

    for seed in seeds:
        soil = seed_to_soil_map.transform(seed)
        fertilizer = soil_to_fertilizer_map.transform(soil)
        water = fertilizer_to_water_map.transform(fertilizer)
        light = water_to_light_map.transform(water)
        temperature = light_to_temperature_map.transform(light)
        humidity = temperature_to_humidity_map.transform(temperature)
        # plant = humidity_to_plant_map.transform(humidity)
        location = humidity_to_location_map.transform(humidity)
        if min_location is None or location < min_location:
            min_location = location

    summary = min_location

    return summary


def part2(
    seeds: Iterable[tuple[int, int]],
    seed_to_soil_map: Map,
    soil_to_fertilizer_map: Map,
    fertilizer_to_water_map: Map,
    water_to_light_map: Map,
    light_to_temperature_map: Map,
    temperature_to_humidity_map: Map,
    humidity_to_plant_map: Map,
    humidity_to_location_map: Map,
):

    for seed in seeds:
        seed_array = np.arange(seed[0], seed[1])
        print(seed_array)

    return 0

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
        mapping = SourceDestinationMap(*map(int, line.split(" ")))
        current_map.add(mapping)


def seeds_range(seeds: list[int]):
    for start_idx in range(0, len(seeds), 2):
        start = seeds[start_idx]
        size = seeds[start_idx + 1]
        for seed in range(start, start + size):
            yield start, size

def main():
    current_dir = Path(__file__).parent.absolute()
    summary = 0

    seed_to_soil_map = Map("seed-to-soil map")
    soil_to_fertilizer_map = Map("soil-to-fertilizer map")
    fertilizer_to_water_map = Map("fertilizer-to-water map")
    water_to_light_map = Map("water-to-light map")
    light_to_temperature_map = Map("light-to-temperature map")
    temperature_to_humidity_map = Map("temperature-to-humidity map")
    humidity_to_plant_map = Map("humidity-to-plant map")
    humidity_to_location_map = Map("humidity-to-location map")

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

    # summary = part1(
    #     seeds,
    #     seed_to_soil_map,
    #     soil_to_fertilizer_map,
    #     fertilizer_to_water_map,
    #     water_to_light_map,
    #     light_to_temperature_map,
    #     temperature_to_humidity_map,
    #     humidity_to_plant_map,
    #     humidity_to_location_map,
    # )
    # assert summary == 379811651

    seeds_2 = seeds_range(seeds)

    summary = part2(
        seeds_2,
        seed_to_soil_map,
        soil_to_fertilizer_map,
        fertilizer_to_water_map,
        water_to_light_map,
        light_to_temperature_map,
        temperature_to_humidity_map,
        humidity_to_plant_map,
        humidity_to_location_map,
    )
    return summary


if __name__ == "__main__":
    print(main())
