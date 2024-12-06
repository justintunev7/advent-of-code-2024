import math
import sys

# --- Day 5: Print Queue ---
# Satisfied with their search on Ceres, the squadron of scholars suggests subsequently scanning the stationery stacks of sub-basement 17.

# The North Pole printing department is busier than ever this close to Christmas, and while The Historians continue their search of this historically significant facility, an Elf operating a very familiar printer beckons you over.

# The Elf must recognize you, because they waste no time explaining that the new sleigh launch safety manual updates won't print correctly. Failure to update the safety manuals would be dire indeed, so you offer your services.

# Safety protocols clearly indicate that new pages for the safety manuals must be printed in a very specific order. The notation X|Y means that if both page number X and page number Y are to be produced as part of an update, page number X must be printed at some point before page number Y.

# The Elf has for you both the page ordering rules and the pages to produce in each update (your puzzle input), but can't figure out whether each update has the pages in the right order.

# For example:

# 47|53
# 97|13
# 97|61
# 97|47
# 75|29
# 61|13
# 75|53
# 29|13
# 97|29
# 53|29
# 61|53
# 97|53
# 61|29
# 47|13
# 75|47
# 97|75
# 47|61
# 75|61
# 47|29
# 75|13
# 53|13

# 75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# 75,97,47,61,53
# 61,13,29
# 97,13,75,29,47
# The first section specifies the page ordering rules, one per line. The first rule, 47|53, means that if an update includes both page number 47 and page number 53, then page number 47 must be printed at some point before page number 53. (47 doesn't necessarily need to be immediately before 53; other pages are allowed to be between them.)

# The second section specifies the page numbers of each update. Because most safety manuals are different, the pages needed in the updates are different too. The first update, 75,47,61,53,29, means that the update consists of page numbers 75, 47, 61, 53, and 29.

# To get the printers going as soon as possible, start by identifying which updates are already in the right order.

# In the above example, the first update (75,47,61,53,29) is in the right order:

# 75 is correctly first because there are rules that put each other page after it: 75|47, 75|61, 75|53, and 75|29.
# 47 is correctly second because 75 must be before it (75|47) and every other page must be after it according to 47|61, 47|53, and 47|29.
# 61 is correctly in the middle because 75 and 47 are before it (75|61 and 47|61) and 53 and 29 are after it (61|53 and 61|29).
# 53 is correctly fourth because it is before page number 29 (53|29).
# 29 is the only page left and so is correctly last.
# Because the first update does not include some page numbers, the ordering rules involving those missing page numbers are ignored.

# The second and third updates are also in the correct order according to the rules. Like the first update, they also do not include every page number, and so only some of the ordering rules apply - within each update, the ordering rules that involve missing page numbers are not used.

# The fourth update, 75,97,47,61,53, is not in the correct order: it would print 75 before 97, which violates the rule 97|75.

# The fifth update, 61,13,29, is also not in the correct order, since it breaks the rule 29|13.

# The last update, 97,13,75,29,47, is not in the correct order due to breaking several rules.

# For some reason, the Elves also need to know the middle page number of each update being printed. Because you are currently only printing the correctly-ordered updates, you will need to find the middle page number of each correctly-ordered update. In the above example, the correctly-ordered updates are:

# 75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# These have middle page numbers of 61, 53, and 29 respectively. Adding these page numbers together gives 143.

# Of course, you'll need to be careful: the actual list of page ordering rules is bigger and more complicated than the above example.

# Determine which updates are already in the correct order. What do you get if you add up the middle page number from those correctly-ordered updates?

# MY NOTES
# for each number on left side of rules, create a list of all numbers that must be after that number, and save in a key-value dictionary (key = number, value = set of numbers that must come after it)
# Keep a set of all previous numbers checked in update

# EXAMPLE 1
# rules
# {
#   47: {53, 61, 29}
#   ... 
# }

