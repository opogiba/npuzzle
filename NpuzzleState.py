import numpy
from heuristic import heuristic_choise
from hashlib import sha1


class NpuzzleState:

    TERMINAL_STATES = {
        3: numpy.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]]),
        4: numpy.array([[1, 2, 3, 4], [12, 13, 14, 5], [11, 0, 15, 6], [10, 9, 8, 7]]),
        5: numpy.array([[1, 2, 3, 4, 5], [16, 17, 18, 19, 6], [15, 24, 0, 20, 7], [14, 23, 22, 21, 8], [13, 12, 11, 10, 9]] )
    }
    final_terminal_state = None
    heuristic = None

    def __init__(self, state, parent_state=None):
        self.state = state
        self.parent = parent_state
        self.g_coff = parent_state.g_coff + 1 if parent_state else 0
        self.empty_puzzle_coord = self.empty_element_coordinates(self.state)
        self.f_coff = None
        self.hash = sha1(self.state).hexdigest()

    def set_f(self, g=None):
        if not g:
            self.f_coff = self.g_coff + heuristic_choise(NpuzzleState.heuristic, self)
        else:
            self.g_coff = g
            self.f_coff = self.g_coff + heuristic_choise(NpuzzleState.heuristic, self)

    def shift_puzzle(self, direction):
        row_indx, col_indx = self.empty_puzzle_coord

        directions = {
            'up_direction': (row_indx - 1, col_indx),
            'down_direction': (row_indx + 1, col_indx),
            'right_direction': (row_indx, col_indx + 1),
            'left_direction': (row_indx, col_indx - 1)
        }

        new_coords = directions[direction]
        return new_coords

    def empty_element_coordinates(self, npuzzle):
        for indx_pair, elem in numpy.ndenumerate(npuzzle):
            if elem == 0:
                return indx_pair

    @classmethod
    def set_final_terminal_state(cls, size, heuristic):
        cls.final_terminal_state = cls.TERMINAL_STATES.get(size)
        cls.heuristic = heuristic

    def __str__(self):
        return str(self.state).replace('[[', ' ').replace(']]', ' ').replace('[', '').replace(']', '')

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.hash == other.hash

    def __lt__(self, other):
        return self.f_coff < other.f_coff

    def __le__(self, other):
        return self.f_coff <= other.f_coff

    def __gt__(self, other):
        return self.f_coff > other.f_coff

    def __ge__(self, other):
        return self.f_coff >= other.f_coff
