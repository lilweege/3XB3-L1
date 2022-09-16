import heapq

class PriorityQueue:
    def __init__(self):
        self.pq = []

    def push(self, x):
        heapq.heappush(self.pq, x)

    def pop(self):
        return heapq.heappop(self.pq)
    
    def __len__(self):
        return len(self.pq)