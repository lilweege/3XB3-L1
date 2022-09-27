from graphlib.metrics.paths.path_metric import PathMetric
from graphlib.common.priority_queue import PriorityQueue
from graphlib.common.graph_utils import reconstruct_path
from collections import defaultdict


class AStarPathMetric(PathMetric):
    '''
    Given a weight function and heuristic function, performs the A* algorithm
    on a graph. The <dist> and <edge> attributes store the distance between
    any pair of node, and the parent of any node, respectively.
    '''

    def set_heuristic_func(self, heuristic_func):
        self.heuristic_func = heuristic_func

    def __call__(self, fr, to, weight_func=None):
        self.reset_counters()

        # If either weight or heuristic functions are not set,
        # then use a sensible default
        weight_func = (lambda a, b: 1) if weight_func is None else weight_func
        heuristic_func = (lambda u: 0) if not hasattr(self, 'heuristic_func') \
            else self.heuristic_func

        # Each tuple in the priority queue should be:
        # (hcost, weight, node, prev_edge)
        pq = PriorityQueue()
        pq.push((0, 0, fr, None))

        self.dist = defaultdict(lambda: float('inf'))
        self.dist[fr] = 0
        self.edge = {}

        while pq:
            # The first value in the tuple (the heuristic) is unused.
            # It is important that it is the first element in the tuple because
            # the priority queue will minimize this value first
            _h, w, u, prev_edge = pq.pop()
            self.increment_nodes_counter()

            # If the target is found, return the path taken
            if u == to:
                return reconstruct_path(fr, to, self.edge)

            # Check all neighbors
            for curr_edge in self.graph.adj[u].edges:
                self.increment_edges_counter()
                v = curr_edge.to
                new_w = w + weight_func(prev_edge, curr_edge)
                # If possible, relax edge
                if self.dist[v] > new_w:
                    self.dist[v] = new_w
                    self.edge[v] = curr_edge
                    self.increment_relaxation_counter()
                    pq.push((new_w + heuristic_func(v), new_w, v, curr_edge))

        # No path was found
        return []
