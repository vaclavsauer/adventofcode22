import re
from pprint import pprint

print("*" * 80)
print("Advent of Code 2022 - Day 15: Beacon Exclusion Zone")
print("*" * 80)
"""
--- Day 15: Beacon Exclusion Zone ---

You feel the ground rumble again as the distress signal leads you to a large network of subterranean tunnels. You don't have time to search them all, but you don't need to: your pack contains a set of deployable sensors that you imagine were originally built to locate lost Elves.

The sensors aren't very powerful, but that's okay; your handheld device indicates that you're close enough to the source of the distress signal to use them. You pull the emergency sensor system out of your pack, hit the big button on top, and the sensors zoom off down the tunnels.

Once a sensor finds a spot it thinks will give it a good reading, it attaches itself to a hard surface and begins monitoring for the nearest signal source beacon. Sensors and beacons always exist at integer coordinates. Each sensor knows its own position and can determine the position of a beacon precisely; however, sensors can only lock on to the one beacon closest to the sensor as measured by the Manhattan distance. (There is never a tie where two beacons are the same distance to a sensor.)

It doesn't take long for the sensors to report back their positions and closest beacons (your puzzle input). For example:

Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3

So, consider the sensor at 2,18; the closest beacon to it is at -2,15. For the sensor at 9,16, the closest beacon to it is at 10,16.

Drawing sensors as S and beacons as B, the above arrangement of sensors and beacons looks like this:

               1    1    2    2
     0    5    0    5    0    5
 0 ....S.......................
 1 ......................S.....
 2 ...............S............
 3 ................SB..........
 4 ............................
 5 ............................
 6 ............................
 7 ..........S.......S.........
 8 ............................
 9 ............................
10 ....B.......................
11 ..S.........................
12 ............................
13 ............................
14 ..............S.......S.....
15 B...........................
16 ...........SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....

This isn't necessarily a comprehensive map of all beacons in the area, though. Because each sensor only identifies its closest beacon, if a sensor detects a beacon, you know there are no other beacons that close or closer to that sensor. There could still be beacons that just happen to not be the closest beacon to any sensor. Consider the sensor at 8,7:

               1    1    2    2
     0    5    0    5    0    5
-2 ..........#.................
-1 .........###................
 0 ....S...#####...............
 1 .......#######........S.....
 2 ......#########S............
 3 .....###########SB..........
 4 ....#############...........
 5 ...###############..........
 6 ..#################.........
 7 .#########S#######S#........
 8 ..#################.........
 9 ...###############..........
10 ....B############...........
11 ..S..###########............
12 ......#########.............
13 .......#######..............
14 ........#####.S.......S.....
15 B........###................
16 ..........#SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....

This sensor's closest beacon is at 2,10, and so you know there are no beacons that close or closer (in any positions marked #).

None of the detected beacons seem to be producing the distress signal, so you'll need to work out where the distress beacon is by working out where it isn't. For now, keep things simple by counting the positions where a beacon cannot possibly be along just a single row.

So, suppose you have an arrangement of beacons and sensors like in the example above and, just in the row where y=10, you'd like to count the number of positions a beacon cannot possibly exist. The coverage from all sensors near that row looks like this:

                 1    1    2    2
       0    5    0    5    0    5
 9 ...#########################...
10 ..####B######################..
11 .###S#############.###########.

In this example, in the row where y=10, there are 26 positions where a beacon cannot be present.

Consult the report from the sensors you just deployed. In the row where y=2000000, how many positions cannot contain a beacon?

"""

file = open("input-15.txt", "r")
lines = file.readlines()


def get_coorinates(lines):
    coordinates = []
    for line in lines:
        search = re.findall(r"(-?\d+)", line)
        search = [int(coordinate) for coordinate in search]
        coordinates.append(
            {
                "sensor": search[:2],
                "beacon": search[2:],
            }
        )
    return coordinates


