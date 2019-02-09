import numpy
import NpuzzleState

#TODO change it, it should be more readable


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
    # TODO: is it good?
    return len(numpy.not_equal(state.state, state.final_terminal_state))


def u_h(state):
    pass


def heuristic_choise(heuristics, state):
    if heuristics is 'U':
        return 0

    if heuristics is 'M':
        return manhattan_heuristic(state)

    if heuristics is 'ML':
        pass

    if heuristics is 'H':
        return hemming_heuristic(state)

    if heuristics is 'E':
        pass

    if heuristics is 'D':
        pass
