import heapq


class PriorityQueue:
    '''A wrapper for Python's heapq library'''

    def __init__(self):
        self.pq = []

    def push(self, x):
        heapq.heappush(self.pq, x)

    def pop(self):
        return heapq.heappop(self.pq)

    def __len__(self):
        return len(self.pq)
