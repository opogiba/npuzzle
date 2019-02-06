import numpy

#TODO change it
def manhattan_h(state):
    manhattan_sum = 0

    for indx_pair, value in numpy.ndenumerate(state.state):
        for t_indx_pair, t_value in numpy.ndenumerate(state.final_terminal_state):
            if value == t_value:
                diff = numpy.subtract(indx_pair, t_indx_pair)
                abs_diff = abs(diff)
                manhattan_sum += sum(abs_diff)
                break
    return manhattan_sum


def heuristic_choise(heuristics, state):
    if heuristics is 'U':
        return 0

    if heuristics is 'M':
        return manhattan_h(state)

    if heuristics is 'ML':
        pass

    if heuristics is 'H':
        pass

    if heuristics is 'E':
        pass

    if heuristics is 'D':
        pass
