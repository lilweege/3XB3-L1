from graphlib.metrics.paths.astar import AStarShortestPathMetric

class DijkstraShortestPathMetric(AStarShortestPathMetric):
    def __call__(self, fr, to, weight_func):
        self.set_heuristic_func(lambda u: 0)
        return super().__call__(fr, to, weight_func)
