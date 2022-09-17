from graphlib.metrics.graph_metric import GraphMetric
from graphlib.metrics.astar import AStarShortestPathMetric

class DijkstraShortestPathMetric(GraphMetric):
    def __call__(self, fr, to, weight_func):
        return AStarShortestPathMetric(self.graph)(fr, to, weight_func, lambda u: 0)