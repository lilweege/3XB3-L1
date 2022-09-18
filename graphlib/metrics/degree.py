from graphlib.metrics.graph_metric import GraphMetric

class DegreeMetric(GraphMetric):
    def __init__(self, graph, u):
        super().__init__(graph)
        self.u = u

    def __call__(self):
        return len(self.graph.adj[self.u].edges)
