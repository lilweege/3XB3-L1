from graphlib.metrics.graph_metric import GraphMetric


class NumberOfNodesMetric(GraphMetric):
    '''Computes the number of nodes in a BiGraph'''
    def __call__(self):
        return len(self.graph.adj)
