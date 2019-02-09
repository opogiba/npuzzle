from queue import PriorityQueue
from typing import Deque


class StateAnalyzeQueue(PriorityQueue):
    time_complexity = 0

    def __contains__(self, item):
        matches = (True for state in self.queue if item == state)
        return next(matches, False)

    def __len__(self):
        return self.qsize() + 1

    def put_nowait(self, item):

        if self.maxsize and self.maxsize == self.qsize():
            max_element = max(self.queue)

            if max_element:
                max_index = self.queue.index(max_element)
                self.queue.pop(max_index)
        return super().put_nowait(item)


class StateDeletedQueue(Deque):
    def __contains__(self, item):
        matches = (True for state in self if item == state)
        return next(matches, False)
