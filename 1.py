import sys


def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()
    
def convert_text_to_lists(text):
    text_list = text.split('\n')
    first_list = list(map(lambda x: int(x.split('   ')[0]), text_list))
    second_list = list(map(lambda x: int(x.split('   ')[1]), text_list))
    return first_list, second_list

def solve_part_1(first_list, second_list):
    first_list.sort()
    second_list.sort()
    
    assert len(first_list) == len(second_list)
    
    differences = []
    for i in range(len(first_list)):
        differences.append(abs(first_list[i] - second_list[i]))
    
    print(differences)
    
    return sum(differences)

def solve_part_2(first_list, second_list):
    assert len(first_list) == len(second_list)
    
    similarity_score = 0
    for i in range(len(first_list)):
        val = first_list[i]
        multiplier = len(list(filter(lambda x: x == val, second_list)))
        similarity_score += val * multiplier
        
    return similarity_score



def main(file_path):
    text = read_file(file_path)
    first_list, second_list = convert_text_to_lists(text)
    return solve_part_2(first_list, second_list)

if __name__ == '__main__':
    filename = sys.argv[1]
    print(main(filename))