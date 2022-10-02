from graphlib.metrics.paths.astar import AStarPathMetric


class DijkstraShortestPathMetric(AStarPathMetric):
    '''A specialization of A* with no heuristic function'''

    def __call__(self, fr, to, weight_func=None):
        self.set_heuristic_func(lambda u: 0)
        return super().__call__(fr, to, weight_func)
