
def num_to_point(x):
    if x == 1:
        return 5
    elif x == 2:
        return 4
    elif x == 3:
        return 3
    elif x in range(4,7):
        return 2
    else:
        return 1

def read_datafile(filepath):
    res = {}
    with open(filepath, 'r') as f:
        lines = f.readlines()
        res['prompt'] = lines[0].strip('\n').strip().lower().capitalize()
        res['correct'] = [lines[i].strip('\n').strip().lower() for i in range(1,11)]
        res['points'] = {lines[i].strip('\n').strip().lower() : num_to_point(i) for i in range(1,11)}
        res['wrong'] = [lines[i].strip('\n').strip().lower() for i in range(11,16)]
    return res