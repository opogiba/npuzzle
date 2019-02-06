from uttils import list_to_string, str_to_numpy_array, str_from_file_to_numpy_array, is_solvable
import random
import numpy


def advance_generator_check(p, solvable, s):
    np_arr = numpy.array(p)
    np_arr = np_arr.reshape((s, s))
    if solvable:
        if is_solvable(np_arr, s):
            return True
        else:
            return False
    return True


def make_puzzle(s, solvable, iterations):
    def swap_empty(p):
        idx = p.index(0)
        poss = []
        if idx % s > 0:
            poss.append(idx - 1)
        if idx % s < s - 1:
            poss.append(idx + 1)
        if idx / s > 0:
            poss.append(idx - s)
        if idx / s < s - 1:
            poss.append(idx + s)
        swi = random.choice(poss)
        p[idx] = p[swi]
        p[swi] = 0

    p = make_goal(s)
    for i in range(iterations):
        swap_empty(p)
    if not solvable:
        if p[0] == 0 or p[1] == 0:
            p[-1], p[-2] = p[-2], p[-1]
        else:
            p[0], p[1] = p[1], p[0]

    flag = advance_generator_check(p, solvable, s)

    if flag is False:
        return make_puzzle(s, solvable=solvable, iterations=iterations)

    return p


def make_goal(s):
    ts = s * s
    puzzle = [-1 for i in range(ts)]
    cur = 1
    x = 0
    ix = 1
    y = 0
    iy = 0
    while True:
        puzzle[x + y * s] = cur
        if cur == 0:
            break
        cur += 1
        if x + ix == s or x + ix < 0 or (ix != 0 and puzzle[x + ix + y * s] != -1):
            iy = ix
            ix = 0
        elif y + iy == s or y + iy < 0 or (iy != 0 and puzzle[x + (y + iy) * s] != -1):
            ix = -iy
            iy = 0
        x += ix
        y += iy
        if cur == s * s:
            cur = 0

    return puzzle


def generate_npuzle(args):
    if args.solvable and args.unsolvable:
        raise Exception('You cannot use arguments -s and -u together')

    if args.greedy and args.uniformcost:
        raise Exception("You cannot use Uniform cost and Greedy searches together!")

    solvable = args.solvable if args.solvable else args.unsolvable if args.unsolvable else random.choice([True, False])
    iterations = args.iterations
    size = args.size

    if size < 3:
        raise Exception('You cannot solve npuzzle where size less then 3*3')

    if args.file:
        numpy_puzzle = str_from_file_to_numpy_array(args)
        str_puzzle = list_to_string(list(numpy_puzzle.flatten()), size)

    else:
        puzzle = make_puzzle(size, solvable=solvable, iterations=iterations)
        str_puzzle = list_to_string(puzzle, size)
        numpy_puzzle = str_to_numpy_array(str_puzzle, size)

    print('Start npuzzle:')
    print(str_puzzle)

    if not is_solvable(numpy_puzzle, args.size):
        print('Puzzle is not solvable')
        exit(1)
    else:
        print('Puzzle is solvable')

    if args.uniformcost:
        args.heuristics = 'U'
    return numpy_puzzle


