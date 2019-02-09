import argparse
from uttils import make_arguments
from generator import generate_npuzle
from NpuzzleState import NpuzzleState
from NpuzzleQueue import StateAnalyzeQueue, StateDeletedQueue
from Statistics import Statistics
import time


def make_solution(final_state):
    list_of_solution = list()
    list_of_solution.insert(0,  final_state)

    while 1:
        if final_state.parent:
            final_state = final_state.parent
            list_of_solution.insert(0, final_state)
        else:
            break

    Statistics.show_result(list_of_solution)


def make_neigbour(direction, min_state, size):
    new_coords = min_state.shift_puzzle(direction)

    if 0 <= new_coords[0] <= size - 1 and 0 <= new_coords[1] <= size - 1:
        new_npuzle_state = min_state.state.copy()
        change_element = new_npuzle_state[new_coords]
        new_npuzle_state[min_state.empty_puzzle_coord] = change_element
        new_npuzle_state[new_coords] = 0
        check_state = NpuzzleState(new_npuzle_state, parent_state=min_state)
        return check_state
    return None


def check_greedy(greedy, g_min_state):
    if greedy:
        g_coff = g_min_state
    else:
        g_coff = g_min_state + 1.0
    return g_coff


def algorithm(open_queue, close_queue, final_state, args):
    size = args.size
    greedy = args.greedy
    min_state = None

    while not open_queue.empty():
        min_state = open_queue.get_nowait()
        time_complexity = Statistics.time_complexity
        size_complexity = Statistics.size_complexity

        Statistics.time_complexity = open_queue.qsize() + 1 if open_queue.qsize() > time_complexity else time_complexity
        Statistics.size_complexity = len(open_queue) + len(close_queue) if size_complexity < len(open_queue) + len(close_queue) else size_complexity

        if min_state != final_state:
            close_queue.append(min_state)

            for direction in ['up_direction', 'down_direction', 'right_direction', 'left_direction']:
                neighbour = make_neigbour(direction, min_state, size)

                if not neighbour or neighbour in close_queue:
                    continue

                g_coff = check_greedy(greedy, min_state.g_coff)

                if neighbour not in open_queue:
                    neighbour.set_f(g=g_coff)
                    open_queue.put_nowait(neighbour)
                elif neighbour in open_queue and g_coff <= neighbour.g_coff:
                    i = open_queue.queue.index(neighbour)
                    neighbour = open_queue.queue[i]
                    neighbour.parent = min_state
                    neighbour.set_f(g=g_coff)
        else:
            Statistics.end_time = time.time()
            break

    return min_state


if __name__ == '__main__':
    Statistics.start_time = time.time()
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    args = make_arguments(parser)
    npuzzle = generate_npuzle(args)
    NpuzzleState.set_final_terminal_state(args.size, args.heuristics)

    start_state = NpuzzleState(state=npuzzle)
    final_state = NpuzzleState(state=NpuzzleState.final_terminal_state)
    start_state.set_f()

    open_queue = StateAnalyzeQueue(maxsize=args.queue_size)
    open_queue.put_nowait(start_state)
    close_queue = StateDeletedQueue()

    solution_case = algorithm(open_queue, close_queue, final_state, args)
    make_solution(solution_case)
