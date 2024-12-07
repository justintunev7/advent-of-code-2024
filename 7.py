import math
import sys

# --- Day 7: Bridge Repair ---
# The Historians take you to a familiar rope bridge over a river in the middle of a jungle. The Chief isn't on this side of the bridge, though; maybe he's on the other side?

# When you go to cross the bridge, you notice a group of engineers trying to repair it. (Apparently, it breaks pretty frequently.) You won't be able to cross until it's fixed.

# You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young elephants were playing nearby and stole all the operators from their calibration equations! They could finish the calibrations if only someone could determine which test values could possibly be produced by placing any combination of operators into their calibration equations (your puzzle input).

# For example:

# 190: 10 19
# 3267: 81 40 27
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20
# Each line represents a single equation. The test value appears before the colon on each line; it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.

# Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).

# Only three of the above equations can be made true by inserting operators:

# 190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
# 3267: 81 40 27 has two positions for operators. Of the four possible configurations of the operators, two cause the right side to match the test value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
# 292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.
# The engineers just need the total calibration result, which is the sum of the test values from just the equations that could possibly be true. In the above example, the sum of the test values for the three equations listed above is 3749.

# Determine which equations could possibly be true. What is their total calibration result?


sys.setrecursionlimit(100000)

def read_file(file_path: str):
    with open(file_path, 'r') as f:
        return f.read()
    
def get_values_from_file_text(file_text: str) -> list[tuple[int, list[int]]]:
    result: list[tuple[int, list[int]]] = []
    for line in file_text.split('\n'):
        test_value_str, equation_str = line.split(': ')
        equation_list_str = [int(num) for num in equation_str.split(' ')]
        result.append(tuple([int(test_value_str), equation_list_str]))
    return result
    
def equation_has_solution_1(result_value: int, inputs: list[int]):
    def has_solution_rec(current_value: int, index: int):
        if current_value > result_value or index >= len(inputs):
            return current_value == result_value
        return has_solution_rec(current_value + inputs[index], index + 1) or has_solution_rec(current_value * inputs[index], index + 1)
        
    return has_solution_rec(0, 0)

def solve_part_1(equations: list[tuple[int, list[int]]]):
    sum = 0
    for equation in equations:
        if equation_has_solution_1(equation[0], equation[1]):
            sum += equation[0]
    return sum

# Same recursive solution as part 1, but with a concatenated branch
def equation_has_solution_2(result_value: int, inputs: list[int]):
    def has_solution_rec(current_value: int, index: int):
        if current_value > result_value or index >= len(inputs):
            return current_value == result_value
        concatenated = int(str(current_value) + str(inputs[index]))
        next_index = index + 1
        return has_solution_rec(current_value + inputs[index], next_index) or has_solution_rec(current_value * inputs[index], next_index) or has_solution_rec(concatenated, next_index)
        
    return has_solution_rec(0, 0)

def solve_part_2(equations: list[tuple[int, list[int]]]):
    sum = 0
    for equation in equations:
        if equation_has_solution_2(equation[0], equation[1]):
            sum += equation[0]
    return sum


def main(file_path: str, part: int):
    file_text = read_file(file_path)
    equations_list = get_values_from_file_text(file_text)
    print("Equations List:", equations_list)

    if part == 1:
        return solve_part_1(equations_list)
    else:
        return solve_part_2(equations_list)
    
if __name__ == '__main__':
    filename = sys.argv[1]
    part = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
    print(main(filename, part))
