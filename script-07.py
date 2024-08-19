import re
from pprint import pprint

print("*" * 80)
print("Advent of Code 2022 - No Space Left On Device")
print("*" * 80)
"""
--- Day 7: No Space Left On Device ---

You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

    cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
        cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
        cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
        cd / switches the current directory to the outermost directory, /.
    ls means list. It prints out all of the files and directories immediately contained by the current directory:
        123 abc means that the current directory contains a file named abc with size 123.
        dir xyz means that the current directory contains a directory named xyz.

Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

    The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
    The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
    Directory d has total size 24933642.
    As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.

To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?

"""

file = open("input-07.txt", "r")
lines = file.readlines()

current_path = []


def get_dir(files, path):
    dir = files
    for dir_name in path:
        for child_dir in dir["directories"]:
            if child_dir["name"] == dir_name:
                dir = child_dir
    return dir


def add_dir(root_dir, name):
    for dir in root_dir["directories"]:
        if dir["name"] == name:
            break
    else:
        root_dir["directories"].append(
            {
                "name": name,
                "type": "dir",
                "directories": [],
                "files": [],
            }
        )


def add_file(dir, file_name, file_size):
    for file in dir["files"]:
        if file["name"] == file_name:
            break
    else:
        dir["files"].append(
            {
                "name": file_name,
                "size": file_size,
            }
        )


def load_directories(lines):

    files = {
        "name": "/",
        "type": "dir",
        "directories": [],
        "files": [],
    }

    for line in lines:
        line = line.strip()
        if line == "$ cd /":
            current_path = []
        elif line == "$ cd ..":
            current_path = current_path[:-1]
        elif line.startswith("$ cd "):
            dir_name = line[5:]
            dir = get_dir(files, current_path)
            add_dir(dir, dir_name)
            current_path.append(dir_name)
        elif re.search("^(\d*)", line)[0] != "":
            file_size, file_name = line.split(" ")
            dir = get_dir(files, current_path)
            add_file(dir, file_name, file_size)
    return files


def calculate_sizes(directory):
    directory_sizes = 0
    file_sizes = 0
    for subdirectory in directory["directories"]:
        calculate_sizes(subdirectory)
        directory_sizes += subdirectory["size"]

    for file in directory["files"]:
        file_sizes += int(file["size"])

    directory["size"] = directory_sizes + file_sizes


def get_small_size(directory):
    small_size = 0
    for subdirectory in directory["directories"]:
        small_size += get_small_size(subdirectory)

    if directory["size"] < 100000:
        small_size += directory["size"]

    return small_size


files = load_directories(lines)
calculate_sizes(files)
small_size = get_small_size(files)

# pprint(files)

print(f"Sum of their total sizes is {small_size}.")

"""
--- Part Two ---

Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70 000 000. To run the update, you need unused space of at least 30 000 000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48 381 165; this means that the size of the unused space must currently be 21 618 835, which isn't quite the 30000000 required by the update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

    Delete directory e, which would increase unused space by 584.
    Delete directory a, which would increase unused space by 94853.
    Delete directory d, which would increase unused space by 24933642.
    Delete directory /, which would increase unused space by 48381165.

Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?

"""


def find_smallest_directory_to_delete(directory, required_free_space):
    smallest_subdirectory = None
    for subdirectory in directory["directories"]:
        small_subdirectory = find_smallest_directory_to_delete(
            subdirectory, required_free_space
        )
        if small_subdirectory and (
            not smallest_subdirectory
            or small_subdirectory["size"] < smallest_subdirectory["size"]
        ):
            smallest_subdirectory = small_subdirectory

    if smallest_subdirectory and smallest_subdirectory["size"] < directory["size"]:
        return smallest_subdirectory

    if directory["size"] > required_free_space:
        return directory
    return None


required_unused_space = 30000000
filesystem_size = 70000000
used_space = files["size"]
required_free_space = required_unused_space - (filesystem_size - used_space)

directory = find_smallest_directory_to_delete(files, required_free_space)
print(f"Size of the smallest directory that needs to be deleted is {directory['size']}")

print("*" * 80)
