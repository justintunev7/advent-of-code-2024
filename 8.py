import math
import sys

# --- Day 8: Resonant Collinearity ---
# You find yourselves on the roof of a top-secret Easter Bunny installation.

# While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise, it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

# Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

# ............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............
# The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

# So, for these two antennas with frequency a, they create the two antinodes marked with #:

# ..........
# ...#......
# ..........
# ....a.....
# ..........
# .....a....
# ..........
# ......#...
# ..........
# ..........
# Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

# ..........
# ...#......
# #.........
# ....a.....
# ........a.
# .....a....
# ..#.......
# ......#...
# ..........
# ..........
# Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

# ..........
# ...#......
# #.........
# ....a.....
# ........a.
# .....a....
# ..#.......
# ......A...
# ..........
# ..........
# The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

# ......#....#
# ...#....0...
# ....#0....#.
# ..#....0....
# ....0....#..
# .#....A.....
# ...#........
# #......#....
# ........A...
# .........A..
# ..........#.
# ..........#.
# Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

# Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?




sys.setrecursionlimit(100000)

empty_space_char = "."

def read_file(file_path: str):
    with open(file_path, 'r') as f:
        return f.read()
    
# Returns the 2d-list of chars and a dictionary representation of the coordinates of each "Antenna" char
def text_to_data(text: str) -> tuple[list[list[str]], dict[str, list[tuple[int,int]]]]:
    grid: list[list[str]] = []
    antenna_coordinates: dict[str, list[tuple[int,int]]] = dict()
    
    rows = text.split('\n')
    for x, row in enumerate(rows):
        grid.append([])
        for y, char in enumerate(row):
            grid[-1].append(char)
            if char != empty_space_char:
                if antenna_coordinates.get(char) == None:
                    antenna_coordinates[char] = list()
                antenna_coordinates[char].append(tuple([x,y]))
    return grid, antenna_coordinates


def solve_part_1(antenna_coordinates: dict[str, list[tuple[int,int]]], max_x: int, max_y: int):
    antinode_coordinates = set()
    
    def get_antinodes(a: tuple[int,int], b: tuple[int,int]) -> tuple[tuple[int,int], tuple[int,int]]:
        diff_vector = tuple([a[0] - b[0], a[1] - b[1]])
        first_antinode = tuple([a[0] + diff_vector[0], a[1] + diff_vector[1]])
        second_antinode = tuple([b[0] - diff_vector[0], b[1] - diff_vector[1]])
        return first_antinode, second_antinode
    
    def get_pairs_to_check(coordinates: list[tuple[int,int]]):
        pairs_to_check: set[tuple[tuple[int,int], tuple[int,int]]] = set()
        for first_coordinate in coordinates:
            for second_coordinate in coordinates:
                if first_coordinate != second_coordinate and not tuple([second_coordinate,first_coordinate]) in pairs_to_check:
                    pairs_to_check.add(tuple([first_coordinate, second_coordinate]))
        return pairs_to_check
    
    def get_frequency_antinodes(coordinates: list[tuple[int,int]]):
        frequency_antinode_coordinates = set()
        pairs_to_check = get_pairs_to_check(coordinates)
        for first_coordinate, second_coordinate in pairs_to_check:
            first_antinode, second_antinode = get_antinodes(first_coordinate, second_coordinate)
            if first_antinode[0] >= 0 and first_antinode[0] < max_x and first_antinode[1] >= 0 and first_antinode[1] < max_y:
                frequency_antinode_coordinates.add(first_antinode)
            if second_antinode[0] >= 0 and second_antinode[0] < max_x and second_antinode[1] >= 0 and second_antinode[1] < max_y:
                frequency_antinode_coordinates.add(second_antinode)
        return frequency_antinode_coordinates
        
    
    for key in antenna_coordinates:
        frequency_antinode_coordinates = get_frequency_antinodes(antenna_coordinates.get(key))
        antinode_coordinates = antinode_coordinates.union(frequency_antinode_coordinates)
    return antinode_coordinates, len(antinode_coordinates)

def solve_part_2(antenna_coordinates: dict[str, list[tuple[int,int]]], max_x: int, max_y: int):
    antinode_coordinates: set[tuple[int,int]] = set()
    
        
    def get_antinodes(a: tuple[int,int], b: tuple[int,int]) -> set[tuple[int,int]]:
        antinodes: set[tuple[int,int]] = set()
        diff_vector = tuple([a[0] - b[0], a[1] - b[1]])
        
        multiplier = 1
        current_antinode = a
        while current_antinode[0] >= 0 and current_antinode[0] < max_x and current_antinode[1] >= 0 and current_antinode[1] < max_y:
            antinodes.add(current_antinode)
            current_antinode = tuple([a[0] + (diff_vector[0] * multiplier), a[1] + (diff_vector[1] * multiplier)])
            multiplier += 1
        
        multiplier = -1
        current_antinode = a
        while current_antinode[0] >= 0 and current_antinode[0] < max_x and current_antinode[1] >= 0 and current_antinode[1] < max_y:
            antinodes.add(current_antinode)
            current_antinode = tuple([a[0] + (diff_vector[0] * multiplier), a[1] + (diff_vector[1] * multiplier)])
            multiplier -= 1
        return antinodes
    
    def get_pairs_to_check(coordinates: list[tuple[int,int]]):
        pairs_to_check: set[tuple[tuple[int,int], tuple[int,int]]] = set()
        for first_coordinate in coordinates:
            for second_coordinate in coordinates:
                if first_coordinate != second_coordinate and not tuple([second_coordinate,first_coordinate]) in pairs_to_check:
                    pairs_to_check.add(tuple([first_coordinate, second_coordinate]))
        return pairs_to_check
    
    def get_frequency_antinodes(coordinates: list[tuple[int,int]]):
        frequency_antinode_coordinates: set[tuple[int,int]] = set()
        pairs_to_check = get_pairs_to_check(coordinates)
        for first_coordinate, second_coordinate in pairs_to_check:
            pair_antinodes = get_antinodes(first_coordinate, second_coordinate)
            frequency_antinode_coordinates = frequency_antinode_coordinates.union(pair_antinodes)
        return frequency_antinode_coordinates
        
    
    for key in antenna_coordinates:
        frequency_antinode_coordinates = get_frequency_antinodes(antenna_coordinates.get(key))
        antinode_coordinates = antinode_coordinates.union(frequency_antinode_coordinates)
    return antinode_coordinates, len(antinode_coordinates)


def main(file_path: str, part: int):
    file_text = read_file(file_path)
    grid, antenna_coordinates = text_to_data(file_text)

    if part == 1:
        return solve_part_1(antenna_coordinates, len(grid), len(grid[0]))
    else:
        return solve_part_2(antenna_coordinates, len(grid), len(grid[0]))
    
if __name__ == '__main__':
    filename = sys.argv[1]
    part = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
    print(main(filename, part))