def get_area_limits(coordinates):
    min_x = None
    max_x = None
    min_y = None
    max_y = None
    for coordinate in coordinates:
        current_min_x = min(coordinate["sensor"][0], coordinate["beacon"][0])
        current_max_x = max(coordinate["sensor"][0], coordinate["beacon"][0])
        current_min_y = min(coordinate["sensor"][1], coordinate["beacon"][1])
        current_max_y = max(coordinate["sensor"][1], coordinate["beacon"][1])
        min_x = min(min_x if min_x is not None else current_min_x, current_min_x)
        max_x = max(max_x if max_x is not None else current_max_x, current_max_x)
        min_y = min(min_y if min_y is not None else current_min_y, current_min_y)
        max_y = max(max_y if max_y is not None else current_max_y, current_max_y)
    return {"min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y}


def print_area(area, area_limits):
    print(
        "  ",
        "".join(
            [str(i % 10) for i in range(area_limits["min_x"], area_limits["max_x"] + 1)]
        ),
    )
    for i, line in enumerate(area):
        print(f"{i:2} {''.join(line)}")


def create_area(area_limits, coordinates):
    area = []
    print(area_limits)
    for _ in range(0, (area_limits["max_y"] - area_limits["min_y"] + 1)):
        area.append(["."] * (area_limits["max_x"] - area_limits["min_x"] + 1))
    for coordinate in coordinates:
        sensor = coordinate["sensor"]
        beacon = coordinate["beacon"]
        area[sensor[1] - area_limits["min_y"]][sensor[0] - area_limits["min_x"]] = "S"
        area[beacon[1] - area_limits["min_y"]][beacon[0] - area_limits["min_x"]] = "B"
    return area


def get_distance(point_1, point_2):
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])


def fill_area(area, area_limits, coordinates):
    for coordinate in coordinates:
        sensor_beacon_distance = get_distance(
            coordinate["sensor"], coordinate["beacon"]
        )
        normalised_sensor_coordinates = [
            coordinate["sensor"][0] - area_limits["min_x"],
            coordinate["sensor"][1] - area_limits["min_y"],
        ]
        for y, row in enumerate(area):
            for x, column in enumerate(area[y]):
                current_point_sensor_distance = get_distance(
                    normalised_sensor_coordinates, [x, y]
                )
                if (
                    current_point_sensor_distance <= sensor_beacon_distance
                    and area[y][x] not in "SB"
                ):
                    area[y][x] = "#"

    return area


def get_tiles_without_beacon(coordinates, area_limits, y_coordinate):
    y_coordinate = y_coordinate - area_limits["min_y"]
    tile_count = 0
    occupied_tiles = [False] * (area_limits["max_x"] - area_limits["min_x"] + 1)
    for i in range(area_limits["min_x"], area_limits["max_x"]):
        for coordinate in coordinates:
            sensor_to_beacon_distance = get_distance(
                coordinate["sensor"], coordinate["beacon"]
            )
            sensor_to_tile_distance = get_distance(
                coordinate["sensor"], [i, y_coordinate]
            )
            if sensor_to_beacon_distance >= sensor_to_tile_distance:
                occupied_tiles[i] = True

    for coordinate in coordinates:
        if coordinate["beacon"][1] == y_coordinate and (
            occupied_tiles[coordinate["beacon"][0] - area_limits["min_x"]] == True
        ):
            occupied_tiles[coordinate["beacon"][0] - area_limits["min_x"]] = False
    for tile in occupied_tiles:
        if tile == True:
            tile_count += 1

    return tile_count


coordinates = get_coorinates(lines)
area_limits = get_area_limits(coordinates)
# area = create_area(area_limits, coordinates)
# filled_area = fill_area(area, area_limits, coordinates)
tiles_without_beacon = get_tiles_without_beacon(coordinates, area_limits, 2000000)
# print_area(filled_area, area_limits)

pprint(coordinates)
print(area_limits)
print(f"{tiles_without_beacon} positions cannot contain a beacon.")

"""

"""
for line in lines:
    pass

print(f"Nothing {0}")

print("*" * 80)
