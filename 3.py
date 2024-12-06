import sys

# --- Day 3: Mull It Over ---
# "Our computers are having issues, so I have no idea if we have any Chief Historians in stock! You're welcome to check the warehouse, though," says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The Historians head out to take a look.

# The shopkeeper turns to you. "Any chance you can see why our computers are having issues again?"

# The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been jumbled up!

# It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.

# However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

# For example, consider the following section of corrupted memory:

# xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
# Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

# Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?

dont_str = "don't()"
do_str = "do()"
mul_start_str = 'mul('
mul_end_char = ')'
multiply_op = 'x'

def read_file(file_path: str):
    with open(file_path, 'r') as f:
        return f.read()


# iterate through string
# for each 'mul(', check recursively for 'num,num)' pattern 
# multiply the two numbers and add result to results list
# at end, add up results list values

def solve_part_1(text: str):
    results: list[int] = []
    i = 0
    
    def scan_number(iterator: int):
        num = ''
        # recursive operations weren't required, but if they were, this should solve that case
        # if text[iterator:iterator+len(mul_start_str) - 1] == mul_start_str:
        #     return mul_recursive(iterator)
        while text[iterator].isdecimal() and iterator < len(text):
            num += text[iterator]
            iterator += 1
        return num, iterator
    
    
    def mul_recursive(iterator: int):
        print('in mul_recursive', iterator)
        first_num_str, iterator = scan_number(iterator)
        if first_num_str is None or iterator >= len(text) or text[iterator] != ',':
            return None, iterator
        iterator += 1
        second_num_str, iterator = scan_number(iterator)
        if second_num_str is None or iterator >= len(text) or text[iterator] != ')':
            return None, iterator
        print('found mul operation', first_num_str, second_num_str, iterator)
        return int(first_num_str) * int(second_num_str), iterator + 1
            

    while i < len(text):    
        print(text[i:i+len(mul_start_str)-1])
        if text[i:i+len(mul_start_str)] == mul_start_str:
            mul_result_value, i = mul_recursive(i+len(mul_start_str))
            if mul_result_value is not None:
                results.append(mul_result_value)
        else:
            i += 1
    
    return sum(results)
                
            
            

def solve_part_2(text: str):
    results: list[int] = []
    i = 0
    do_mul = True
    
    def scan_number(iterator: int):
        num = ''
        # recursive operations weren't required, but if they were, this should solve that case
        # if text[iterator:iterator+len(mul_start_str) - 1] == mul_start_str:
        #     return mul_recursive(iterator)
        while text[iterator].isdecimal() and iterator < len(text):
            num += text[iterator]
            iterator += 1
        return num, iterator
    
    
    def mul_recursive(iterator: int):
        first_num_str, iterator = scan_number(iterator)
        if first_num_str is None or iterator >= len(text) or text[iterator] != ',':
            return None, iterator
        iterator += 1
        second_num_str, iterator = scan_number(iterator)
        if second_num_str is None or iterator >= len(text) or text[iterator] != ')':
            return None, iterator
        print('found mul operation', first_num_str, second_num_str, iterator)
        return int(first_num_str) * int(second_num_str), iterator + 1
            
    while i < len(text):    
        if text[i:i+len(do_str)] == do_str:
            print('do')
            do_mul = True
            i += len(do_str)
        elif text[i:i+len(dont_str)] == dont_str:
            print('dont')
            do_mul = False
            i += len(dont_str)
        elif do_mul and text[i:i+len(mul_start_str)] == mul_start_str:
            mul_result_value, i = mul_recursive(i+len(mul_start_str))
            if mul_result_value is not None:
                results.append(mul_result_value)
        else:
            i += 1
    
    return sum(results)



def main(file_path: str, part: int):
    text = read_file(file_path)
    return solve_part_1(text) if part == 1 else solve_part_2(text)
    
if __name__ == '__main__':
    filename = sys.argv[1]
    part = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
    print(main(filename, part))