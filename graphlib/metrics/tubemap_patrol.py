from graphlib.metrics.graph_metric import GraphMetric
from graphlib.metrics.paths import DijkstraShortestPathMetric
from graphlib.common.graph_utils import reconstruct_path
from collections import defaultdict
from functools import cache


class TubemapPatrolMetric(GraphMetric):
    '''
    Solves the Travelling Salesman Problem for a Tubemap BiGraph
    NOTE: Each Edge (Connection) in a Tubemap should have a "time" attribute
    '''

    def __init__(self, graph, stations, weight_func=lambda p, c: c.time):
        super().__init__(graph)
        if len(stations) == 0:
            raise ValueError("stations must be a non-empty list")
        self.stations = stations
        self.weight_func = weight_func

    def __call__(self):
        # Compute the distance from every node to every other node
        dist = {}
        edge = {}
        for start in self.stations:
            search = DijkstraShortestPathMetric(self.graph)
            # Use -1 as the target node (which will never be found)
            # This way the entire graph will be searched (SSSP)
            search(start, -1, self.weight_func)
            dist[start] = search.dist
            edge[start] = search.edge

        pred = defaultdict(dict)
        start = self.stations[0]

        # The python functools.cache (or lru_cache) decorator is very useful
        # for dynamic programming in python
        # https://docs.python.org/3/library/functools.html#functools.cache

        @cache
        def tsp(u, remain):
            if remain == 0:
                return dist[u][start]
            min_cost = float('inf')
            for v in filter(lambda v: remain & (1 << v), self.stations):
                cost = tsp(v, remain & ~(1 << v)) + dist[u][v]
                if min_cost > cost:
                    min_cost = cost
                    pred[u][remain] = v
            return min_cost

        # 'all_stations' is a bitmask where the i_th bit is set if it hasn't
        # been visited yet. Ideally this would be a bitset (or frozenset,
        # but not slow to copy/hash), but this is python...
        # NOTE: Arbirarily large ids are slow with this method...
        # This could be avoided by relabelling stations starting at 1
        all_stations = 0
        for station in self.stations:
            all_stations |= (1 << station)
        best_cost = tsp(start, all_stations)

        # Reconstruct the path
        remain = all_stations & ~(1 << start)
        curr = start
        path = [curr]
        while remain:
            curr = pred[curr][remain]
            remain &= ~(1 << curr)
            path.append(curr)

        # Reconstruct "sub-paths"
        all_paths = []
        for i in range(len(path)):
            fr, to = path[i-1], path[i]
            all_paths.append(reconstruct_path(fr, to, edge[fr]))

        return best_cost, all_paths
