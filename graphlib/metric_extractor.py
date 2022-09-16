from graphlib.common.priority_queue import PriorityQueue
import math
from functools import lru_cache
from collections import defaultdict

class Itinerary:
    def __init__(self, u, v):
        self.station1 = u
        self.station2 = v
        self.search_strategy = None

    def set_search_strategy(self, strategy):
        self.search_strategy = strategy

    def shortest_path(self, timeWeight=1, connWeight=1, transferWeight=1):
        if timeWeight < 0: raise ValueError(f"timeWeight must be non-negative, got {timeWeight}")
        if connWeight < 0: raise ValueError(f"connWeight must be non-negative, got {connWeight}")
        if transferWeight < 0: raise ValueError(f"transferWeight must be non-negative, got {transferWeight}")
        if self.search_strategy is None: raise ValueError("No search stategy defined")

        weight = lambda prev_edge, curr_edge: (
            timeWeight * curr_edge.time +
            connWeight +
            transferWeight * bool(prev_edge and (curr_edge.line != prev_edge.line))
        )

        path = self.search_strategy(self.station1, self.station2, weight)
        return path

class GraphMetrics:
    def __init__(self, graph):
        self.graph = graph

    def dijkstras(self, fr, to, weight_func):
        return self.astar_impl(fr, to, weight_func, lambda u: 0)
    
    def astar_euclid(self, fr, to, weight_func):
        def eucl_dist(x1, y1, x2, y2):
            # return math.sqrt((x2-x1)**2+(y2-y1)**2)
            # Omitting the square root is okay because the function is monotonic
            return (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1)
        def heuristic(u):
            currNode = self.graph.adj[u]
            endNode = self.graph.adj[to]
            dist = eucl_dist(currNode.latitude, currNode.longitude, endNode.latitude, endNode.longitude)
            return dist * 100
        return self.astar_impl(fr, to, weight_func, heuristic)

    def astar_impl(self, fr, to, weight_func, heuristic_func, cache_funcs=True):
        if cache_funcs:
            # Add a cache layer to both weight and heuristic functions to avoid redundant computation
            # Use this if the functions are particularly expensive
            @lru_cache
            def weight(prev_edge, curr_edge):
                return weight_func(prev_edge, curr_edge)
            @lru_cache
            def heuristic(u):
                return heuristic_func(u)
        else:
            weight = weight_func
            heuristic = heuristic_func

        # Each tuple in the priority queue should be:
        # (hcost, weight, node, prev_edge)
        pq = PriorityQueue()
        pq.push((0, 0, fr, None))

        dist = defaultdict(lambda: 1e99)
        edge = {}
        # self.edges = []

        while pq:
            # The first value in the tuple (the heuristic) is unused.
            # It is important that it is the first element in the tuple because
            # the priority queue will minimize this value first
            _h, w, u, prev_edge = pq.pop()

            # If the target is found, return the path taken
            if u == to:
                # print(len(self.edges))
                path = []
                while to != fr:
                    path.append(to)
                    to = edge[to]
                path.append(to)
                return path[::-1]

            # Check all neighbors
            for curr_edge in self.graph.adj[u].edges:
                v = curr_edge.to
                new_w = w + weight(prev_edge, curr_edge)
                if dist[v] > new_w:
                    dist[v] = new_w
                    edge[v] = u
                    # self.edges.append((u, curr_edge))
                    pq.push((new_w + heuristic(v), new_w, v, curr_edge))

        # No path was found (usually impossible)
        return []

    def degree(self, u):
        return len(self.graph.adj[u].edges)

    def num_nodes(self):
        return len(self.graph.adj)
    
    def num_edges(self):
        return self.graph.edges

    # def number_of_lines(self, uu):
    #     vis = set()
    #     lines_of_uu = set()
    #     for root in list(self.graph.adj.keys()):
    #         q = deque()
    #         q.append(root)
    #         while len(q) != 0:
    #             u = q.pop()
    #             if u in vis:
    #                 continue
    #             vis.add(u)
    #             for v in self.graph.adj[u].edges:
    #                 if u == uu:
    #                     lines_of_uu.add(v.line)
    #                 q.append(v.to)
    #     return len(lines_of_uu)
