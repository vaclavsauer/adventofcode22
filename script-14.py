print("*" * 80)
print("Advent of Code 2022 - Day 14: Regolith Reservoir")
print("*" * 80)
"""
--- Day 14: Regolith Reservoir ---

The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the waterfall itself, and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will come in handy here. You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures made of rock.

Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path, where x represents distance to the right and y represents distance down. Each path appears as a single line of text in your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9

This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 through 498,6 and another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:


  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.

Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes to rest. A unit of sand is large enough to fill one tile of air in your scan.

A unit of sand always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move diagonally one step down and to the left. If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as long as it is able to do so, at each step trying to move down, then down-left, then down-right. If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.

So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.

The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.

After a total of five units of sand have come to rest, they form this pattern:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.

After a total of 22 units of sand:

......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.

Finally, only two more units of sand can possibly come to rest:

......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.

Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom, falling into the endless void. Just for fun, the path any new sand takes before falling forever is shown here with ~:

.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........

Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the abyss below?

"""

file = open("input-14.txt", "r")
lines = file.readlines()


def extend_cave(cave, width, height):
    current_height = len(cave)
    current_width = len(cave[0]) if cave else 0
    if current_height < height:
        if current_height < height:
            for i in range(current_height, height):
                cave.append(["."] * current_width)

    for row in cave:
        for i in range(current_width, width):
            row.append(".")

    return cave


def fill_rock_formation(cave, start, end):
    cave = extend_cave(cave, max(start[0], end[0]) + 1, max(start[1], end[1]) + 1)
    for i in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
        cave[i][start[0]] = "#"
    for i in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
        cave[start[1]][i] = "#"
    return cave


def print_cave(cave):
    for row in cave:
        print("".join(row))
    print("-" * len(cave[0]))


def load_cave(lines, add_bottom=False):
    cave = []
    for line in lines:
        rock_formations = line.split(" -> ")
        for i in range(0, len(rock_formations) - 1):
            first_formation = [
                int(coordinate) for coordinate in rock_formations[i].split(",")
            ]
            second_formation = [
                int(coordinate) for coordinate in rock_formations[i + 1].split(",")
            ]
            cave = fill_rock_formation(cave, first_formation, second_formation)
    if add_bottom:
        cave = fill_rock_formation(cave, [0, len(cave) + 1], [1000, len(cave) + 1])

    # print_cave(cave)
    return cave


def simulate_cave(cave):
    for i in range(0, len(cave)):
        for j in range(0, len(cave[0])):
            if cave[i][j] in [".", "#", "o"]:
                continue
            elif cave[i][j] == "O":
                if i == len(cave) - 1:
                    cave[i][j] = "."
                    return cave, True
                if cave[i + 1][j] == ".":
                    cave[i + 1][j] = "O"
                    cave[i][j] = "."
                elif cave[i + 1][j - 1] == ".":
                    cave[i + 1][j - 1] = "O"
                    cave[i][j] = "."
                elif cave[i + 1][j + 1] == ".":
                    cave[i + 1][j + 1] = "O"
                    cave[i][j] = "."
                else:
                    cave[i][j] = "o"
                    if i == 0 and j == 500:
                        return cave, True
                    cave[0][500] = "O"
                # print_cave(cave)
                continue

    return cave, False


def count_grains(cave):
    grains = 0
    for row in cave:
        for tile in row:
            if tile == "o":
                grains += 1
    return grains


cave = load_cave(lines)
cave[0][500] = "O"
settled = False

print_cave(cave)
while not settled:
    cave, settled = simulate_cave(cave)

print_cave(cave)
grains = count_grains(cave)

print(f"{grains} grains of sand fit into first cave system.")

"""

"""
cave = load_cave(lines, True)
cave[0][500] = "O"
settled = False

print_cave(cave)
while not settled:
    cave, settled = simulate_cave(cave)

print_cave(cave)
grains = count_grains(cave)

print(f"{grains} grains of sand fit into second cave system.")

print("*" * 80)
