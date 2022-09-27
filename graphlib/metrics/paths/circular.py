from graphlib.metrics.paths.astar import AStarPathMetric
from math import cos, asin, sqrt, radians
AVG_EARTH_RADIUS = 6378


class CircularDistancePathMetric(AStarPathMetric):
    '''A specialization of A* with a circular distance heuristic function'''

    def __call__(self, fr, to, weight_func):
        def circ_dist(lat1, lon1, lat2, lon2):
            # https://en.wikipedia.org/wiki/Great-circle_distance
            c1 = cos(radians(lat2-lat1))
            c2 = cos(radians(lat1))
            c3 = cos(radians(lat2))
            c4 = cos(radians(lon2-lon1))
            d = 0.5 - c1/2 + c2 * c3 * (1 - c4)/2
            return 2 * AVG_EARTH_RADIUS * asin(sqrt(d))

        def heuristic(u):
            currNode = self.graph.adj[u]
            endNode = self.graph.adj[to]
            dist = circ_dist(
                currNode.latitude,
                currNode.longitude,
                endNode.latitude,
                endNode.longitude
            )
            return dist * 100

        self.set_heuristic_func(heuristic)
        return super().__call__(fr, to, weight_func)
