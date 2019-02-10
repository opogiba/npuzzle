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


def make_arguments(parser):
    parser.add_argument('-H', '--heuristics', choices=['M', 'DH', 'H', 'E', 'D', 'A'], default='M',
                        dest='heuristics',
                        help='''Select heuristics to solve.
    M - for Manhattan distance.
    DH - for Diagonal distance + Hemming distance.
    E - for Euclidean distance.
    D - for Diagonal distance.
    A - for all above.
    Default value is M''')
    parser.add_argument("-s", "--solvable", action="store_true", default=False,
                         help="Generates solvable puzzle. Not to use with -u.")
    parser.add_argument("-u", "--unsolvable", action="store_true", default=False,
                         help="Generates unsolvable")
    parser.add_argument("-i", "--iterations", type=int, default=10000, help="Passes number")

    parser.add_argument('-f', '--file', default='', type=str, help='filepath to puzzle textfile')

    parser.add_argument('-g', '--greedy', action='store_true', help='''Greedy one. Not to use
      with -uc''', dest='greedy')

    parser.add_argument('-uc', '--uniformcost', action='store_true', help='''Uniform-cost search
    ''', dest='uniformcost')
    parser.add_argument("-size", type=int, help="Map size, >= 3", default=3, dest='size')

    parser.add_argument('-q', '--queuesize', type=int, default=100, help='''Set size''', dest='queue_size')
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


def is_solvable(npuzzle_map_numpy, size):
    inv = 0
    size_not_even = size % 2 != 0
    # Make an array from map
    array_map = npuzzle_map_numpy.flatten()

    for i, puzzle in enumerate(array_map):
        for elem in array_map[:i]:
            if not puzzle:
                break
            if elem > puzzle:
                inv += 1

    is_inv_even = inv % 2 == 0

    if size_not_even:
        return not is_inv_even
    if 0 in npuzzle_map_numpy[::-2]:
        return is_inv_even
    elif 0 in npuzzle_map_numpy[::2]:
        return not is_inv_even
    return False

