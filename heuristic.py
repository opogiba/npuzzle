import numpy
import math
import NpuzzleState


def manhattan_heuristic(state: NpuzzleState):
    distance = 0
    for tuple_index_to_solve, to_solve_value in numpy.ndenumerate(state.state):
        for tuple_index_goal, t_value in numpy.ndenumerate(state.final_terminal_state):
            if to_solve_value == t_value:
                diff = numpy.subtract(tuple_index_to_solve, tuple_index_goal)
                distance += sum(abs(diff))
                break
    return distance


def hemming_heuristic(state: NpuzzleState):
    return len(numpy.not_equal(state.state, state.final_terminal_state))


def euclidean_heuristic(state: NpuzzleState):
    distance = 0
    for tuple_index_to_solve, to_solve_value in numpy.ndenumerate(state.state):
        for tuple_index_goal, t_value in numpy.ndenumerate(state.final_terminal_state):
            if to_solve_value == t_value:
                absolute_diff = abs(numpy.subtract(tuple_index_to_solve, tuple_index_goal))
                distance += math.sqrt(absolute_diff[0] ** 2 + absolute_diff[1] ** 2)
                break
    return distance


def diagonal_heuristic(state: NpuzzleState):
    distance = 0
    for tuple_index_to_solve, to_solve_value in numpy.ndenumerate(state.state):
        for tuple_index_goal, t_value in numpy.ndenumerate(state.final_terminal_state):
            if to_solve_value == t_value:
                absolute_diff = abs(numpy.subtract(tuple_index_to_solve, tuple_index_goal))
                distance += sum(absolute_diff) + (math.sqrt(2) - 2) * min(absolute_diff)
                break
    return distance


def heuristic_choise(heuristics, state):

    if heuristics == 'D':
        return diagonal_heuristic(state)

    if heuristics == 'DH':
        return diagonal_heuristic(state) + hemming_heuristic(state)

    if heuristics == 'M':
        return manhattan_heuristic(state)

    if heuristics == 'H':
        return hemming_heuristic(state)

    if heuristics == 'E':
        return euclidean_heuristic(state)

    if heuristics == 'A':
        return diagonal_heuristic(state) + hemming_heuristic(state) + \
            manhattan_heuristic(state) + euclidean_heuristic(state)
