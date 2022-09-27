from graphlib.metrics.graph_metric import GraphMetric
from graphlib.graphs.bigraph import BiGraph
from graphlib.common.graph_utils import reconstruct_path
from collections import defaultdict

class TubemapIslandMetric(GraphMetric):
    def __call__(self):
        rep_node = {}
        components = defaultdict(list)

        def dfs(start, u):
            if u in rep_node:
                return
            rep_node[u] = start
            components[start].append(u)
            for edge in self.graph.adj[u].edges:
                if self.graph.adj[edge.fr].zone == self.graph.adj[edge.to].zone:
                    dfs(start, edge.to)

        for start in self.graph.adj.keys():
            dfs(start, start)

        zone_edges = []
        for node in self.graph.adj.values():
            for edge in node.edges:
                if edge.fr < edge.to:
                    if self.graph.adj[edge.fr].zone != self.graph.adj[edge.to].zone:
                        zone_edges.append(edge)

        return components, rep_node, zone_edges
