import sys


def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()
    
def convert_text_to_lists(text):
    lines = text.split('\n')
    data = []
    for i in range(len(lines)):
        data.append(list(map(int, lines[i].split(' '))))
    return data

def removed_index_from_list(list, index):
    return list[:index] + list[index+1:]

def is_report_safe(report):
    is_increasing = report[1] > report[0]
    for index, value in enumerate(report):
        if index == 0:
            continue
        difference = abs(value - report[index-1])
        if is_increasing != (value > report[index-1]) or difference < 1 or difference > 3:
            return False
    
    return True
            
def is_report_safe_2(report, removed_index):
    is_increasing = report[1] > report[0]
    for index, value in enumerate(report):
        if index == 0:
            continue
        difference = abs(value - report[index-1])
        if is_increasing != (value > report[index-1]) or difference < 1 or difference > 3:
            if removed_index != None:
                return False
            return any([is_report_safe_2(removed_index_from_list(report, i), i) for i in range(len(report))])
    
    return True           

def solve_part_1(data):
    reports_safety = list(map(lambda x: is_report_safe(x), data))
    return len(list(filter(lambda x: x, reports_safety)))
                
            
            

def solve_part_2(data):
    reports_safety = list(map(lambda x: is_report_safe_2(x, None), data))
    return len(list(filter(lambda x: x, reports_safety)))



def main(file_path):
    text = read_file(file_path)
    data = convert_text_to_lists(text)
    
    # return solve_part_1(data)
    return solve_part_2(data)

if __name__ == '__main__':
    filename = sys.argv[1]
    print(main(filename))