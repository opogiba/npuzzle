import numpy
import re


def basic_check(npuzzle, size):
    if npuzzle.shape != (size, size):
        raise Exception('Not valid npuzzle, map error')

    unique_elements = set()

    for el in npuzzle:
        unique_elements = unique_elements.union(set(el))

    if len(unique_elements) != size * size:
        raise Exception('Not valid npuzzle, map error, dublicate elements')

    final_set = {elem for elem in range(size * size)}

    if final_set.intersection(unique_elements) != final_set:
        raise Exception('Not valid npuzzle, map error')

#TODO CHANGE IT change help field
def make_arguments(parser):
    parser.add_argument("-size", type=int, help="Size of the puzzle's side. Must be >= 3.", default=3, dest='size')
    parser.add_argument("-s", "--solvable", action="store_true", default=False,
                        help="Forces generation of a solvable puzzle. Overrides -u.")
    parser.add_argument("-u", "--unsolvable", action="store_true", default=False,
                        help="Forces generation of an unsolvable puzzle")
    parser.add_argument("-i", "--iterations", type=int, default=10000, help="Number of passes")

    parser.add_argument('-f', '--file', default='', type=str, help='path to file with puzzle')

    parser.add_argument('-g', '--greedy', action='store_true', help='''greedy search is basis.
    Do not work with -uc option''', dest='greedy')

    parser.add_argument('-uc', '--uniformcost', action='store_true', help='''uniform-cost search is basis. 
    Do not work with -g option.''', dest='uniformcost')

    parser.add_argument('-q', '--queuesize', type=int, default=100, help='''Set the size of the Queue. 
    Default value is 100''', dest='queue_size')

    parser.add_argument('-H', '--heuristics', choices=['M', 'ML', 'H', 'E', 'D'], default='M',
                        dest='heuristics',
                        help='''Choose one of heuristics to solve the puzzle.
    M - for Manhattan distance.
    ML - for Manhattan distance + Linear conflict.
    H - for Hemming distance.
    E - for Euclidean distance.
    D - for Diagonal distance.
    Default value is M''')
    args = parser.parse_args()

    return args


def list_to_string(list_map, size):
    space = len(str(size * size))
    str_map = ''
    for coord_y in range(size):
        for coord_x in range(size):
            str_map += str(list_map[coord_y * size + coord_x]).rjust(space) + ' '
        str_map += '\n'
    return str_map


def str_to_numpy_array(string_map, size):
    start_map = list()
    lines = string_map.strip().split('\n')

    for line in lines:
        row = re.findall(r'\d+', line)
        row = [int(digit) for digit in row]
        start_map.append(row)

    npuzzle = numpy.array(start_map)

    if npuzzle.shape != (size, size):
        raise Exception('Not valid npuzzle, map error')

    return npuzzle


def str_from_file_to_numpy_array(args):
    start_map = list()
    size = args.size
    filename = args.file

    try:
        with open(filename, 'r') as lines:
            for line in lines:
                row = re.findall(r'\d+', line)
                row = [int(digit) for digit in row]
                start_map.append(row)
        npuzzle = numpy.array(start_map)

    except Exception:
        raise Exception('Not valid path to file')

    basic_check(npuzzle, size)

    return npuzzle

#TODO change function
def is_solvable(numpy_puzzle, size):
    inversions = 0
    flat_map = numpy_puzzle.flatten()

    for i, puzzle in enumerate(flat_map):
        if puzzle == 0:
            continue
        for elem in flat_map[:i]:
            if elem > puzzle:
                inversions += 1

    is_inversions_even = True if inversions % 2 == 0 else False

    if size % 2 != 0:
        return not is_inversions_even
    if 0 in numpy_puzzle[::-2]:
        return is_inversions_even
    elif 0 in numpy_puzzle[::2]:
        return not is_inversions_even
    return False





