import heapq


class PriorityQueue:

    def __init__(self):
        self._queue = []
        self._index = 0

    def insert(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1
        print("Queue size: ", self._index)

    def remove(self):
        # self._index -= 1
        return heapq.heappop(self._queue)[-1]

    def is_empty(self):
        return len(self._queue) == 0

    def is_exist(self, item):
        pass
