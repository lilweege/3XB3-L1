from graphlib.metrics.graph_metric import GraphMetric

class DegreeMetric(GraphMetric):
    def __call__(self, u):
        return len(self.graph.adj[u].edges)
