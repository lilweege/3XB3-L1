from graphlib.metrics.graph_metric import GraphMetric

class NumberOfEdgesMetric(GraphMetric):
    def __call__(self):
        return self.graph.edges
