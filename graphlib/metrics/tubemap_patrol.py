from graphlib.metrics.graph_metric import GraphMetric
from graphlib.metrics.paths import DijkstraShortestPathMetric
from graphlib.common.graph_utils import reconstruct_path
from collections import defaultdict
from functools import cache

class TubemapPatrolMetric(GraphMetric):
    def __init__(self, graph, stations, weight_func=lambda p, c: c.time):
        super().__init__(graph)
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
        # The python functools.cache (or lru_cache) decorator is very useful for dynamic programming in python
        # https://docs.python.org/3/library/functools.html#functools.cache
        @cache
        def tsp(u, remain):
            if remain == 0:
                return dist[u][start]
            c_min = float('inf')
            for v in filter(lambda v: remain & (1 << v), self.stations):
                c = tsp(v, remain & ~(1 << v)) + dist[u][v]
                if c_min > c:
                    c_min = c
                    pred[u][remain] = v
            return c_min

        # 'all_stations' is a bitmask where the i_th bit is set if it hasn't been visited yet
        # Ideally this would be a bitset (or frozenset, but slow to copy/hash), but this is python...
        # NOTE: Arbirarily large ids are slow with this method
        all_stations = 0
        for station in self.stations:
            all_stations |= (1 << station)
        g = tsp(start, all_stations)

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
        N = len(path)
        for i in range(N):
            fr, to = path[i-1], path[i]
            all_paths.append(reconstruct_path(fr, to, edge[fr]))
        return g, all_paths
