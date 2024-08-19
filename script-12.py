print("*" * 80)
print("Advent of Code 2022 - Day 12: Hill Climbing Algorithm")
print("*" * 80)
"""
--- Day 12: Hill Climbing Algorithm ---

You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^

In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?

"""

file = open("input-12.txt", "r")
lines = file.readlines()


def load_heightmap(lines):
    heightmap = []

    for i in range(0, len(lines)):
        line = []
        for j in range(0, len(lines[i].strip())):
            tile = {
                "height": int(lines[i][j], 36) - 10,
                "x": j,
                "y": i,
                "letter": lines[i][j],
            }
            if lines[i][j] == "S":
                tile["height"] = 0
            elif lines[i][j] == "E":
                tile["height"] = int("z", 36) - 10

            line.append(tile)
        heightmap.append(line)

    return heightmap


def find_path(heightmap, visited, ending_position):
    width = len(heightmap[0]) - 1
    height = len(heightmap) - 1
    end = False
    while not end:
        visited_length = len(visited)
        for _ in range(0, visited_length):
            tile = visited[0]
            x = tile["x"]
            y = tile["y"]
            steps = tile["steps"]

            if (  # RIGHT
                x < width
                and "steps" not in heightmap[y][x + 1]
                and heightmap[y][x + 1]["height"] - 1 <= tile["height"]
            ):
                if heightmap[y][x + 1]["letter"] == ending_position:
                    end = heightmap[y][x + 1]
                heightmap[y][x + 1]["steps"] = steps + 1
                visited.append(heightmap[y][x + 1])

            if (  # DOWN
                y < height
                and "steps" not in heightmap[y + 1][x]
                and heightmap[y + 1][x]["height"] - 1 <= tile["height"]
            ):
                if heightmap[y + 1][x]["letter"] == ending_position:
                    end = heightmap[y + 1][x]
                heightmap[y + 1][x]["steps"] = steps + 1
                visited.append(heightmap[y + 1][x])

            if (  # RIGHT
                x > 0
                and "steps" not in heightmap[y][x - 1]
                and heightmap[y][x - 1]["height"] - 1 <= tile["height"]
            ):
                if heightmap[y][x - 1]["letter"] == ending_position:
                    end = heightmap[y][x - 1]
                heightmap[y][x - 1]["steps"] = steps + 1
                visited.append(heightmap[y][x - 1])

            if (  # UP
                y > 0
                and "steps" not in heightmap[y - 1][x]
                and heightmap[y - 1][x]["height"] - 1 <= tile["height"]
            ):
                if heightmap[y - 1][x]["letter"] == ending_position:
                    end = heightmap[y - 1][x]
                heightmap[y - 1][x]["steps"] = steps + 1
                visited.append(heightmap[y - 1][x])

            visited = visited[1:]
            # print_heightmap()

        if len(visited) == 0:
            # print("No path found.")
            return None

    return end


def find_tiles(heightmap, letter):
    tiles = []
    for line in heightmap:
        for tile in line:
            if tile["letter"] == letter:
                tiles.append(tile)
    print(f"Found {len(tiles)} tiles with letter {letter}.")
    return tiles


def clear_heightmap(heightmap):
    for line in heightmap:
        for tile in line:
            if "steps" in tile:
                del tile["steps"]


def print_heightmap():
    for line in heightmap:
        msg = ""
        for tile in line:
            msg += tile["letter"].upper() if "steps" in tile else tile["letter"]
        print(msg)


heightmap = load_heightmap(lines)
visited = [find_tiles(heightmap, "S")[0]]
visited[0]["steps"] = 0
end = find_path(heightmap, visited, "E")

print(
    f"Fewest number of steps required to move from current position to the location with best signal is {end['steps']}"
)

"""
--- Part Two ---

As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^

This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?

"""


tiles = find_tiles(heightmap, "a")
nearest_end = None
for tile in tiles:
    clear_heightmap(heightmap)
    tile["steps"] = 0
    end = find_path(heightmap, [tile], "E")
    if not end:
        continue
    if not nearest_end or nearest_end > end["steps"]:
        nearest_end = end["steps"]

print(
    f"Fewest number of steps required to move starting point to any square with elevation 'a' is {nearest_end}"
)
print(f"Nothing {0}")

print("*" * 80)
