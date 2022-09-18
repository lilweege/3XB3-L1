from graphlib.metrics.paths.astar import AStarShortestPathMetric

class EuclidianDistanceShortestPathMetric(AStarShortestPathMetric):
    def __call__(self, fr, to, weight_func):
        def eucl_dist(x1, y1, x2, y2):
            # Omitting the square root is okay because the function is monotonic
            return (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1)
        def heuristic(u):
            currNode = self.graph.adj[u]
            endNode = self.graph.adj[to]
            dist = eucl_dist(currNode.latitude, currNode.longitude, endNode.latitude, endNode.longitude)
            return dist * 100 # FIXME: Arbitrary constant weighting of heuristic
        self.set_heuristic_func(heuristic)
        return super().__call__(fr, to)
