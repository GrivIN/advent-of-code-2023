
from prettytable import PrettyTable
from itertools import zip_longest


t = PrettyTable()
t.field_names = [
    "seed_map",
    "seed_to_soil_map",
    "soil_to_fertilizer_map",
    "fertilizer_to_water_map",
    "water_to_light_map",
    "light_to_temperature_map",
    "temperature_to_humidity_map",
    "humidity_to_location_map",
]
rows = zip_longest(
    seed_map.source_destination_maps,
    seed_to_soil_map.source_destination_maps,
    soil_to_fertilizer_map.source_destination_maps,
    fertilizer_to_water_map.source_destination_maps,
    water_to_light_map.source_destination_maps,
    light_to_temperature_map.source_destination_maps,
    temperature_to_humidity_map.source_destination_maps,
    humidity_to_location_map.source_destination_maps,
)
for row in rows:
    t.add_row(row)
print(t)
