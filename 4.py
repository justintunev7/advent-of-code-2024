import sys

# --- Day 4: Ceres Search ---
# "Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

# As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

# This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


# ..X...
# .SAMX.
# .A..A.
# XMAS.S
# .X....
# The actual word search will be full of letters instead. For example:

# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX
# In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

# ....XXMAS.
# .SAMXMS...
# ...S..A...
# ..A.A.MS.X
# XMASAMX.MM
# X.....XA.A
# S.S.S.S.SS
# .A.A.A.A.A
# ..M.M.M.MM
# .X.X.XMASX
# Take a look at the little Elf's word search. How many times does XMAS appear?

xmas = 'XMAS'
mas = 'MAS'
mas_reversed = 'SAM'

def read_file(file_path: str):
    with open(file_path, 'r') as f:
        return f.read()
    
def text_to_grid(text: str):
    result: list[list[str]] = []
    rows = text.split('\n')
    for row in rows:
        result.append([])
        for char in row:
            result[-1].append(char)
    return result

up = (-1, 0)
down = (1, 0)
right = (0, 1)
left = (0, -1)
upleft = (-1, -1)
upright = (-1, 1)
downleft = (1, -1)
downright = (1, 1)

def sum_tuples(a: tuple[int, int], b: tuple[int, int]):
    return tuple[int, int]([a[0] + b[0], a[1] + b[1]])

def get_coordinates_in_direction(current_coordinate: tuple[int, int], direction: tuple[int, int], length: int):
    coordinates: list[tuple[int, int]] = [current_coordinate]
    previous_coordinate = current_coordinate
    for i in range(length-1):
        coordinates.append(sum_tuples(previous_coordinate, direction))
        previous_coordinate = sum_tuples(previous_coordinate, direction)
    return coordinates
    
def get_coordinates_to_check_1(current_coordinate: tuple[int, int], length: int):
    return [
        get_coordinates_in_direction(current_coordinate, up, length),
        get_coordinates_in_direction(current_coordinate, down, length),
        get_coordinates_in_direction(current_coordinate, left, length),
        get_coordinates_in_direction(current_coordinate, right, length),
        get_coordinates_in_direction(current_coordinate, upleft, length),
        get_coordinates_in_direction(current_coordinate, upright, length),
        get_coordinates_in_direction(current_coordinate, downleft, length),
        get_coordinates_in_direction(current_coordinate, downright, length),
        ]
    
def get_coordinates_to_check_2(current_coordinate: tuple[int, int], length: int):
    return [
        get_coordinates_in_direction(current_coordinate, downright, length),
        # start from bottom-left of X and search up-right
        get_coordinates_in_direction(sum_tuples(current_coordinate, tuple([2, 0])), upright, length),
        ]

def search_for_keyword(grid: list[list[str]], coordinates: list[tuple[int, int]], keyword: str):
    for i, coordinate in enumerate(coordinates):
        x = coordinate[0]
        y = coordinate[1]
        if x < 0 or x >= len(grid) or y < 0 or y >= len(grid) or grid[x][y] != keyword[i]:
            return False
    return True

# for each element in grid, check for an X, then call a recursive up/down/left/right/diagonal(4) search
def solve_part_1(grid: list[list[str]]):
    occurences = 0
    result = [['.' for char in row]for row in grid]
    
    def mark_coordinates_success(coordinates: list[tuple[int, int]]):
        for coordinate in coordinates:
            result[coordinate[0]][coordinate[1]] = grid[coordinate[0]][coordinate[1]]
        
    for x, row in enumerate(grid):
        for y, element in enumerate(row):
            if element == xmas[0]:
                all_coordinates_to_check = get_coordinates_to_check_1(tuple([x, y]), len(xmas))
                for coordinates_to_check in all_coordinates_to_check:
                    if search_for_keyword(grid, coordinates_to_check, xmas):
                        occurences += 1
                        mark_coordinates_success(coordinates_to_check)
                
    return occurences
                
            
            

def solve_part_2(grid: list[list[str]]):
    occurences = 0
    result = [['.' for char in row]for row in grid]
    
    def mark_coordinates_success(coordinates: list[tuple[int, int]]):
        print('success', coordinates)
        for coordinate in coordinates:
            result[coordinate[0]][coordinate[1]] = grid[coordinate[0]][coordinate[1]]
            
    for x, row in enumerate(grid):
        for y, element in enumerate(row):
            if element == mas[0] or element == mas_reversed[0]:
                all_coordinates_to_check = get_coordinates_to_check_2(tuple([x, y]), len(mas))
                def found_x_mas():
                    for coordinates_to_check in all_coordinates_to_check:
                        if not search_for_keyword(grid, coordinates_to_check, mas) and not search_for_keyword(grid, coordinates_to_check, mas_reversed):
                            return False
                    return True
                if found_x_mas():
                    occurences += 1
                    

                
    return occurences



def main(file_path: str, part: int):
    text = read_file(file_path)
    grid = text_to_grid(text)
    return solve_part_1(grid) if part == 1 else solve_part_2(grid)
    
if __name__ == '__main__':
    filename = sys.argv[1]
    part = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
    print(main(filename, part))