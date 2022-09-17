from graphlib.metrics.graph_metric import GraphMetric
from graphlib.common.priority_queue import PriorityQueue
from collections import defaultdict

class AStarShortestPathMetric(GraphMetric):
    def __call__(self, fr, to, weight_func, heuristic_func):
        # Each tuple in the priority queue should be:
        # (hcost, weight, node, prev_edge)
        pq = PriorityQueue()
        pq.push((0, 0, fr, None))

        dist = defaultdict(lambda: float('inf'))
        edge = {}

        while pq:
            # The first value in the tuple (the heuristic) is unused.
            # It is important that it is the first element in the tuple because
            # the priority queue will minimize this value first
            _h, w, u, prev_edge = pq.pop()
            self.increment_nodes_counter()

            # If the target is found, return the path taken
            if u == to:
                path = []
                while to != fr:
                    path.append(to)
                    to = edge[to]
                path.append(to)
                return path[::-1]

            # Check all neighbors
            for curr_edge in self.graph.adj[u].edges:
                self.increment_edges_counter()
                v = curr_edge.to
                new_w = w + weight_func(prev_edge, curr_edge)
                if dist[v] > new_w:
                    dist[v] = new_w
                    edge[v] = u
                    self.increment_relaxation_counter()
                    pq.push((new_w + heuristic_func(v), new_w, v, curr_edge))

        # No path was found (usually impossible)
        return []
