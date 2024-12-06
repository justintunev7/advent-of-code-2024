import math
import sys

# --- Day 6: Guard Gallivant ---
# The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

# You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

# Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

# You start by making a map (your puzzle input) of the situation. For example:

# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...
# The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

# Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

# If there is something directly in front of you, turn right 90 degrees.
# Otherwise, take a step forward.
# Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

# ....#.....
# ....^....#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#...
# Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

# ....#.....
# ........>#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#...
# Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#......v.
# ........#.
# #.........
# ......#...
# This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#v..
# By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

# ....#.....
# ....XXXXX#
# ....X...X.
# ..#.X...X.
# ..XXXXX#X.
# ..X.X.X.X.
# .#XXXXXXX.
# .XXXXXXX#.
# #XXXXXXX..
# ......#X..
# In this example, the guard will visit 41 distinct positions on your map.

# Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?

sys.setrecursionlimit(100000)
up: tuple[int,int] = tuple([-1, 0])
down: tuple[int,int] = tuple([1, 0])
right: tuple[int,int] = tuple([0, 1])
left: tuple[int,int] = tuple([0, -1])

turn_dict = {
    up: right,
    right: down,
    down: left,
    left: up,
}

guard_char = "^"
obstacle = "#"

def read_file(file_path: str):
    with open(file_path, 'r') as f:
        return f.read()
    
def text_to_grid(text: str):
    result: list[list[str]] = []
    rows = text.split('\n')
    for x, row in enumerate(rows):
        result.append([])
        for y, char in enumerate(row):
            if (char == guard_char):
                starting_position = tuple([x,y])
            result[-1].append(char)
    return result, starting_position


def sum_tuples(a: tuple[int, int], b: tuple[int, int]):
    return tuple[int, int]([a[0] + b[0], a[1] + b[1]])

def solve_part_1(grid: list[list[str]], guard_position: tuple[int,int], currect_direction: tuple[int,int], visited: set[tuple[int,int]]):
    visited.add(guard_position)
    new_position = sum_tuples(guard_position, currect_direction)
    if not is_in_bounds(new_position, len(grid), len(grid[0])): #new_position[0] < 0 or new_position[0] >= len(grid) or new_position[1] < 0 or new_position[1] >= len(grid[0]):
        print("Guard left map", new_position)
        return visited 
    if grid[new_position[0]][new_position[1]] == obstacle:
        print("Obstacle hit", new_position)
        currect_direction = turn_dict[currect_direction]
        new_position = guard_position
    
    return solve_part_1(grid, new_position, currect_direction, visited)

def is_in_bounds(position: tuple[int,int], max_x: int, max_y: int):
    return position[0] >= 0 and position[0] < max_x and position[1] >= 0 and position[1] < max_y

def check_if_obstruction_creates_cycle(grid: list[list[str]], guard_position: tuple[int,int], obstacle_position: tuple[int,int]):
    currect_direction = up
    visited: set[tuple[tuple[int,int],tuple[int,int]]] = set()
    current_position = guard_position
    while is_in_bounds(current_position, len(grid), len(grid[0])):
        current_visited_coordinate = tuple([current_position, currect_direction])
        if current_visited_coordinate in visited:
            return True
        visited.add(tuple([current_position, currect_direction]))
        new_position = sum_tuples(current_position, currect_direction)
        if new_position == obstacle_position or (is_in_bounds(new_position, len(grid), len(grid[0])) and grid[new_position[0]][new_position[1]] == obstacle):
            currect_direction = turn_dict[currect_direction]
        else:
            current_position = new_position
    return False

def solve_part_2(grid: list[list[str]], guard_position: tuple[int,int]):
    count_solutions = 0
    for x, row in enumerate(grid):
        for y, char in enumerate(row):
            if check_if_obstruction_creates_cycle(grid, guard_position, tuple([x,y])):
                count_solutions += 1
                print("Cycle found", count_solutions)
    return count_solutions


def main(file_path: str, part: int):
    file_text = read_file(file_path)
    grid, starting_position = text_to_grid(file_text)
    print("Guard starting at: ", starting_position)

    if part == 1:
        visited = solve_part_1(grid, starting_position, currect_direction=up, visited=set())
        return len(visited)
    else:
        return solve_part_2(grid, starting_position)
    
if __name__ == '__main__':
    filename = sys.argv[1]
    part = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
    print(main(filename, part))