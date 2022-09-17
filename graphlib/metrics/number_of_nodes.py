from graphlib.metrics.graph_metric import GraphMetric

class NumberOfNodesMetric(GraphMetric):
    def __call__(self):
        return len(self.graph.adj)
