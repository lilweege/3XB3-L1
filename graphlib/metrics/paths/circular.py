from graphlib.metrics.paths.astar import AStarPathMetric
from math import cos, asin, sqrt, radians
AVG_EARTH_RADIUS = 6378

class CircularDistancePathMetric(AStarPathMetric):
    def __call__(self, fr, to, weight_func):
        def circ_dist(lat1, lon1, lat2, lon2): # https://en.wikipedia.org/wiki/Great-circle_distance
            return 2 * AVG_EARTH_RADIUS * asin(sqrt(0.5 - cos(radians(lat2-lat1))/2 + cos(radians(lat1)) * cos(radians(lat2)) * (1 - cos(radians(lon2-lon1)))/2))

        def heuristic(u):
            currNode = self.graph.adj[u]
            endNode = self.graph.adj[to]
            dist = circ_dist(currNode.latitude, currNode.longitude, endNode.latitude, endNode.longitude)
            return dist 

        self.set_heuristic_func(heuristic)
        return super().__call__(fr, to)