# for each number in update row, check rules.
# Ex: 53, 47
# 53 (no previous numbers, good :thumbsup:)
# 47
    # check left-side rules. If any previous numbers appear in set, fail.
    # 53 (previously checked) appears in 47's rules, fails
   
# EXAMPLE 2
# rules
# {
#   97: {13, 61, 47, 29, 75}
#   29: {13}
#   61: {53, 29, 13}
#   ... 
# }

# for each number in update row, check rules.
# Ex: 97, 29, 97, 13, 61 (bad)
# 97 (no previous numbers, good :thumbsup:)
# 29
    # check for 13 before 29, none found, good 
# 97
    # check for {13, 61, 47, 29, 75} before 97, found 29, fails

   
# EXAMPLE 3
# rules
# {
#   97: {13, 61, 47, 29, 75}
#   29: {13}
#   61: {53, 29, 13}
#   ... 
# }

# for each number in update row, check rules.
# Ex: 97, 29, 13, 61 (bad)
# 97 (no previous numbers, good :thumbsup:)
# 29
    # check for 13 before 29, none found, good 
# 13
    # check for 13's rules in previous. No rules found, good
# 61
    # check for {53, 29, 13} before 61. Found 13 (and 29), fails
    
    
    

def read_file(file_path: str):
    with open(file_path, 'r') as f:
        return f.read()
    
def rules_to_dict(rules: str):
    rules_dict: dict[str, set[str]] = dict()
    lines = rules.split('\n')
    rules_list: list[tuple[str, str]] = [tuple[str,str](line.split('|')) for line in lines]
    for rule in rules_list:
        if rules_dict.get(rule[0]) == None:
            rules_dict[rule[0]] = set()
        rules_dict[rule[0]].add(rule[1])
    return rules_dict

def updates_to_list(updates: str):
    return [row.split(',') for row in updates.split('\n')]
    

def sets_are_exclusive(prohibited: set[str], values: set[str]):
    return len(prohibited.intersection(values)) == 0

    
def get_mid_value(values: list[str]):
    return values[int(round((len(values) - 1) / 2))]

def solve_part_1(rules: dict[str, set[str]], updates: list[list[str]]):
    def is_update_valid(update: list[str]):
        previous = set[str]()
        for value in update:
            if not sets_are_exclusive(rules.get(value, set()), previous):
                return False
            previous.add(value)
        return True
    
    mid_values: list[int] = []
    for update in updates:
        if is_update_valid(update):
            print(update)
            mid_values.append(int(get_mid_value(update)))

    print(mid_values)
    return sum(mid_values)
        

def solve_part_2(rules: dict[str, set[str]], updates: list[list[str]]):
    def is_update_valid(update: list[str]):
        previous = set[str]()
        for value in update:
            if not sets_are_exclusive(rules.get(value, set()), previous):
                return False
            previous.add(value)
        return True

    def fix_ordering_rec(update: list[str]):
        previous = set[str]()
        for i, value in enumerate(update):
            intersection = rules.get(value, set()).intersection(previous)
            if len(intersection) == 0:
                previous.add(value)
                continue
            
            min_index = i
            for val in intersection:
                new_index = update.index(val)
                min_index = min(min_index, new_index)
            
            new_update = update[:i] + update[i+1:]
            new_update.insert(min_index, value)
            return fix_ordering_rec(new_update)
        return update

    
    mid_values: list[int] = []
    for update in updates:
        if not is_update_valid(update):
            # fix ordering
            fixed_order = fix_ordering_rec(update)
            mid_values.append(int(get_mid_value(fixed_order)))

    print(mid_values)
    return sum(mid_values)


def main(file_path: str, part: int):
    rules_text = read_file(file_path)
    updates_text = read_file(file_path.replace("rules", "updates"))
    rules_dict = rules_to_dict(rules_text)
    updates_list = updates_to_list(updates_text)
    
    return solve_part_1(rules_dict, updates_list) if part == 1 else solve_part_2(rules_dict, updates_list)
    
if __name__ == '__main__':
    filename = sys.argv[1]
    part = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
    print(main(filename, part))