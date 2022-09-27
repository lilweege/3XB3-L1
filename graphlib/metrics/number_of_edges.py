from graphlib.metrics.graph_metric import GraphMetric


class NumberOfEdgesMetric(GraphMetric):
    '''Computes the number of edges in a BiGraph'''
    def __call__(self):
        return self.graph.edges
